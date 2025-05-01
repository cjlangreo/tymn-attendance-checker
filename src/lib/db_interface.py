"""
Hello
"""
import sqlite3
from os import path

db_path = 'src/lib/faces.db'

class ColumnFilters:
    ID = 'id'
    NAME = 'name'
    IMAGE_ARRAY = 'image_array'
    COURSE = 'course'
    YEAR = 'year'

class Courses:
    BSCS = 'BSCS'
    BSIT = 'BSIT'
    BSA = 'BSA'
    BSHM = 'BSHM'
    BSEE = 'BSEE'
    BSCE = 'BSCE'
    BSME = 'BSME'
    BSOA = 'BSOA'
    BSBA = 'BSBA'

if not path.exists(db_path):
    print('Database file doesn\'t exist, creating it now.')
    open(db_path, 'w')
    con = sqlite3.connect(db_path)    
    cur = con.cursor()

    cur.execute("""
                CREATE TABLE "courses" (
                "course"	TEXT,
                PRIMARY KEY("course")
                );
                """)
    
    con.commit()
    
    cur.execute("""
                CREATE TABLE "registered_students" (
                "id"	INTEGER,
                "name"	TEXT NOT NULL,
                "image_array"	BLOB NOT NULL,
                "course"	TEXT NOT NULL,
                "year"	INTEGER NOT NULL,
                FOREIGN KEY("course") REFERENCES "courses"("course") ON UPDATE CASCADE,
                PRIMARY KEY("id")
            );
                """)
    
    con.commit()



con = sqlite3.connect(db_path, check_same_thread=False)
cur = con.cursor()


def insert_into_db(id : int, name : str, image_array, course : str, year : int) -> None:
    """
    Inserts passed arguments as values in a new record into the database

    :param image_array: A binary array of an image from image_to_db(img_path)
    :param id: The new record's ID i.e. student ID
    :param name: The new record's name i.e. "Chanz Jryko"
    """
    data_to_db = [
        id,
        name,
        image_array,
        course,
        year
    ]
    
    cur.execute("INSERT INTO registered_students VALUES(?, ?, ?, ?, ?)", data_to_db)

    con.commit()

def pull_from_db(values : tuple[ColumnFilters] | None = '*', filter : tuple[ColumnFilters, any] | None = '') -> list[tuple]:
    """
    Queries the database.

    Args:
        values (tuple[ColumnFilters]): A tuple[ColumnFilters] to select what columns to query.
        filter (tuple[ColumnFilters, any]): A tuple[ColumnFilters, any] to filter the query by column with a value.

    Returns:
        list[tuple]: A list containing all the records from the query.
    """

    if filter:
        filter = f" WHERE {filter[0]}='{filter[1]}'"

    res = cur.execute(f"SELECT {values} FROM registered_students{filter}")

    return res.fetchall()
