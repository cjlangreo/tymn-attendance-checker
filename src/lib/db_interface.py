"""
Hello
"""
from PIL import Image
import sqlite3
from lib import img_manip

con = sqlite3.connect('../faces.db')
cur = con.cursor()


def insert_into_db(binary_img, id : int, name : str, course : str, year : int) -> None:
    """
    Inserts passed arguments as values in a new record into the database

    :param binary_img: A binary array of an image from image_to_db(img_path)
    :param id: The new record's ID i.e. student ID
    :param name: The new record's name i.e. "Chanz Jryko"
    """
    data_to_db = [
        id,
        name,
        binary_img,
        course,
        year
    ]
    
    cur.execute("INSERT INTO registered_students VALUES(?, ?, ?, ?, ?)", data_to_db)

def pull_from_db(id : int, values : tuple | None = None):
    if values:
        res = cur.execute(f"SELECT {values} FROM registered_students WHERE id={id}")
    else:
        res = cur.execute(f"SELECT * FROM registered_students WHERE id={id}")
    return res.fetchone()


con.commit()
con.close()