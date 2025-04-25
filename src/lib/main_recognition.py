import face_recognition
import cv2
import numpy as np
import db_interface
from enum import Enum
from PIL import Image, ImageDraw, ImageFont

video_capture = cv2.VideoCapture(0)

class RecognitionModes(Enum):
    REGISTER = 1
    RECOGNIZE = 2

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
        # for i in range(len(record)):
            # known_records[i].append(record[i])

    return known_records


def retrieve_frame(mode : RecognitionModes | None = None) -> Image:
    known_records = retrieve_db_data()
    # known_records = [id, name, face_encodings, course, year]

    print(known_records)
    print(f'Known Face ID: {known_records[0]}')
    print(f'Known Face Names: {known_records[1]}')
    print(f'Known Face Encodings: {known_records[2]}')
    print(f'Known Face Course: {known_records[3]}')
    print(f'Known Face Year: {known_records[4]}')

    face_locations = []
    face_encodings = []
    face_names = []

    frame = video_capture.read()[1]
    rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    flipped_frame = cv2.flip(rotated_frame, 1)
    rgb_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
    x, y, width, height = 125, 600, 700, 700
    cropped_frame = rgb_frame[y:y+height, x:x+width]


    resized_frame = cv2.resize(cropped_frame, (0,0), fx=0.25, fy=0.25)
    face_locations = face_recognition.face_locations(resized_frame) # Get all faces in the frame
    face_encodings = face_recognition.face_encodings(resized_frame, face_locations) # Encode those faces

    face_names = []
    
    # Just for the names
    for face_encoding in face_encodings:
        name = "Unknown"
        if len(known_records[2]) > 0: # Because compare_faces breaks when face_encodings is empty.
            matches = face_recognition.compare_faces(known_records[2], face_encoding)
            face_distances = face_recognition.face_distance(known_records[2], face_encoding)
            best_match_index = np.argmin(face_distances) # find the smallest value of 'face_distances' by index

            if matches[best_match_index]:
                name = known_records[1][best_match_index]

        face_names.append(name)

    if face_locations:
        print(f'Faces detected: {len(face_locations)} at {face_locations}')

    cv2_image : Image = Image.fromarray(cropped_frame)
    new_cv2_image = ImageDraw.ImageDraw(cv2_image)
    
    # This section just draws stuff on the frame.
    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        left *= 4
        right *= 4
        bottom *= 4

        text_to_draw = f"Name: {name}\nID: {top}"


        new_cv2_image.rectangle([left, top, right, bottom], width=10) # The bounding square
        # new_cv2_image.rectangle([left, bottom, right, bottom + 100], fill='red')
        image_font = ImageFont.truetype('Lexend.ttf', size=15)
        new_cv2_image.multiline_text([left, bottom, right, bottom + 50], text=text_to_draw, font=image_font)
        
    # new_cv2_image.point([50, 5], fill='red')
    # new_cv2_image.point([100, 100], fill='blue')

    return cv2_image


    

        

