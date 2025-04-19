import face_recognition
import cv2
import numpy as np
import os

directory = 'image_source'

video_capture = cv2.VideoCapture(0)

known_face_encodings = []
known_face_names = []

for filename in os.listdir(directory):
    file_path = os.path.join(directory, filename)
    if os.path.isfile(file_path):
        image = face_recognition.load_image_file(file_path)
        image_face_encoding = face_recognition.face_encodings(image)[0]

        
        known_face_encodings.append(image_face_encoding)
        face_name = os.path.basename(os.path.splitext(file_path)[0]).capitalize()
        print(face_name)
        known_face_names.append(face_name)

print(f'Known Face Encodings: {known_face_encodings}')
print(f'Known Face Names: {known_face_names}')

face_locations = []
face_encodings = []
face_names = []
process_this_frame = True

while True:
    ret, frame = video_capture.read()

    frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)



    if process_this_frame:
        small_frame = cv2.resize(frame, (0, 0), fx=0.25, fy=0.25)

        rgb_small_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
        
        face_locations = face_recognition.face_locations(rgb_small_frame)
        face_encodings = face_recognition.face_encodings(rgb_small_frame, face_locations)

        face_names = []
        for face_encoding in face_encodings:
            matches = face_recognition.compare_faces(known_face_encodings, face_encoding)
            name = "Unknown"

            face_distances = face_recognition.face_distance(known_face_encodings, face_encoding)
            best_match_index = np.argmin(face_distances)
            if matches[best_match_index]:
                name = known_face_names[best_match_index]

            face_names.append(name)

    process_this_frame = not process_this_frame


    for (top, right, bottom, left), name in zip(face_locations, face_names):
        top *= 4
        right *= 4
        bottom *= 4
        left *= 4

        cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

        cv2.rectangle(frame, (left, bottom - 35), (right, bottom), (0, 0, 255), cv2.FILLED)
        font = cv2.FONT_HERSHEY_DUPLEX
        cv2.putText(frame, name, (left + 6, bottom - 6), font, 1.0, (255, 255, 255), 1)

    x, y, width, height = 500, 500, 1000, 1000

    cropped_frame = frame[y:y+height, x:x+width]
    resized_frame = cv2.resize(cropped_frame, (0,0), fx=0.5, fy=0.5)
    cv2.imshow('Video', resized_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

video_capture.release()
cv2.destroyAllWindows()