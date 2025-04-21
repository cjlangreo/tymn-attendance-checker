from PIL import Image
import sqlite3
import tempfile

img_path = 'image_source/chanz.jpg'

con = sqlite3.connect('app/main_face_recognition/faces.db')
cur = con.cursor()

def image_to_db(image):
    bnw_image = Image.open(image).convert('1')
    temp_name = tempfile.NamedTemporaryFile(suffix='.jpg')
    bnw_image.save(temp_name)

    with open(temp_name.name, 'rb') as file:
        temp_image = file.read()

    data_to_db = [
        11172,
        "Chanz Jryko",
        temp_image,
        "BSCS",
        4
    ]
    
    cur.execute("INSERT INTO registered_students VALUES(?, ?, ?, ?, ?)", data_to_db)




res = cur.execute("SELECT face_encodings FROM registered_students WHERE id=11172")

with open('yeah.png', 'wb') as file:
    file.write(res.fetchone()[0])


con.commit()
con.close()