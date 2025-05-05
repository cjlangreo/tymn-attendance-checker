import os, sys
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from PIL import ImageTk
import threading

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(parent_dir)

from lib.main_recognition import start_face_recognition, Student
from lib.db_interface import Courses, Tables

student = Student()

# Font Default
def set_font(size, weight):
  return ctk.CTkFont(family="Ubuntu", size=size, weight=weight)

def set_font_mono(size, weight):
  return ctk.CTkFont(family="Ubuntu Mono", size=size, weight=weight)

def update_label_image(dest_label : tk.Label, src_image):
    tk_image = ImageTk.PhotoImage(src_image)
    dest_label.configure(image=tk_image)
    dest_label.image = tk_image

def open_register_window(master):
    
    recog_window = tk.Toplevel(master)
    recog_window.title('Register New Student')
    recog_window.resizable(False, False)
    
    image_label = tk.Label(recog_window)
    image_label.pack()
    
    face_recog_thread = threading.Thread(target=start_face_recognition, args=(image_label, recog_window, 'r', student))
    face_recog_thread.start()

def display_form(main_frame):
  """
  Minimize below method to proceed to widgets
  Method to save entries to database
  """
  def reset_validation():
    for entry in [fname_entry, mi_entry, lname_entry, stid_entry]:
      entry.configure(border_width=0)
    for btns in [course_btns, year_btns]:
      for btn in btns:
        btn.configure(border_color="#adadad")
    cam_btn.configure(border_width=0)

  def add_student():
    # Populat the student object with the entries ======================
    global student
    student.id = stid_entry.get().strip()
    
    fname = fname_entry.get().strip()
    mi = mi_entry.get().strip()
    lname = lname_entry.get().strip()
    student.name = f"{lname}, {fname} {mi}."
    
    student.course = course_var.get().strip()
    student.year = year_var.get().strip()

    # Validation Checker
    # Reset previous invalid entries back to their OG form first
    reset_validation()
    #Checks for any invalid or empty entries
    if not student.id or not student.name or not student.course or not student.year or student.temp_frame is None:
      if mi and (len(mi) != 1 or not mi.isalpha()):
        mi_entry.configure(
          border_width=2,
          border_color="red"
        )
        print("Single letter or blank only")
      if not fname:
        fname_entry.configure(border_width=2,  border_color="red")
      if not lname:
        lname_entry.configure(border_width=2,  border_color="red")
      if not student.id:
        stid_entry.configure(border_width=2,  border_color="red")
      if not student.course:
        for btn in course_btns:
            btn.configure(
              border_color="red"
            )
      if not student.year:
        for btn in year_btns:
            btn.configure(
              border_color="red"
            )
      if student.temp_frame is None:
        cam_btn.configure(border_width=2,  border_color="red")

      return

    print("Student ID: ", student.id)
    print("Student Name: ", student.name)
    print("Student Course: ", student.course)
    print("Student Year: ", student.year)
    print("Student Image: ", student.temp_frame)

    student.submit_student(Tables.REGISTERED_STUDENTS)
  
    lname_entry.delete(0, "end")
    fname_entry.delete(0, "end")
    mi_entry.delete(0, "end")
    stid_entry.delete(0, "end")
    course_var.set(0)
    year_var.set(0)
    student = Student() # We reinstantiate the student object to clear the previous entries.
    student.label_indicator = face_registered_indicator # We reassign the label indicator to the new student object.
    face_registered_indicator.configure(text="") # We clear the label indicator text.

  """
  Widgets Starts Here:
  In order:
  1.  main and label: root container for this tab
  2.  -persinf_frame and label: container for name entries
  3.  ---name_entries and label: lname_entry, fname_entry, mi_entry

  4.  -acadinf_frame and label: container for academic info entries
  5.  ---stud_id_entry and label: label for student id
  6.  ---course_frame and label: container frame for course radio buttons
  7.  ------course_btn and label: courses buttons
  8.  ---year_frame and label: container frame for year radio buttons
  9.  ------year_btn and label: years buttons
  
  10. -fdata_frame and label: container for face registration
  11. ---face_registration btn: button to register face data

  12. -submit btn: button to store all valid entries to database 

  main resolution: 922x768
  """
  main = ctk.CTkFrame(master=main_frame, fg_color="transparent")
  main.propagate(False)
  main.place(relwidth=1.0, relheight=1.0, x=0, y=0)


  # ====== CSS =========
  style = ttk.Style()
  style.theme_use("clam")
  # == CSS ENDS HERE ===

# Name =====================================
  
  # Wrapper
  # 414x230
  persinf_frame = ctk.CTkFrame(master=main, fg_color="#2a2a2a", corner_radius=16)
  persinf_frame.place(relx=0.055, rely=0.065, relheight=0.3, relwidth=0.45, anchor="nw")
  persinf_frame.propagate(False)

  ctk.CTkLabel(master=persinf_frame, text="Personal Information", font=set_font(32, "bold"), text_color="#d8d8d8").place(relx=0.05, rely=0.085)
  
  fname_entry = ctk.CTkEntry(
    master=persinf_frame,  
    font=set_font_mono(18, "normal"),
    placeholder_text="First Name",
    fg_color="#3b3b3b",
    text_color="#adadad",
    corner_radius=10,
    border_width=0
  )
  fname_entry.place(relx=0.075, rely=0.325, relwidth=0.5, relheight=0.25)

  mi_entry = ctk.CTkEntry(
    master=persinf_frame, 
    font=set_font_mono(18, "normal"),
    placeholder_text="M.I.",
    fg_color="#3b3b3b",
    text_color="#adadad",
    corner_radius=10,
    border_width=0
  )
  mi_entry.place(relx=0.625, rely=0.325, relwidth=0.2, relheight=0.25)

  lname_entry = ctk.CTkEntry(
    master=persinf_frame, 
    font=set_font_mono(19, "normal"),
    placeholder_text="Last Name",
    fg_color="#3b3b3b",
    text_color="#adadad",
    corner_radius=10,
    border_width=0
  )
  lname_entry.place(relx=0.075, rely=0.65, relwidth=0.75, relheight=0.25)

# Face Registration =========================================

  # Wrapper
  # 392x230
  facedata_frame = ctk.CTkFrame(master=main, fg_color="#2a2a2a", corner_radius=16)
  facedata_frame.place(relx=0.95, rely=0.065, relheight=0.3, relwidth=0.425, anchor="ne")
  facedata_frame.propagate(False)

  ctk.CTkLabel(master=facedata_frame, text="Facial Data", font=set_font(32, "bold"), text_color="#d8d8d8").place(relx=0.05, rely=0.085)
  
  face_registered_indicator = ctk.CTkLabel(master=facedata_frame, text="", font=set_font(20, "normal"), text_color="green")
  face_registered_indicator.place(relx=0.2, rely=0.35)
  student.label_indicator = face_registered_indicator

  # CAMERA HERE
  cam_btn = ctk.CTkButton(
    master=facedata_frame,
    text="Register Face",
    font=set_font(28, "bold"),
    border_width=2,
    corner_radius=12,
    fg_color="transparent",
    border_color="#474747",
    command=lambda: open_register_window(facedata_frame)
  )
  cam_btn.place(relx=0.5, rely=0.65, relwidth=0.8, relheight=0.35, anchor="c")

# Student ID ==============================

  # Wrapper
  # 825x365
  studinf_frame = ctk.CTkFrame(master=main, fg_color="#2a2a2a", corner_radius=16)
  studinf_frame.place(relx=0.055, rely=0.39, relheight=0.475, relwidth=0.895)
  studinf_frame.propagate(False)

  ctk.CTkLabel(master=studinf_frame, text="Academic Information", font=set_font(36, "bold"), text_color="#d8d8d8").place(relx=0.025, rely=0.055)

  ctk.CTkLabel(master=studinf_frame, text="Student ID:", font=set_font(20, "bold"), text_color="#d8d8d8").place(relx=0.035, rely=0.2125)  
  
  stid_entry = ctk.CTkEntry(
    master=studinf_frame, 
    font=set_font_mono(19, "normal"),
    placeholder_text="####",
    fg_color="#3b3b3b",
    text_color="#adadad",
    border_width=0
  )
  stid_entry.place(relx=0.16, rely=0.2, relwidth=0.1, relheight=0.1)

# Course ============================================

  # Wrapper
  course_frame = ctk.CTkFrame(master=studinf_frame, fg_color="transparent")
  course_frame.place(relx=0.035, rely=0.35, relheight=0.4, relwidth=0.8 )
  course_frame.propagate(False)

  button_grid = ctk.CTkFrame(master=course_frame, fg_color="transparent")
  button_grid.place(relx=0.5, rely=0.2, relheight=0.7, relwidth=0.95, anchor="n")

  # Variable to store
  course_var = tk.StringVar(master=button_grid)

  course_label = ctk.CTkLabel(master=course_frame, text="Course", font=set_font(20, "bold"), fg_color="transparent", text_color="#d8d8d8")
  course_label.pack(anchor="w")

  # OPTIONS FOR COURSES
  courses = [ Courses.BSA, Courses.BSBA, Courses.BSCE, Courses.BSCS, Courses.BSEE, Courses.BSHM, Courses.BSIT, Courses.BSME, Courses.BSOA ]

  course_btns = []
  for index, course in enumerate(courses):
    row = index // 3
    col = index % 3

    btn = ctk.CTkRadioButton(
      master=button_grid,
      text=course,
      variable=course_var,
      value=course,
      font=set_font(20, "normal"),
      border_color="#adadad",
      text_color="#adadad",
      hover_color="orange",
      cursor="hand2"
    )
    btn.grid(row=row, column=col, padx=[0, 120], pady=5)
    course_btns.append(btn)

# Year =================================================

  # Wrapper
  year_frame = ctk.CTkFrame(master=studinf_frame, fg_color="transparent")
  year_frame.place(relx=0.035, rely=0.75, relheight=0.2, relwidth=0.8)

  # Variable to store
  year_var = tk.StringVar(master=year_frame)

  # Label
  year_label = ctk.CTkLabel(master=year_frame, text="Year", font=set_font(20, "bold"), fg_color="transparent", text_color="#d8d8d8")
  year_label.pack(anchor="w")

  # OPTIONS FOR YEARS
  year_btns = []
  for year in ["1", "2", "3", "4"]:
    btn = ctk.CTkRadioButton(
      master=year_frame,
      text=year,
      variable=year_var,
      value=year,
      font=set_font(20, "normal"),
      border_color="#adadad",
      text_color="#adadad",
      hover_color="orange",
      cursor="hand2"
    )
    btn.pack(side="left", padx=[20, 0])
    year_btns.append(btn)

# Submit ===========================================

  submit_data = ctk.CTkButton(
    master=main,
    text="Submit",
    font=set_font(20, "bold"),
    fg_color="#E36A00",
    text_color="#d8d8d8",
    border_width=0,
    cursor="hand2",
    height=50,
    corner_radius=25,
    command=add_student
  )
  submit_data.place(relx=0.5, rely=0.925, anchor="center")
  

  # return registered_face
