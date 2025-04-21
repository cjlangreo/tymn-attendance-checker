from tkinter import *
import lib.img_manip as img_manip
import lib.db_interface as db_interface
import tempfile



def main():
    with tempfile.TemporaryDirectory(dir='.') as temp_path:
        print(f'Temporary directory created at ./{temp_path}')
        
        res = img_manip.image_to_binary('../image_source/chanz.jpg', temp_path)
        print(res)
        root = Tk()
        root.mainloop()
        
        
        
if __name__ == '__main__':
    main()
    