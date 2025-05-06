import face_recognition
import cv2
import time
from lib.db_interface import RegStdsColumns, Courses, insert_into_db, Tables, pull_from_db
from lib.img_manip import TEMP_IMAGE_PATH, frame_to_bytes
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter
import customtkinter as ctk
import numpy as np
import os

video_capture = cv2.VideoCapture(2)

class Student:
    def __init__(self):
        self.id : int = None
        self.name : str = None
        self.course : Courses = None
        self.year : int = None
        self.temp_frame = None
        self.label_indicator = None
        self.register_button = ctk.CTkButton
        self.date = None
        self.time = None

    def submit_student(self, table : Tables):
        if table == Tables.REGISTERED_STUDENTS:
            insert_into_db(
                table=table,
                id=self.id,
                name=self.name,
                image_array=frame_to_bytes(self.temp_frame, self.id),
                course=self.course,
                year=self.year
            )
        elif table == Tables.ATTENDANCE:
            self.set_date_time()
            insert_into_db(
                table=table,
                date=self.date,
                time=self.time,
                id=self.id
            )

    def set_temp_frame(self, frame):
      self.label_indicator.configure(text="Face registered! ✔")
      self.register_button.configure(border_color="#474747")
      self.temp_frame = frame

    def set_date_time(self):
        self.date = time.strftime("%Y-%m-%d")
        self.time = time.strftime("%H:%M:%S")


def _value_to_hex(value, max, multiplier, reverse : bool = False) -> float:
    if value > max:
        value =  max

    if reverse:
        value = max - value

    hex_value = int((value / max) * multiplier)
    return f'{hex_value:02x}'

def get_known_records():
    records = pull_from_db(table=(Tables.REGISTERED_STUDENTS, ), values=(RegStdsColumns.ID, RegStdsColumns.NAME, RegStdsColumns.COURSE, RegStdsColumns.YEAR)) # [(id, name, course, year), (...)}
    
    known_id = []
    known_name = []
    known_course = []
    known_year = []
    known_face_encoding = []

    for record in records:
        known_id.append(record[0])
        known_name.append(record[1])
        known_course.append(record[2])
        known_year.append(record[3])

        # Convert the image array to a numpy array
        image = face_recognition.load_image_file(TEMP_IMAGE_PATH + str(record[0]) + '.jpg')
        # Encode the face
        face_encodings = face_recognition.face_encodings(image)
        
        if len(face_encodings) > 0:
            known_face_encoding.append(face_encodings[0])  # Add only the first face encoding
        else:
            print(f"Warning: No face detected in image for ID {record[0]}")
    
    return known_id, known_name, known_course, known_year, known_face_encoding


def update_label_image(dest_label : tkinter.Label, src_image):
    tk_image = ImageTk.PhotoImage(src_image)
    dest_label.configure(image=tk_image)
    dest_label.image = tk_image


def start_face_recognition(dest_label : tkinter.Label, master_window : tkinter.Toplevel, mode : str, student : Student):
    known_ids, known_names, known_courses, known_years, known_face_encodings = get_known_records() # [(id, name, course, year, face_encoding), (...)]
    known_face_encodings = np.array(known_face_encodings)
    process_this_frame : bool = True
    prev_name = ''
    time_left = time.time() + 3
    text_to_draw = ''

    face_location = []
    face_encoding = []
    matches = []
    best_match_index = None

    while True:
        if process_this_frame:
            frame = video_capture.read()[1]
            rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
            # flipped_frame = cv2.flip(rotated_frame, 1)
            rgb_frame = cv2.cvtColor(rotated_frame, cv2.COLOR_BGR2RGB)
            
            X = 125
            Y = 600
            WIDTH = 700
            HEIGHT = 700
        
            cropped_frame = rgb_frame[Y:Y+HEIGHT, X:X+WIDTH]
        
            resized_frame = cv2.resize(cropped_frame, (0,0), fx=0.25, fy=0.25)

            frame_image : Image = Image.fromarray(cropped_frame)
            image_draw_frame = ImageDraw.ImageDraw(frame_image)

            id = "Unknown"
            name = "Unknown"
            course = "Unknown"
            year = "Unknown"
        
            try:
                face_location = face_recognition.face_locations(resized_frame) # Get all faces in the frame
                face_encoding = face_recognition.face_encodings(resized_frame, face_location) # Encode those faces
                matches = face_recognition.compare_faces(known_face_encodings, face_encoding, tolerance=0.4)
                face_distances = face_recognition.face_distance(known_face_encodings, face_encoding[0])
                best_match_index = np.argmin(face_distances)
                if matches[best_match_index]:
                    id = known_ids[best_match_index]
                    name = known_names[best_match_index]
                    course = known_courses[best_match_index]
                    year = known_years[best_match_index]
            except:
                print('No faces found')


            prev_name = name
        
            print('Time left:', time_left - time.time())

            color = 'white'

            if mode == 'r':
                color = f'#ff{_value_to_hex(time_left - time.time(), 3, 255, True)}{_value_to_hex(time_left - time.time(), 3, 255, True)}'
            elif mode == 'a':
                if name == 'Unknown':
                    color = 'red'
                color = f'#{_value_to_hex(time_left - time.time(), 3, 255)}ff{_value_to_hex(time_left - time.time(), 3, 255)}'


            if (name == prev_name) and (face_location != []):
                if mode == 'r' and name == 'Unknown':
                    if (time.time() > time_left):
                        student.set_temp_frame(cropped_frame)
                        master_window.destroy()
                        break
                elif mode == 'a' and name != 'Unknown':
                    if (time.time() > time_left):
                        student.id = id
                        student.submit_student(Tables.ATTENDANCE)
                        master_window.destroy()
                        break
                else:
                    time_left = time.time() + 3
            else:
                time_left = time.time() + 3
                        
            text_to_draw = f"Name: {name}\nID: {id}\nCourse: {course}\nYear: {year}"

            if face_location != []:
                top, right, bottom, left = face_location[0]
                top *= 4
                left *= 4
                right *= 4
                bottom *= 4
    
                # color = f'#{_value_to_hex(time_left - time.time(), 3)}{_value_to_hex(time_left - time.time(), 3)}{_value_to_hex(time_left - time.time(), 3)}'
                image_draw_frame.rectangle([left, top, right, bottom], width=10, outline=color) # The bounding square
                image_font = ImageFont.truetype('src/lib/Lexend.ttf', size=15)
                image_draw_frame.multiline_text([left, bottom, right, bottom + 50], text=text_to_draw, font=image_font, fill=color)


            
            update_label_image(dest_label, frame_image)

        process_this_frame = not process_this_frame
