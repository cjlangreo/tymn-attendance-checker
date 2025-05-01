import tkinter as tkinter
import threading
import numpy as np
import face_recognition
import time
from PIL import ImageTk, Image, ImageDraw, ImageFont
from lib import main_recognition
from lib import db_interface

def retrieve_db_data():
    records = db_interface.pull_from_db()

    known_face_ids = []
    known_face_names = []
    known_face_encodings = []
    known_face_courses = []
    known_face_years = []
    known_records = [known_face_ids, known_face_names, known_face_encodings, known_face_courses, known_face_years]

    # We take the records list of type list[tuple] returned from db_interface.pull_from_db() and supply the known_records' lists with those records.
    for record in records:
        # record = (id, name, face_encodings, course, year)
        for known_record, column in zip(known_records, record):
            known_record.append(column)

    return known_records


def update_label_image(dest_label : tkinter.Label, src_image):
    tk_image = ImageTk.PhotoImage(src_image)
    dest_label.configure(image=tk_image)
    dest_label.image = tk_image


def start_face_recognition(dest_label : tkinter.Label, master_window : tkinter.Toplevel, mode : str | None = None):
    """

    Args:
        dest_label:
        mode: hello
    """
    known_records = retrieve_db_data()
    process_this_frame : bool = True
    prev_name = ''
    start_time = time.time()
    time_left = start_time + 3

    while True:
        if process_this_frame:
            frame_data = main_recognition.retrieve_frame_data() # (frame, face_encodings, face_locations)
            
            frame = frame_data[0]
            face_encodings = frame_data[1]
            face_locations = frame_data[2]

            frame_image : Image = Image.fromarray(frame)
            image_draw_frame = ImageDraw.ImageDraw(frame_image)
            
            face_names = []
            name = "Unknown"
            
            # Match the names
            if len(known_records[2]) > 0 and len(face_encodings) > 0: # Because compare_faces breaks when face_encodings is empty.
                matches : list[any] = face_recognition.compare_faces(known_records[2], face_encodings[0])
                print(matches)
                face_distances = face_recognition.face_distance(known_records[2], face_encodings[0])
                best_match_index = np.argmin(face_distances) # find the smallest value of 'face_distances' by index
        
                if matches[best_match_index]:
                    name = known_records[1][best_match_index]

            face_names.append(name)

            box_outline_color = 'white'

            if face_encodings:
                if prev_name == name:
                    print('Face recognized')
                    print(f'Time remaining: {time_left - time.time()}')
            else:
                start_time = time.time()
                time_left = start_time + 3

            if (start_time + 3) - time.time() < 0:
                image_draw_frame.rectangle([left, top, right, bottom], width=10, outline='red') # The bounding square
                master_window.destroy()
                

        
            prev_name = name
            
            for (top, right, bottom, left), name in zip(face_locations, face_names):
                top *= 4
                left *= 4
                right *= 4
                bottom *= 4
        
                text_to_draw = f"Name: {name}\nID: {top}"
        
                image_draw_frame.rectangle([left, top, right, bottom], width=10, outline=box_outline_color) # The bounding square
                image_font = ImageFont.truetype('src/lib/Lexend.ttf', size=15)
                image_draw_frame.multiline_text([left, bottom, right, bottom + 50], text=text_to_draw, font=image_font)
            
        process_this_frame = not process_this_frame
        update_label_image(dest_label, frame_image)


def open_register_window(master):
    recog_window = tkinter.Toplevel(master)
    recog_window.title('Register New Student')
    
    image_label = tkinter.Label(recog_window)
    image_label.pack()
    
    face_recog_thread = threading.Thread(target=start_face_recognition, args=(image_label, recog_window,))
    face_recog_thread.start()
    recog_window.wait_window()

class MainWindow:
    def __init__(self, master : tkinter.Tk):
        self.master = master
        self.master.title('Student Facial-recognition Attendance')
        
        self.label = tkinter.Label(self.master, text='Test Label')
        self.label.pack()

        self.register_student_btn = tkinter.Button(self.master, text='Register New Student', command=lambda: open_register_window(self.master))
        self.register_student_btn.pack()

        self.take_attendance_btn = tkinter.Button(self.master, text='Take Attendance')
        self.take_attendance_btn.pack()
        
def start_gui():
    root = tkinter.Tk()
    MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    start_gui()