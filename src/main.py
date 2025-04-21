from lib import img_manip, main_recognition, db_interface
import tkinter
import tempfile
from PIL import Image, ImageTk

class MyGUI:
    def __init__(self):
        self.root = tkinter.Tk()
        self.root.mainloop()


def main():
    with tempfile.TemporaryDirectory(dir='.') as temp_path: # Main loop should be inside this context.
        print(f'Temporary directory created at ./{temp_path}') # To mainly store converted images which are then deleted on system exit.
        MyGUI()
        
 
if __name__ == '__main__':
    main()
    