import os, sys
import customtkinter as ctk
from tkinter import *
from tkinter import ttk
import datetime as dt
import threading
import tkinter as tk
from components import palette
from PIL import ImageTk
from lib.main_recognition import start_face_recognition, Student

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(parent_dir)

from lib.db_interface import pull_from_db, Tables, RegStdsColumns, AttendanceColumns

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

def set_font_mono(size, weight):
  return ctk.CTkFont(family="Ubuntu Mono", size=size, weight=weight)

def display_log(main_frame):
  main = ctk.CTkFrame(master=main_frame, fg_color=main_frame.cget("fg_color"), corner_radius=0)
  main.propagate(False)
  main.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="c")

  # Header =======================================
  ctk.CTkLabel(
     master=main, 
     text="Attendance",
     font=set_font_mono(36, "bold"),
     text_color=palette.TEXT_1
    ).place(relx=0.875, rely=0.1, anchor="c")

  # Clock ========================================
  day = ctk.CTkLabel(master=main, text=f"{dt.datetime.now():%A}", font=set_font(24, "bold"))
  day.place(relx=0.875, rely=0.25, anchor="c")
  date = ctk.CTkLabel(master=main, text=f"{dt.datetime.now():%B %d, %Y}", font=set_font(24, "bold"))
  date.place(relx=0.875, rely=0.3, anchor="c")

  time = ctk.CTkLabel(master=main, font=set_font(32, "bold"))
  time.place(relx=0.875, rely=0.4, anchor="c")

  def clock():
    datetime = dt.datetime.now() 
    this_time = f"{datetime:%H:%M:%S}"
    time.configure(text=this_time)
    time.after(500, clock)

  clock()

  # Scan Button ================================
  scan_btn = ctk.CTkButton(
    master=main,
    text="Scan",
    font=set_font(20, "bold"),
    fg_color=palette.TONE_1,
    text_color=palette.TEXT_2,
    border_width=0,
    cursor="hand2",
    height=50,
    width=164,
    corner_radius=8,
    command=lambda : open_register_window(main_frame)
  )
  scan_btn.place(relx=0.875, rely=0.6, anchor="c")
  # Table =========================================
  table_frame = ctk.CTkFrame(
    master=main, 
    fg_color=palette.PRIMARY_2,
    corner_radius=8,
  )
  table_frame.place(relx=0, rely=0.5, relwidth=0.70, relheight=1, anchor="w")

  tree = ttk.Treeview(master=table_frame, columns=("Name", "Date", "Time"), show="headings")
  
  def relative_width(event):
    tree_width = tree.winfo_width()

    tree.column("Name", width=int(tree_width * 0.5), stretch=False, anchor="w")
    tree.column("Time", width=int(tree_width * 0.2), stretch=False, anchor="c")
    tree.column("Date", width=int(tree_width * 0.3), stretch=False, anchor="c")

  def block_header_drag(event):
    if tree.identify_region(event.x, event.y) == "separator":
        return "break"

  tree.heading("Name", text="Name", anchor="w")
  tree.heading("Time", text="Time", anchor="c")
  tree.heading("Date", text="Date", anchor="c")

  tree.bind("<Configure>", relative_width)
  tree.bind("<Button-1>", block_header_drag, add="+")

  style = ttk.Style()
  style.theme_use("clam")

  style.configure(
    "Treeview",
    background=palette.PRIMARY_2,
    foreground=palette.TEXT_1,
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
    background=palette.TONE_1,
    foreground=palette.TEXT_2
  )

  style.map(
    "Treeview",
    background=[("selected", palette.PRIMARY_2)],
    foreground=[("selected", palette.TEXT_1)]
  )

  style.map(
    "Treeview.Heading",
    background=[("active", palette.TONE_2)], 
    foreground=[("active", palette.TEXT_2)] 
  )

  scrollbar = ctk.CTkScrollbar(master=table_frame, orientation="vertical", command=tree.yview)
  tree.configure(yscrollcommand = scrollbar.set)
  scrollbar.place(anchor="e", relx=0.985, rely=0.525, relheight=0.9)

  tree.pack(
    side="top",
    expand=True,
    fill="y",
    pady=12,
    padx=12,
  )

  # Display Database
  def show_records():
    for row in tree.get_children():
      tree.delete(row)
    
    rows = pull_from_db(table=(Tables.REGISTERED_STUDENTS, Tables.ATTENDANCE), values=(RegStdsColumns.NAME, AttendanceColumns.DATE, AttendanceColumns.TIME))
    # print(rows)
    for row in rows:
      tree.insert("", "end", values=row)

  show_records()

