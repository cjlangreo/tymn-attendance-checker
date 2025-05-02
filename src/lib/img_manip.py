"""
A utility module.
"""
from PIL import Image
import tempfile
from os import mkdir
from shutil import rmtree
import time

TEMP_IMAGE_PATH = '/tmp/face_recognition/'


def delete_temp_folder():
    """
    Deletes the temporary folder.
    """
    try:
        rmtree(TEMP_IMAGE_PATH)
    except Exception as e:
        print(e)
        
        
def create_temp_folder():
    """
    Creates a temporary folder to store images.
    """
    try:
        mkdir(TEMP_IMAGE_PATH)
    except FileExistsError:
        delete_temp_folder()
        create_temp_folder()


def frame_to_bytes(frame, student_id: int) -> bytes:
    """
    Takes a frame and converts it into a byte array. Also stores the image in a temporary folder as a side effect. For use to store into the database.

    Args:
        img_path (str): A compatbile MatLike.
        student_id (int): The student's ID whose photo image is being processed. To be used as the image's name.
        
    Returns:
        image_byte_array: The image's byte array.
    """
    temp_image_name = str(student_id)
    image = Image.fromarray(frame)
    bnw_image = image.convert('L')
    bnw_image_path = TEMP_IMAGE_PATH + temp_image_name + '.jpg'
    bnw_image.save(bnw_image_path)

    with open(bnw_image_path, 'rb') as file:
        image_byte_array = file.read()


    return image_byte_array

def bytes_to_image(byte_array : bytes, student_id : int) -> str:
    temp_image_name = str(student_id)
    temp_image_path = TEMP_IMAGE_PATH + temp_image_name + '.jpg'
    with open(temp_image_path, 'wb') as file:
        file.write(byte_array)