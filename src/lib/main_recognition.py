import face_recognition
import cv2
import time
from lib import db_interface
from lib.img_manip import TEMP_IMAGE_PATH, frame_to_bytes
from PIL import Image, ImageDraw, ImageFont, ImageTk
import tkinter
import numpy as np

video_capture = cv2.VideoCapture(2)

def update_label_image(dest_label : tkinter.Label, src_image):
    tk_image = ImageTk.PhotoImage(src_image)
    dest_label.configure(image=tk_image)
    dest_label.image = tk_image

def start_face_recognition(dest_label : tkinter.Label, master_window : tkinter.Toplevel, mode : str):
    known_face_encodings = []
    process_this_frame : bool = True
    prev_name = ''
    start_time = time.time()
    time_left = start_time + 3

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
            face_locations = face_recognition.face_locations(resized_frame) # Get all faces in the frame
            face_encodings = face_recognition.face_encodings(resized_frame, face_locations) # Encode those faces
        
            if face_locations:
                print(f'Faces detected: {len(face_locations)} at {face_locations}')
            

            frame_image : Image = Image.fromarray(cropped_frame)
            image_draw_frame = ImageDraw.ImageDraw(frame_image)
            
            face_names = []
            name = "Unknown"
            
            # Match the names
            try:
                matches : list[any] = face_recognition.compare_faces(known_face_encodings, face_encodings[0])
                face_distances = face_recognition.face_distance(known_face_encodings, face_encodings[0])
                best_match_index = np.argmin(face_distances) # find the smallest value of 'face_distances' by index
        
                if matches[best_match_index]:
                    name = known_records[1][best_match_index]
            except Exception as e:
                print(e)

            face_names.append(name)

            box_outline_color = 'white'

            match mode:
                case 'register':
                    if face_encodings:
                        if prev_name == name:
                            print('Face recognized')
                            print(f'Time remaining: {time_left - time.time()}')
                    else:
                        start_time = time.time()
                        time_left = start_time + 3


            if (start_time + 3) - time.time() < 0:
                match mode:
                    case 'register':
                        db_interface.insert_into_db(
                            11172,
                            'Chanz',
                            frame_to_bytes(cropped_frame, 11172),
                            'BSIT',
                            1
                        )
                        image_draw_frame.rectangle([left, top, right, bottom], width=10, fill='red') # The bounding square
                        master_window.destroy()
                        break
                
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

    

        

