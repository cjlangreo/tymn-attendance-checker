import tkinter as tkinter
import threading
from PIL import ImageTk
import main_recognition

def face_recognition(image_label : tkinter.Label):
    process_this_frame = True
    
    while True:

        if process_this_frame:
            cv2_image = main_recognition.retrieve_frame()
            tk_image = ImageTk.PhotoImage(cv2_image)
            image_label.configure(image=tk_image)
            image_label.image = tk_image
            
        process_this_frame = not process_this_frame






class RegisterWindow:
    def __init__(self, master):
        self.recog_window = tkinter.Toplevel(master)
        self.recog_window.title = 'Register New Student'
        
        self.image_label = tkinter.Label(self.recog_window)
        self.image_label.pack()
        
        self.thread = threading.Thread(target=face_recognition, args=(self.image_label,))
        self.thread.start()

        self.recog_window.mainloop()

def open_register_window(master):
    register_window = RegisterWindow(master)


class MainWindow:
    def __init__(self, master : tkinter.Tk):
        master.title('Main Window')
        
        self.label = tkinter.Label(master, text='Test Label')
        self.label.pack()

        self.register_student_btn = tkinter.Button(master, text='Register New Student', command=open_register_window(self))
        self.register_student_btn.pack()

        self.take_attendance_btn = tkinter.Button(master, text='Take Attendance')
        self.take_attendance_btn.pack()
        

def start_gui():
    root = tkinter.Tk()
    main_window = MainWindow(root)
    root.mainloop()
    

if __name__ == '__main__':
    start_gui()