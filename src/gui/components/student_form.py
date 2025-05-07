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

class PersonalInfoFrame(ctk.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, fg_color="#2a2a2a", corner_radius=16, **kwargs)
    self.propagate(False)

    ctk.CTkLabel(master=self, text="Personal Information", font=set_font(32, "bold"), text_color="#d8d8d8").place(relx=0.05, rely=0.085)

    self.name_entry = ctk.CTkEntry(
      master=self,
      font=set_font_mono(19, "normal"),
      placeholder_text="Full Name (Last, First M.I.)",
      fg_color="#3b3b3b",
      text_color="#adadad",
      corner_radius=10,
      border_width=0
    )
    self.name_entry.place(relx=0.5, rely=0.6, relwidth=0.9, relheight=0.35, anchor="c")

  def get_data(self):
    return self.name_entry.get()

class CourseFrame(ctk.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, fg_color="transparent", **kwargs)
    self.propagate(False)

    self.button_grid = ctk.CTkFrame(master=self,fg_color="transparent")
    self.button_grid.place(relx=0.5, rely=0.2, relheight=0.7, relwidth=0.95, anchor="n")

    self.course_var = tk.StringVar(master=self.button_grid)

    self.course_label = ctk.CTkLabel(master=self, text="Course", font=set_font(20, "bold"), fg_color="transparent", text_color="#d8d8d8")
    self.course_label.pack(anchor="w")

    self.courses = [Courses.BSA, Courses.BSBA, Courses.BSCE, Courses.BSCS, Courses.BSEE, Courses.BSHM, Courses.BSIT, Courses.BSME, Courses.BSOA]
    
    self.course_btns = []
    self.create_course_buttons()

  def create_course_buttons(self):
    for index, course in enumerate(self.courses):
        row = index // 3
        col = index % 3

        btn = ctk.CTkRadioButton(
            master=self.button_grid,
            text=course,
            variable=self.course_var,
            value=course,
            font=set_font(20, "normal"),
            border_color="#adadad",
            text_color="#adadad",
            hover_color="orange",
            cursor="hand2"
        )
        btn.grid(row=row, column=col, padx=[0, 120], pady=5)
        self.course_btns.append(btn)
  def get_data(self):
      return self.course_var.get().strip()

class StudentIDFrame(ctk.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, fg_color="transparent", **kwargs)

    self.stid_label = ctk.CTkLabel(master=self, text="Student ID:", font=set_font(20, "bold"), text_color="#d8d8d8")
    self.stid_label.place(relx=0, rely=0.5, anchor="w")
    self.stid_entry = ctk.CTkEntry(
      master=self, 
      font=set_font_mono(19, "normal"),
      placeholder_text="####",
      fg_color="#3b3b3b",
      text_color="#adadad",
      border_width=0
    )
    self.stid_entry.place(relx=0.4, rely=0.5, relwidth=0.3, relheight=0.9, anchor="w")
  
  def get_data(self):
    return self.stid_entry.get()

class YearFrame(ctk.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, fg_color="transparent",**kwargs)

    self.year_var = tk.StringVar(master=self)
    self.year_label = ctk.CTkLabel(master=self, text="Year", font=set_font(20, "bold"), fg_color="transparent", text_color="#d8d8d8")
    self.year_label.pack(anchor="w")

    self.year_btns = []
    self.create_year_buttons()
  
  def create_year_buttons(self):
    for year in ["1", "2", "3", "4"]:
      btn = ctk.CTkRadioButton(
        master=self,
        text=year,
        variable=self.year_var,
        value=year,
        font=set_font(20, "normal"),
        border_color="#adadad",
        text_color="#adadad",
        hover_color="orange",
        cursor="hand2"
      )
      btn.pack(side="left", padx=[20, 0])
      self.year_btns.append(btn)
  
  def get_data(self):
    return self.year_var.get().strip()

class FaceDataFrame(ctk.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, fg_color="#2a2a2a", corner_radius=16, **kwargs)
    self.propagate(False)

    self.frame_label = ctk.CTkLabel(master=self, text="Facial Data", font=set_font(32, "bold"), text_color="#d8d8d8").place(relx=0.05, rely=0.085)
    self.face_registered_indicator = ctk.CTkLabel(master=self, text="", font=set_font(24, "normal"), text_color="green")
    self.face_registered_indicator.place(relx=0.9, rely=0.375, anchor="e")
    student.label_indicator = self.face_registered_indicator

    self.camera_btn = ctk.CTkButton(
      master=self,
      text="Register Face",
      font=set_font(28, "bold"),
      border_width=2,
      corner_radius=12,
      fg_color="transparent",
      border_color="#474747",
      command=lambda: open_register_window(self)
    )
    self.camera_btn.place(relx=0.5, rely=0.65, relwidth=0.8, relheight=0.35, anchor="c")
    student.register_button = self.camera_btn

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
  Minimize below methods to proceed to widgets
  Method to save entries to database
  """
  def event_listener(event, index):
     widgets = [persinfo.name_entry, stid.stid_entry, course_frame.course_btns, year_frame.year_btns]
     match index:
        case 0|1:
           widgets[index].configure(border_width=0)
        case 2|3:
           for btn in widgets[index]:
              btn.configure(border_color="#adadad")

  def add_student():
    # Populat the student object with the entries ======================
    global student
    student.id = stid.get_data()
    student.name = persinfo.get_data()
    student.course = course_frame.get_data()
    student.year = year_frame.get_data()

    # Validation Checker
    # Reset previous invalid entries back to their OG form first
    # reset_validation()
    #Checks for any invalid or empty entries
    if not student.id or not student.name or not student.course or not student.year or student.temp_frame is None:
      if not student.name:
         persinfo.name_entry.configure(border_width=2, border_color="red")
      if not student.id:
        stid.stid_entry.configure(border_width=2,  border_color="red")
      if not student.course:
        for btn in course_frame.course_btns:
            btn.configure(
              border_color="red"
            )
      if not student.year:
        for btn in year_frame.year_btns:
            btn.configure(
              border_color="red"
            )
      if student.temp_frame is None:
        facedata_frame.camera_btn.configure(border_width=2,  border_color="red")

      return

    print("Student ID: ", student.id)
    print("Student Name: ", student.name)
    print("Student Course: ", student.course)
    print("Student Year: ", student.year)
    print("Student Image: ", student.temp_frame)

    student.submit_student(Tables.REGISTERED_STUDENTS)
  
    persinfo.name_entry.delete(0, "end")
    stid.stid_entry.delete(0, "end")
    course_frame.course_var.set(0)
    year_frame.year_var.set(0)
    student = Student() # We reinstantiate the student object to clear the previous entries.
    student.label_indicator = facedata_frame.face_registered_indicator # We reassign the label indicator to the new student object.
    facedata_frame.face_registered_indicator.configure(text="") # We clear the label indicator text.

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
  persinfo = PersonalInfoFrame(master=main)
  persinfo.place(relx=0.055, rely=0.065, relheight=0.3, relwidth=0.45, anchor="nw")

  persinfo.name_entry.bind("<KeyPress>", lambda event: event_listener(event, 0))
     
  # Wrapper
  # 414x230

# Face Registration =========================================
  facedata_frame = FaceDataFrame(master=main)
  facedata_frame.place(relx=0.95, rely=0.065, relheight=0.3, relwidth=0.425, anchor="ne")

# STUDENT INFO WRAPPER =================== 
  studinf_frame = ctk.CTkFrame(master=main, fg_color="#2a2a2a", corner_radius=16)
  studinf_frame.place(relx=0.055, rely=0.39, relheight=0.475, relwidth=0.895)
  studinf_frame.propagate(False)

  ctk.CTkLabel(master=studinf_frame, text="Academic Information", font=set_font(36, "bold"), text_color="#d8d8d8").place(relx=0.025, rely=0.055)
  

# Student ID
  stid = StudentIDFrame(master=studinf_frame)

  stid.place(relx=0.035, rely=0.2, relwidth=0.3, relheight=0.1)
  stid.stid_entry.bind("<KeyPress>", lambda event: event_listener(event, 1))

# Course 
  course_frame = CourseFrame(master=studinf_frame)
  course_frame.place(relx=0.035, rely=0.35, relheight=0.4, relwidth=0.8)

  for btn in course_frame.course_btns:
     btn.bind("<Button-1>", lambda event: event_listener(event, 2))

# Year
  year_frame = YearFrame(master=studinf_frame)
  year_frame.place(relx=0.035, rely=0.75, relheight=0.2, relwidth=0.8)

  for btn in year_frame.year_btns:
     btn.bind("<Button-1>", lambda event: event_listener(event, 3))

# Submit
  submit_data = ctk.CTkButton(
    master=main,
    text="Submit",
    font=set_font(20, "bold"),
    fg_color="transparent",
    text_color="#d8d8d8",
    border_width=2,
    border_color="#474747",
    cursor="hand2",
    height=50,
    corner_radius=10,
    command=add_student
  )
  submit_data.place(relx=0.5, rely=0.925, anchor="center")

