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
sys.path.append(parent_dir)

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
# ============================================================

# Font Default
def set_font(size, weight):
  return ctk.CTkFont(family="Ubuntu", size=size, weight=weight)

def display_log(main_frame):
  main = ctk.CTkFrame(master=main_frame, fg_color=main_frame.cget("fg_color"))
  main.propagate(False)
  main.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="c")


  date = ctk.CTkLabel(master=main, text=f"{dt.datetime.now():%A, %B %d, %Y}", font=set_font(24, "bold"))
  date.place(relx=1, rely=0.1, anchor="e")

  time = ctk.CTkLabel(master=main, font=set_font(48, "bold"))
  time.place(relx=0.965, rely=0.18, anchor="e")

  def clock():
    datetime = dt.datetime.now() 
    this_time = f"{datetime:%H:%M:%S}"
    time.configure(text=this_time)
    time.after(500, clock)

  clock()

  table_frame = ctk.CTkFrame(
    master=main, 
    fg_color="#2a2a2a",
    corner_radius=16,
  )
  table_frame.place(relx=0.33, rely=0.5, relwidth=0.67, relheight=0.95, anchor="c")

  tree = ttk.Treeview(master=table_frame, columns=("Name", "Date", "Time"), show="headings")
  
  def relative_width(event):
    tree_width = tree.winfo_width()

    tree.column("Name", width=int(tree_width * 0.4))
    tree.column("Time", width=int(tree_width * 0.3))
    tree.column("Date", width=int(tree_width * 0.3))

  tree.heading("Name", text="Name")
  tree.heading("Time", text="Time")
  tree.heading("Date", text="Date")

  tree.bind("<Configure>", relative_width)

  style = ttk.Style()
  style.theme_use("default")

  style.configure(
    "Treeview",
    background="#2a2a2a",
    foreground="#adadad",
    fieldbackground="transparent",
    font=("Ubuntu Mono", 14, "normal"),
    rowheight=50,
    borderwidth=0,
  )

  style.configure(
    "Treeview.Heading",
    font=("Ubuntu", 16, "bold"),
    relief="flat",
    borderwidth=0,
    height=50,
    background="#1a1a1a",
    foreground="#d8d8d8"
  )

  tree.pack(
    side="top",
    expand=True,
    fill="y",
    pady=20,
  )

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

  # Display Database
  # def show_records():
  #   for row in tree.get_children():
  #     tree.delete(row)
    
  #   rows = pull_from_db()
  #   # print(rows)
  #   for row in rows:
  #     tree.insert("", "end", values=row)

  # show_records()

