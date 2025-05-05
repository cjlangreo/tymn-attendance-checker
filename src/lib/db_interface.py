"""
Hello
"""
import sqlite3
from os import path

db_path = 'src/lib/faces.db'

class RegStdsColumns:
    ID = 'rs.id'
    NAME = 'rs.name'
    IMAGE_ARRAY = 'rs.image_array'
    COURSE = 'rs.course'
    YEAR = 'rs.year'

class AttendanceColumns:
    DATE = 'a.date'
    TIME = 'a.time'
    ID = 'a.student'

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

class Tables:
    REGISTERED_STUDENTS = 'registered_students rs'
    ATTENDANCE = 'attendance a'

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


def insert_into_db(table : Tables, id : int | None = None, name : str | None = None, image_array : None=None, course : str | None=None, year : int | None=None, date : str | None=None, time : str | None=None) -> None:
    """
    Inserts passed arguments as values in a new record into the database

    :param image_array: A binary array of an image from image_to_db(img_path)
    :param id: The new record's ID i.e. student ID
    :param name: The new record's name i.e. "Chanz Jryko"
    """
    
    if table == Tables.REGISTERED_STUDENTS:
        data_to_db = [
            id,
            name,
            image_array,
            course,
            year
        ]
        cur.execute(f"INSERT INTO {table.split(maxsplit=1)[0]} VALUES(?, ?, ?, ?, ?)", data_to_db)
        
    else:
        data_to_db = [
            date,
            time,
            id
        ]
        cur.execute(f"INSERT INTO {table.split(maxsplit=1)[0]} VALUES(?, ?, ?)", data_to_db)



    con.commit()

def pull_from_db(table : tuple[Tables], values : tuple[RegStdsColumns | AttendanceColumns] | None = '*', filter : tuple[(RegStdsColumns | AttendanceColumns, any)] | None = '') -> list[tuple]:
    if filter:
        filter = f" WHERE {filter[0]}='{filter[1]}'"

    if values != '*':
        values = ', '.join(values)
        
    query = f"SELECT {values} FROM {table}{filter}"
    print(query)

    res = cur.execute(query)

    return res.fetchall()
