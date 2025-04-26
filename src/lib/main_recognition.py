import face_recognition
import cv2

video_capture = cv2.VideoCapture(0)

def retrieve_frame_data() -> tuple:
    frame = video_capture.read()[1]
    rotated_frame = cv2.rotate(frame, cv2.ROTATE_90_CLOCKWISE)
    flipped_frame = cv2.flip(rotated_frame, 1)
    rgb_frame = cv2.cvtColor(flipped_frame, cv2.COLOR_BGR2RGB)
    x, y, width, height = 125, 600, 700, 700
    cropped_frame = rgb_frame[y:y+height, x:x+width]

    resized_frame = cv2.resize(cropped_frame, (0,0), fx=0.25, fy=0.25)
    face_locations = face_recognition.face_locations(resized_frame) # Get all faces in the frame
    face_encodings = face_recognition.face_encodings(resized_frame, face_locations) # Encode those faces

    if face_locations:
        print(f'Faces detected: {len(face_locations)} at {face_locations}')

    return (cropped_frame, face_encodings, face_locations)


    

        

