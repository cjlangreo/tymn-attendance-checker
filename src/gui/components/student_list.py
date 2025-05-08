import os, sys
import customtkinter as ctk
from tkinter import ttk
from components import palette
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(parent_dir)

from lib.db_interface import pull_from_db, Tables, RegStdsColumns, update_student, delete_student
from lib.img_manip import bytes_to_image
from components.student_form import NameFrame, CourseFrame, StudentIDFrame, YearFrame, FaceDataFrame


# Font Default
def set_font(size, weight):
  return ctk.CTkFont(family="Ubuntu", size=size, weight=weight)

def set_font_mono(size, weight):
  return ctk.CTkFont(family="Ubuntu Mono", size=size, weight=weight)

def display_list(main_frame):

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
        edit_data = ctk.CTkToplevel(tree, fg_color=palette.PRIMARY_1)
        edit_data.title("Edit Student Data")
        edit_data.geometry("480x800")
        edit_data.propagate(False)
        edit_data.resizable(False, False)

        ed_wrapper = ctk.CTkFrame(master=edit_data, fg_color="transparent", corner_radius=0)
        ed_wrapper.place(relwidth=0.8, relheight=0.875, relx=0.5, rely=0.5, anchor="c" )
        ctk.CTkLabel(master=ed_wrapper, text="Edit Student Data", font=set_font(36, "bold"), text_color=palette.TEXT_1).pack(anchor="w", pady=(0, 24))
        
        # Name
        persinfo = NameFrame(master=ed_wrapper)
        persinfo.pack(fill="x")
        persinfo.name_entry.insert(0, values[1])

        acad_wrapper = ctk.CTkFrame(master=ed_wrapper, fg_color="transparent", corner_radius=0)
        acad_wrapper.place(relx=0.3, rely=0.3, relwidth=0.60, anchor="n")
        # Student ID
        stid = StudentIDFrame(master=acad_wrapper)
        stid.stid_label.configure(text="Student ID:")
        stid.pack(pady=(0, 12), fill="x")
        stid.stid_entry.insert(0, values[0])
        old_stdid = values[0]

        # Course
        course_frame = CourseFrame(master=acad_wrapper)
        course_frame.pack(anchor="w", pady=(0, 12), fill="x")
        course_frame.course_var.set(values[2])

        # Year
        year_frame = YearFrame(master=acad_wrapper)
        year_frame.pack(anchor="w", pady=(0, 12), fill="x")
        year_frame.year_var.set(values[3])

        def submit_button():
          update_student(old_stdid, ((RegStdsColumns.ID, stid.stid_entry.get()), (RegStdsColumns.NAME, persinfo.name_entry.get()), (RegStdsColumns.COURSE, course_frame.course_var.get()), (RegStdsColumns.YEAR, year_frame.year_var.get())))
          edit_data.destroy()

        def delete_button():
          delete_student(old_stdid)
          edit_data.destroy()

        # Delete Button
        delete_btn = ctk.CTkButton(
          master=ed_wrapper,
          text="- Delete",
          font=set_font(20, "bold"),
          fg_color=palette.PRIMARY_3,
          text_color=palette.TEXT_1,
          hover_color=palette.PRIMARY_4,
          border_width=0,
          cursor="hand2",
          height=50,
          corner_radius=10,
          command = delete_button
        )
        delete_btn.place(relx=0.6, rely=1, anchor="se")

        # Save Button
        submit_btn = ctk.CTkButton(
          master=ed_wrapper,
          text="+ Save",
          font=set_font(20, "bold"),
          fg_color=palette.TONE_1,
          text_color=palette.TEXT_2,
          hover_color=palette.TONE_2,
          border_width=0,
          cursor="hand2",
          height=50,
          corner_radius=10,
          command = submit_button
        )
        submit_btn.place(relx=1, rely=1, anchor="se")
        


  main = ctk.CTkFrame(master=main_frame, fg_color=main_frame.cget("fg_color"))
  main.propagate(False)
  main.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="c")
  # Table Frame (tree + scrollbar)
  table_frame = ctk.CTkFrame(
    master=main, 
    fg_color=palette.PRIMARY_2,
    corner_radius=8,
  )
  table_frame.place(relx=0, rely=0, relwidth=1, relheight=1, anchor="nw")

  # Treeview
  def relative_width(event):
    tree_width = tree.winfo_width()

    tree.column("ID", width=int(tree_width * 0.1), anchor="center")
    tree.column("Name", width=int(tree_width * 0.35))
    tree.column("Course", width=int(tree_width * 0.15), anchor="c")
    tree.column("Year", width=int(tree_width * 0.15), anchor="c")
    tree.column("Image", width=int(tree_width * 0.15), anchor="c")
    tree.column("", width=int(tree_width * 0.1), anchor="c")

  def block_header_drag(event):
    if tree.identify_region(event.x, event.y) == "separator":
        return "break"


  tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Course", "Year", "Image", ""), show="headings")
  tree.heading("ID", text="ID")
  tree.heading("Name", text="Name", anchor="w")
  tree.heading("Course", text="Course", anchor="c")
  tree.heading("Year", text="Year", anchor="c")
  tree.heading("Image", text="Image", anchor="c")
  tree.heading("", text="", anchor="c")

  tree.bind("<Configure>", relative_width)
  tree.bind("<Button-1>", data_onclick)
  tree.bind("<Button-1>", block_header_drag, add="+")

  # Scrollbar
  scrollbar = ctk.CTkScrollbar(master=table_frame, orientation="vertical", command=tree.yview)
  tree.configure(yscrollcommand = scrollbar.set)
  
  # Styling
  style = ttk.Style()
  style.theme_use("clam")

  # Tree Rows and Columns Styling
  style.configure(
    "Treeview",
    background=palette.PRIMARY_2,
    foreground=palette.TEXT_1,
    fieldbackground="transparent",
    font=("Ubuntu Mono", 14, "normal"),
    rowheight=50,
    borderwidth=0,
  )
  
  style.map(
    "Treeview",
    background=[("selected", palette.PRIMARY_2)],
    foreground=[("selected", palette.TEXT_1)]
  )

  # Tree Heading Styling
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
    "Treeview.Heading",
    background=[("active", palette.TONE_2)], 
    foreground=[("active", palette.TEXT_2)] 
  )

  # Scrollbar Styling 
  style.configure(
    "Vertical.TScrollbar",
    relief="flat",
    background=palette.PRIMARY_3,
    arrowcolor=table_frame["bg"],
    borderwidth=0,
    troughcolor=table_frame["bg"]
  )

  # Pack scrollbar and tree
  tree.pack(
    side="top",
    expand=True,
    fill="y",
    pady=12,
    padx=12,
  )
  scrollbar.place(anchor="e", relx=0.99, rely=0.525, relheight=0.9)

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
      masked_row = row[:4] + ("VIEW", "EDIT", )
      tree.insert("", "end", values=masked_row)

      img_array_map[row[0]] = img_array

  show_records()