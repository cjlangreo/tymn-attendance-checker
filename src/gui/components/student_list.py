import os, sys
import customtkinter as ctk
from tkinter import ttk

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(parent_dir)

from lib.db_interface import pull_from_db, Tables, RegStdsColumns, update_student, delete_student
from lib.img_manip import bytes_to_image
from components.student_form import PersonalInfoFrame, CourseFrame, StudentIDFrame, YearFrame, FaceDataFrame


# Font Default
def set_font(size, weight):
  return ctk.CTkFont(family="Ubuntu", size=size, weight=weight)

def display_list(main_frame):

  def relative_width(event):
    tree_width = tree.winfo_width()

    tree.column("ID", width=int(tree_width * 0.1), anchor="center")
    tree.column("Name", width=int(tree_width * 0.35))
    tree.column("Course", width=int(tree_width * 0.15))
    tree.column("Year", width=int(tree_width * 0.15))
    tree.column("Image", width=int(tree_width * 0.1))
    tree.column("", width=int(tree_width * 0.1))

  def data_onclick(event):
    item = tree.identify_row(event.y)
    column = tree.identify_column(event.x)
    
    # To view image 
    if column =="#5" and item:
      values = tree.item(item, "values")
      if values:
        student_id = int(values[0])
        img_data = img_array_map.get(student_id)
        if img_data:
          img_path = bytes_to_image(img_data, student_id)
          os.system(f"xdg-open '{img_path}'")
    
    # To edit data
    if column == "#6" and item:
      values = tree.item(item, "values")
      if values:

        # Toplevel
        edit_data = ctk.CTkToplevel(tree, fg_color="#222")
        edit_data.title("Edit Student Data")
        edit_data.geometry("800x800")
        edit_data.propagate(False)
        edit_data.resizable(False, False)

        # Student Info Wrapper
        studinf_wrapper = ctk.CTkFrame(master=edit_data, fg_color="#2a2a2a", corner_radius=16)
        studinf_wrapper.place(relx=0.055, rely=0.3, relheight=0.55, relwidth=0.895)
        studinf_wrapper.propagate(False)
        ctk.CTkLabel(master=studinf_wrapper, text="Academic Information", font=set_font(28, "bold"), text_color="#d8d8d8").place(relx=0.025, rely=0.055)

        # Student ID
        stid = StudentIDFrame(master=studinf_wrapper)
        stid.stid_label.configure(text="Stud. ID:")
        stid.place(relx=0.035, rely=0.2, relwidth=0.3, relheight=0.1)
        stid.stid_entry.insert(0, values[0])
        old_stdid = values[0]

        # Name
        persinfo = PersonalInfoFrame(master=edit_data)
        persinfo.place(relx=0.055, rely=0.065, relheight=0.2, relwidth=0.895, anchor="nw")
        persinfo.name_entry.insert(0, values[1])
  
        # Course
        course_frame = CourseFrame(master=studinf_wrapper)
        course_frame.place(relx=0.035, rely=0.35, relheight=0.4, relwidth=0.8)
        course_frame.course_var.set(values[2])

        # Year
        year_frame = YearFrame(master=studinf_wrapper)
        year_frame.place(relx=0.035, rely=0.75, relheight=0.2, relwidth=0.8)
        year_frame.year_var.set(values[3])

        def submit_button():
          update_student(old_stdid, ((RegStdsColumns.ID, stid.stid_entry.get()), (RegStdsColumns.NAME, persinfo.name_entry.get()), (RegStdsColumns.COURSE, course_frame.course_var.get()), (RegStdsColumns.YEAR, year_frame.year_var.get())))
          edit_data.destroy()

        def delete_button():
          delete_student(old_stdid)
          edit_data.destroy()

        # Save Button
        submit_btn = ctk.CTkButton(
          master=edit_data,
          text="Save",
          font=set_font(20, "bold"),
          fg_color="transparent",
          text_color="#d8d8d8",
          border_width=1,
          border_color="#474747",
          cursor="hand2",
          height=50,
          corner_radius=10,
          command = submit_button
        )
        submit_btn.place(relx=0.75, rely=0.885, anchor="ne")
        
        # Delete Button
        delete_btn = ctk.CTkButton(
          master=edit_data,
          text="Delete",
          font=set_font(20, "bold"),
          fg_color="#C70000",
          text_color="#d8d8d8",
          border_width=0,
          cursor="hand2",
          height=50,
          corner_radius=10,
          command = delete_button
        )
        delete_btn.place(relx=0.95, rely=0.885, anchor="ne")

  main = ctk.CTkFrame(master=main_frame, fg_color=main_frame.cget("fg_color"))
  main.propagate(False)
  main.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="c")

  # Table Frame (tree + scrollbar)
  table_frame = ctk.CTkFrame(
    master=main, 
    fg_color="#2a2a2a",
    corner_radius=16,
  )
  table_frame.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.92, anchor="c")

  # Treeview
  tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Course", "Year", "Image", ""), show="headings")
  tree.heading("ID", text="ID")
  tree.heading("Name", text="Name", anchor="w")
  tree.heading("Course", text="Course", anchor="w")
  tree.heading("Year", text="Year", anchor="w")
  tree.heading("Image", text="Image", anchor="w")
  tree.heading("", text="", anchor="w")

  tree.bind("<Configure>", relative_width)
  tree.bind("<Button-1>", data_onclick)

  # Scrollbar
  scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
  tree.configure(yscrollcommand = scrollbar.set)
  
  # Styling
  style = ttk.Style()
  style.theme_use("default")

  # Tree Rows and Columns Styling
  style.configure(
    "Treeview",
    background="#2a2a2a",
    foround="#adadad",
    fieldbackground="transparent",
    font=("Ubuntu Mono", 14, "normal"),
    rowheight=50,
    borderwidth=0,
  )
  
  style.map(
    "Treeview",
    background=[("selected", "#2a2a2a")],
    foreground=[("selected", "#adadad")]
  )

  # Tree Heading Styling
  style.configure(
    "Treeview.Heading",
    font=("Ubuntu", 16, "bold"),
    relief="flat",
    borderwidth=0,
    height=50,
    background="#1a1a1a",
    foreground="#d8d8d8"
  )

  style.map(
    "Treeview.Heading",
    background=[("active", "#1a1a1a")], 
    foreground=[("active", "#d8d8d8")] 
  )

  # Scrollbar Styling 
  style.configure(
    "Vertical.TScrollbar",
    relief="flat",
    background="#3b3b3b",
    arrowcolor=table_frame["bg"],
    borderwidth=0,
    troughcolor=table_frame["bg"]
  )

  style.map(
    "Vertical.TScrollbar",
    background=[("active", "#E36A00"), ("!active", "#3b3b3b")]
  )

  # Pack scrollbar and tree
  tree.pack(
    side="top",
    expand=True,
    fill="y",
    pady=20,
  )
  scrollbar.place(relx=0.9585, rely=0.075, relheight=0.875)

  img_array_map = {}
  # Display Database
  def show_records():
    for row in tree.get_children():
      tree.delete(row)
    
    rows = pull_from_db(table=(Tables.REGISTERED_STUDENTS, ), values=(RegStdsColumns.ID, RegStdsColumns.NAME, RegStdsColumns.COURSE, RegStdsColumns.YEAR, RegStdsColumns.IMAGE_ARRAY))
    # print(rows)
    for row in rows:
      """
      img_array - variable where array data is stored
      row[:4] - sets cell value from index 0 to 3 (not including index 4 because it's then replaced by "View" text)
      """
      img_array = row[4]
      masked_row = row[:4] + ("View", "Edit", )
      tree.insert("", "end", values=masked_row)

      img_array_map[row[0]] = img_array

  show_records()