"""
Hello
"""
import sqlite3
from os import path, rename
from lib.img_manip import TEMP_IMAGE_PATH

db_path = 'src/lib/faces.db'

class RegStdsColumns:
    ID = 'id'
    NAME = 'name'
    IMAGE_ARRAY = 'image_array'
    COURSE = 'course'
    YEAR = 'year'

class AttendanceColumns:
    DATE = 'date'
    TIME = 'time'
    ID = 'student'

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
    REGISTERED_STUDENTS = 'registered_students'
    ATTENDANCE = 'attendance'

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
        cur.execute(f"INSERT INTO {table} VALUES(?, ?, ?, ?, ?)", data_to_db)
        
    else:
        data_to_db = [
            date,
            time,
            id
        ]
        cur.execute(f"INSERT INTO {table} VALUES(?, ?, ?)", data_to_db)



    con.commit()

def pull_from_db(table : tuple[Tables], values : tuple[RegStdsColumns | AttendanceColumns] | None = '*', filter : tuple[(RegStdsColumns | AttendanceColumns, any)] | None = '') -> list[tuple]:
    """
    Takes a tuple of Tables (and JOIN if multiple) and queries them with the passed values and filter arguments.

    Args:
        table (tuple[Tables]): Takes a tuple consisting of Tables and JOINs them if > 1.
        values (tuple[RegStdsColumns | AttendanceColumns]): Takes a tuple of either RegStdsColumns or AttendanceColumns to return only those columns.
        filter (tuple[RegStdsColumns | AttendanceColumns, any): Takes a tuple of either RegStdsColumns or AttendanceColumns and a value to filter those columns with.
    """
    if filter:
        filter = f" WHERE {filter[0][0]}='{filter[1]}'"

    if values != '*':
        values = ', '.join(values)
        
        
    if len(table) == 2:
        table = f'{table[0]} JOIN {table[1]} ON {table[0]}.id = {table[1]}.student'    
    else:
        table = ', '.join(table)
        
    
    query = f"SELECT {values} FROM {table}{filter}"
    res = cur.execute(query)

    return res.fetchall()


def update_student(old_student_id : int, column_values : tuple[(RegStdsColumns, any)]):
    registered_student_values = ', '.join(f"{col[0]} = '{col[1]}'" for col in column_values)
    registered_students_query = f'UPDATE {Tables.REGISTERED_STUDENTS} SET {registered_student_values} WHERE {RegStdsColumns.ID} = {old_student_id}'
    print(f'Registered students table query: {registered_students_query}')
    cur.execute(registered_students_query)
    print('Successfully updated Registered Students Record')

    if column_values[0][1] != old_student_id:
        attendance_values = f"{AttendanceColumns.ID} = '{column_values[0][1]}'"
        attendance_query = f'UPDATE {Tables.ATTENDANCE} SET {attendance_values} WHERE {AttendanceColumns.ID} = {old_student_id}'
        print(f'Attendance table query: {attendance_query}')
        cur.execute(attendance_query)

        old_image_path = f"{TEMP_IMAGE_PATH}{old_student_id}.jpg"
        new_image_path = f"{TEMP_IMAGE_PATH}{column_values[0][1]}.jpg"

        rename(old_image_path, new_image_path)
        print('Successfully updated Attendance Record')

    con.commit()