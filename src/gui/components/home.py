import os, sys
import customtkinter as ctk
from tkinter import *
from tkinter import ttk
import datetime as dt
import threading
import tkinter as tk
from PIL import ImageTk
from lib.main_recognition import start_face_recognition, Student

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))


# Face Recognition =======================
student = Student()

def update_label_image(dest_label : tk.Label, src_image):
    tk_image = ImageTk.PhotoImage(src_image)
    dest_label.configure(image=tk_image)
    dest_label.image = tk_image

def open_register_window(master):
    recog_window = tk.Toplevel(master)
    recog_window.title('Taking Attendance')
    recog_window.resizable(False, False)
    
    image_label = tk.Label(recog_window)
    image_label.pack()
    
    face_recog_thread = threading.Thread(target=start_face_recognition, args=(image_label, recog_window, 'a', student))
    face_recog_thread.start()

def set_font(size, weight):
  return ctk.CTkFont(family="Ubuntu", size=size, weight=weight)   

def display_log(main_frame):
  main = ctk.CTkFrame(master=main_frame, fg_color=main_frame.cget("fg_color"))
  main.propagate(False)
  main.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="c")

  scan_btn = ctk.CTkButton(
    master=main,
    text="Scan",
    font=set_font(28, "bold"),
    fg_color="transparent",
    text_color="#d8d8d8",
    border_width=2,
    border_color="#474747",
    cursor="hand2",
    height=75,
    width=256,
    corner_radius=16,
    command=lambda : open_register_window(main_frame)
  )
  scan_btn.place(relx=1, rely=0.35, anchor="e")