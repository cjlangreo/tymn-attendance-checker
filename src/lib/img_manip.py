"""
A utility module.
"""
from PIL import Image
from _io import BufferedReader
import tempfile
from uuid import uuid4


def image_to_binary(img_path : str, temp_folder_path : str) -> BufferedReader:
    """
    Takes an image and converts it into a binary array.

    Args:
        img_path (str): The image's path.
        temp_folder_path (str): Where to store the temporary BNW file.
        
    Returns:
        BufferedReader: The image's binary array.
    """
    temp_image_name = str(uuid4())
    bnw_image = Image.open(img_path).convert('1')
    bnw_image_path = temp_folder_path + '/' + temp_image_name + '.jpg'
    bnw_image.save(bnw_image_path)
    with open(bnw_image_path, 'rb') as file:
        temp_image = file.read()

    return temp_image

def binary_to_image(image_array) -> str:
    """
    Args:
        image_array: An image's binary array.
    Returns:
        str: The resulting image's file path.
    """
    temp_image = tempfile.NamedTemporaryFile(suffix='.jpg', delete=False)
    print(temp_image.name)
    with open(temp_image.name, 'wb') as file:
        file.write(image_array[0])
    return temp_image
