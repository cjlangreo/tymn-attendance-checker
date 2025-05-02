import tkinter as tkinter
import threading
from lib.main_recognition import start_face_recognition
from lib.img_manip import create_temp_folder, bytes_to_image
from lib.db_interface import pull_from_db, ColumnFilters

def load_all_images():
    records = pull_from_db(values=(ColumnFilters.ID, ColumnFilters.IMAGE_ARRAY))
    for record in records:
        bytes_to_image(record[1], record[0])

def open_register_window(master):
    recog_window = tkinter.Toplevel(master)
    recog_window.title('Register New Student')
    
    image_label = tkinter.Label(recog_window)
    image_label.pack()
    
    face_recog_thread = threading.Thread(target=start_face_recognition, args=(image_label, recog_window, 'register'))
    face_recog_thread.start()

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
    create_temp_folder()
    start_gui()