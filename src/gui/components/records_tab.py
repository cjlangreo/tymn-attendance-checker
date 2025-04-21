import tkinter as tk
from tkinter import ttk
from fakedb import cursor

def records_tab(main_frame):
  records_frame = tk.Frame(main_frame)
  records_label = tk.Label(records_frame, text="List of Student Records", font=("Ubuntu", 32))
  records_label.pack()
  records_frame.pack()

  # Table
  tree = ttk.Treeview(records_frame, columns=("ID", "Name", "Course", "Year"), show="headings")
  tree.heading("ID", text="ID")
  tree.heading("Name", text="Name")
  tree.heading("Course", text="Course")
  tree.heading("Year", text="Year")

  tree.column("ID", width=40, anchor="center")
  tree.column("Name", width=120)
  tree.column("Course", width=60)
  tree.column("Year", width=40)

  tree.pack()

  # Display Database
  def show_records():
    for row in tree.get_children():
      tree.delete(row)
    
    cursor.execute("SELECT id, name, course, year FROM registered_students")
    rows = cursor.fetchall()
    for row in rows:
      tree.insert("", "end", values=row)

  show_records() 