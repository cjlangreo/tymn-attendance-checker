import os, sys
import tkinter as tk
import customtkinter as ctk
from tkinter import ttk
from PIL import ImageTk
import threading
from components import palette
from components import assets

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(parent_dir)

from lib.main_recognition import start_face_recognition, Student
from lib.db_interface import Courses, Tables

student = Student()

class NameFrame(ctk.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, fg_color="transparent", corner_radius=0, **kwargs)

    ctk.CTkLabel(master=self, text=" Name", font=set_font(24, "bold"), text_color=palette.TEXT_1, image=assets.name, compound="left",).pack(anchor="w", pady=(0, 12),)

    self.name_entry = ctk.CTkEntry(
      master=self,
      font=set_font_mono(19, "normal"),
      placeholder_text="Dela Cruz, Juan A.",
      fg_color=palette.PRIMARY_3,
      text_color=palette.TEXT_1,
      corner_radius=4,
      border_width=0,
      height=56,
    )
    self.name_entry.pack(anchor="w", fill="x")

  def get_data(self):
    return self.name_entry.get()

class StudentIDFrame(ctk.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, fg_color="transparent", border_color=palette.PRIMARY_4, **kwargs)

    self.stid_label = ctk.CTkLabel(master=self, text=" Student ID", font=set_font(24, "bold"), text_color=palette.TEXT_1, image=assets.id, compound="left",)
    self.stid_label.pack(anchor="w", pady=(0, 12))
    self.stid_entry = ctk.CTkEntry(
      master=self, 
      font=set_font_mono(19, "normal"),
      placeholder_text="####",
      fg_color=palette.PRIMARY_3,
      text_color=palette.TEXT_1,
      border_width=0,
      corner_radius=4,
      height=50, 
    )
    self.stid_entry.pack(anchor="w", fill="x")
  
  def get_data(self):
    return self.stid_entry.get()

class CourseFrame(ctk.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, fg_color="transparent", border_color=palette.PRIMARY_4, **kwargs)

    self.course_var = tk.StringVar(value=Courses.BSA)

    self.course_label = ctk.CTkLabel(master=self, text=" Course", font=set_font(24, "bold"), fg_color="transparent", text_color=palette.TEXT_1, image=assets.course, compound="left",)
    self.course_label.pack(anchor="w", pady=(0,12))

    self.courses = [Courses.BSA, Courses.BSBA, Courses.BSCE, Courses.BSCS, Courses.BSEE, Courses.BSHM, Courses.BSIT, Courses.BSME, Courses.BSOA]

    self.options = ctk.CTkOptionMenu(
      master=self, 
      values=self.courses,
      variable=self.course_var,
      fg_color=palette.PRIMARY_4,
      button_color=palette.PRIMARY_3,
      dropdown_fg_color=palette.PRIMARY_4,
      dropdown_text_color=palette.TEXT_1,
      dropdown_hover_color=palette.TONE_1,
      font=set_font(16, "bold"),
      dropdown_font=set_font(18, "normal"),
      corner_radius=8,
      height=50
    )
    self.options.pack(anchor="w", fill="x")

  def get_data(self):
      return self.course_var.get().strip()

class YearFrame(ctk.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, fg_color="transparent", border_color=palette.PRIMARY_4, **kwargs)

    self.year_var = tk.StringVar(value="1")
    self.year_label = ctk.CTkLabel(master=self, text=" Year", font=set_font(24, "bold"), fg_color="transparent", text_color=palette.TEXT_1, image=assets.year, compound="left",)
    self.year_label.pack(anchor="w", pady=(0, 12))

    self.options = ctk.CTkOptionMenu(
      master=self, 
      values=["1", "2", "3", "4"],
      variable=self.year_var,
      fg_color=palette.PRIMARY_4,
      button_color=palette.PRIMARY_3,
      dropdown_fg_color=palette.PRIMARY_4,
      dropdown_text_color=palette.TEXT_1,
      dropdown_hover_color=palette.TONE_1,
      font=set_font(16, "bold"),
      dropdown_font=set_font(18, "normal"),
      corner_radius=8,
      height=50
    )
    self.options.pack(anchor="w", fill="x")

  def get_data(self):
    return self.year_var.get().strip()

class FaceDataFrame(ctk.CTkFrame):
  def __init__(self, master, **kwargs):
    super().__init__(master, fg_color=palette.PRIMARY_2, **kwargs)

    self.frame_label = ctk.CTkLabel(master=self, text=" Facial Data", font=set_font(24, "bold"), text_color=palette.TEXT_1, image=assets.fingerprint, compound="left",).pack(anchor="w", pady=(0, 12))

    self.camera_btn = ctk.CTkButton(
      master=self,
      text="Register Face",
      font=set_font(20, "bold"),
      border_width=2,
      width=256,
      height=56,
      corner_radius=12,
      border_color=palette.PRIMARY_3,
      text_color=palette.TEXT_1,
      fg_color=palette.PRIMARY_2,
      command=lambda: open_register_window(self)
    )
    self.camera_btn.pack(anchor="w")
    student.register_button = self.camera_btn
    student.label_indicator = self.camera_btn

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
     widgets = [nameinfo.name_entry, stid.stid_entry]
     match index:
        case 0|1:
           widgets[index].configure(border_width=0)

  def add_student():
    # Populat the student object with the entries ======================
    global student
    student.id = stid.get_data()
    student.name = nameinfo.get_data()
    student.course = course_frame.get_data()
    student.year = year_frame.get_data()

    # Validation Checker
    # Reset previous invalid entries back to their OG form first
    # reset_validation()
    #Checks for any invalid or empty entries
    if not student.id or not student.name or not student.course or not student.year or student.temp_frame is None:
      if not student.name:
         nameinfo.name_entry.configure(border_width=2, border_color="red")
      if not student.id:
        stid.stid_entry.configure(border_width=2,  border_color="red")
      if student.temp_frame is None:
        facedata_frame.camera_btn.configure(border_width=2,  border_color="red")

      return

    print("Student ID: ", student.id)
    print("Student Name: ", student.name)
    print("Student Course: ", student.course)
    print("Student Year: ", student.year)
    print("Student Image: ", student.temp_frame)

    student.submit_student(Tables.REGISTERED_STUDENTS)
  
    nameinfo.name_entry.delete(0, "end")
    stid.stid_entry.delete(0, "end")
    course_frame.course_var.set(0)
    year_frame.year_var.set(0)
    student = Student() # We reinstantiate the student object to clear the previous entries.
    student.label_indicator = facedata_frame.camera_btn # We reassign the label indicator to the new student object.
    facedata_frame.camera_btn.configure(text="Register Face", text_color=palette.TEXT_1) # We clear the label indicator text.

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

  # ====== CSS =========
  style = ttk.Style()
  style.theme_use("clam")
  # == CSS ENDS HERE ===

  main = ctk.CTkFrame(master=main_frame, fg_color=main_frame.cget("fg_color"), corner_radius=0)
  main.propagate(False)
  main.place(relwidth=0.7, relheight=0.85, relx=0.5, rely=0.5, anchor="center")

  ctk.CTkLabel(master=main, text="Personal Information", font=set_font(32, "bold"), text_color=palette.TEXT_1).pack(anchor="w", pady=(0, 16))

  persinfo_wrapper = ctk.CTkFrame(master=main, fg_color=palette.PRIMARY_2, corner_radius=12)
  persinfo_wrapper.pack(fill="x")
# Name =====================================

  nameinfo = NameFrame(master=persinfo_wrapper)
  nameinfo.pack(fill="x", padx=24, pady=(24, 12))

  nameinfo.name_entry.bind("<KeyPress>", lambda event: event_listener(event, 0))
     
  # Wrapper
  # 414x230

# Face Registration =========================================
  facedata_frame = FaceDataFrame(master=persinfo_wrapper)
  facedata_frame.pack(fil="x", pady=(12, 24), padx=24)

# STUDENT INFO WRAPPER =================== 
  ctk.CTkLabel(master=main, text="Academic Information", font=set_font(32, "bold"), text_color=palette.TEXT_1).pack(anchor="w", pady=(48,16))

  studinf_frame = ctk.CTkFrame(master=main, fg_color=palette.PRIMARY_2, corner_radius=12)
  studinf_frame.pack(fill="x")
  studinf_frame.grid_columnconfigure(0, weight=1)
  studinf_frame.grid_columnconfigure(1, weight=1)
  studinf_frame.grid_columnconfigure(2, weight=1)


# Student ID
  stid = StudentIDFrame(master=studinf_frame)
  stid.grid(row=0, column=0, sticky="nsew", pady=24, padx=(24, 12))
  stid.stid_entry.bind("<KeyPress>", lambda event: event_listener(event, 1))

# Course 
  course_frame = CourseFrame(master=studinf_frame)
  course_frame.grid(row=0, column=1, sticky="nsew", pady=24, padx=12)

# Year
  year_frame = YearFrame(master=studinf_frame)
  year_frame.grid(row=0, column=2, sticky="nsew", pady=24, padx=(12, 24))

# Submit
  submit_data = ctk.CTkButton(
    master=main,
    text="Submit",
    font=set_font(24, "bold"),
    fg_color=palette.TONE_1,
    text_color=palette.TEXT_2,
    border_width=0,
    cursor="hand2",
    height=60,
    width=200,
    corner_radius=8,
    command=add_student
  )
  submit_data.place(relx=0.5, rely=1, anchor="s")

