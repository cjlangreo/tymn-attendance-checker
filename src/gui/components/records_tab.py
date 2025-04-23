import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from fakedb import cursor

# Font Default
def set_font(size, weight):
  return tkFont.Font(family="Ubuntu", size=size, weight=weight)

def records_tab(main_frame):
  records_frame = tk.Frame(main_frame, width=900, height=800, bg=main_frame["bg"])
  records_frame.propagate(False)
  records_frame.pack(padx=40, pady=40)

  tk.Label(records_frame, text="Student Records", font=set_font(40, "bold"), bg=records_frame["bg"], fg="#d8d8d8").pack(anchor="w", pady=[0, 30])
  
  # Styling Table
  table_style = ttk.Style()
  table_style.theme_use("default")

  # Rows and Columns
  table_style.configure(
    "Treeview",
    background=records_frame["bg"],
    foreground="#adadad",
    fieldbackground=records_frame["bg"],
    font=("Ubuntu Mono", 14, "normal"),
    borderwidth=0,
    rowheight=50
    )
  table_style.map(
    "Treeview",
    background=[("selected", "#E36A00")],
    foreground=[("selected", "#d8d8d8")]
  )

  # Heading
  table_style.configure(
    "Treeview.Heading",
    font=("Ubuntu", 16, "bold"),
    relief="flat",
    borderwidth=0,
    height=50,
    background="#1a1a1a",
    foreground="#d8d8d8"
  )
  table_style.map(
    "Treeview.Heading",
    background=[("active", "#1a1a1a")], 
    foreground=[("active", "#d8d8d8")] 
  )


  # Table
  tree = ttk.Treeview(records_frame, columns=("ID", "Name", "Course", "Year"), show="headings")
  tree.heading("ID", text="ID")
  tree.heading("Name", text="Name")
  tree.heading("Course", text="Course")
  tree.heading("Year", text="Year")

  tree.column("ID", width=80, anchor="center")
  tree.column("Name", width=400)
  tree.column("Course", width=220)
  tree.column("Year", width=100)

  tree.pack(anchor="w")

  # Display Database
  def show_records():
    for row in tree.get_children():
      tree.delete(row)
    
    cursor.execute("SELECT id, name, course, year FROM registered_students")
    rows = cursor.fetchall()
    for row in rows:
      tree.insert("", "end", values=row)

  show_records() 