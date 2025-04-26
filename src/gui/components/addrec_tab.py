import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
import subprocess
import threading
from fakedb import connect_db


# Font Default
def set_font(size, weight):
  return tkFont.Font(family="Ubuntu", size=size, weight=weight)

def open_cam():
  threading.Thread(
    target=lambda: subprocess.run(["python3", "imong_script.py"]) # <================================================== [0<>0]
  )


def addrec_tab(main_frame):

  def add_student():
    name = name_entry.get().strip()
    course = course_var.get().strip()
    year = year_var.get().strip()

    if not name or not course or not year:
        print("Whoopsie! You missed a spot.")
        return

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute(
      """
      INSERT INTO registered_students (name, face_encodings, course, year)
      VALUES (?, ?, ?, ?)
    """, (name, None, course, int(year))
    )
    conn.commit()
    conn.close()

    name_entry.delete(0, tk.END)
    course_var.set(0)
    year_var.set(0)


  addrec_frame = tk.Frame(main_frame, width=900, height=800, bg=main_frame["bg"])
  addrec_frame.propagate(False)
  addrec_frame.pack(padx=40, pady=40)

  tk.Label(addrec_frame, text="Add Student Record", font=set_font(40, "bold"), bg=addrec_frame["bg"], fg="#d8d8d8").place(x=0, y=0)
  
  addrec_frame.radio_off = tk.PhotoImage(file="src/gui/assets/radio_button_unchecked.png", master=main_frame)
  addrec_frame.radio_on = tk.PhotoImage(file="src/gui/assets/radio_button_checked.png", master=main_frame)

  radio_off = addrec_frame.radio_off
  radio_on = addrec_frame.radio_on

  year_var = tk.StringVar(addrec_frame)

  # Name
  tk.Label(addrec_frame, text="Full Name", font=set_font(20, "normal"), bg="#222", fg="#d8d8d8").place(x=0, y=80)
  tk.Label(addrec_frame, text="( Last Name,   First Name,   M.I. )", font=set_font(16, "normal"), bg="#222", fg="#5b5b5b").place(x=125, y=85)

  entry_style = ttk.Style()
  entry_style.theme_use("clam")

  entry_style.configure(
    "Custom.TEntry",
    relief="flat",
    foreground="#adadad",
    fieldbackground="#222",
    background="#222",
    padding=10,
    insertcolor="#E36A00",
    insertwidth=2,
    cursor="hand2"
  )
  name_entry = ttk.Entry(addrec_frame, style="Custom.TEntry", font=set_font(20, "normal"))
  name_entry.place(x=0, y=120, width=550, height=60)

  # Course
  course_frame = tk.Frame(addrec_frame, bg="#222", width=900, height=800)
  course_frame.place(x=0, y=210)
  tk.Label(course_frame, text="Course", font=set_font(20, "bold"), bg="#222", fg="#d8d8d8").pack(anchor="w", pady=(0, 10))
 
  course_var = tk.StringVar(course_frame)

  courses = [
    ("Computer Science", "BSCS"),
    ("Information Technology", "BSIT"),
    ("Computer Engineering", "BSCPE")
  ]

  radio_btns = []

  def selected_course(*args):
    for btn in radio_btns:
      if course_var.get() ==btn["value"]:
        btn.config(fg="#E36A00")
      else:
        btn.config(fg="#adadad")
  course_var.trace_add("write", selected_course)

  for label, value in courses:
    btn = tk.Radiobutton(
      course_frame,
      text=label,
      image=radio_off,
      selectimage=radio_on,
      variable=course_var,
      value=value,
      font=set_font(20, "normal"),
      fg="#adadad",
      bg="#222",
      activeforeground="#faa152",
      activebackground="#222",
      selectcolor="#222",
      padx=30,
      pady=10,
      bd=0,
      highlightthickness=0,
      indicatoron=False,
      justify="left",
      compound="left",
      cursor="hand2"
    )
    btn.pack(anchor="w", padx=20)
    radio_btns.append(btn)


  # Year
  year_frame = tk.Frame(addrec_frame, bg="#222", width=900, height=800)
  year_frame.place(x=0, y=420)

  tk.Label(year_frame, text="Year", font=set_font(20, "bold"), bg="#222", fg="#d8d8d8").pack(anchor="w", pady=(0, 10))
  for year in ["1", "2", "3", "4"]:
    tk.Radiobutton(
      year_frame,
      text=year,
      variable=year_var,
      value=year,
      image=radio_off,
      selectimage=radio_on,
      font=set_font(20, "normal"),
      fg="#adadad",
      bg="#222",
      activeforeground="#faa152",
      activebackground="#222",
      selectcolor="#222",
      padx=10,
      pady=10,
      bd=0,
      highlightthickness=0,
      indicatoron=False,
      justify="left",
      compound="left",
      cursor="hand2"
    ).pack(side="left", padx=40)

  # Camera
  cam_btn = tk.Button(
    addrec_frame,
    text="Register Face",
    font=set_font(20, "bold"),
    bd=0,
    background="#222",
    foreground="#d8d8d8",
    activeforeground="#d8d8d8",
    activebackground="#E36A00",
    highlightbackground="#d8d8d8",
    cursor="hand2",
    command=open_cam
  )
  cam_btn.place(x=0, y=550)

  # Image Upload (TEST ONLY)
  

  # Submit
  submit_data = tk.Button(
    addrec_frame,
    text="Submit",
    font=set_font(16, "bold"),
    background="#E36A00",
    foreground="#d8d8d8",
    highlightthickness=0,
    relief="flat",
    padx=50,
    pady=10,
    cursor="hand2",
    command=add_student
  )
  submit_data.place(relx=0.5, y=650, anchor="center")