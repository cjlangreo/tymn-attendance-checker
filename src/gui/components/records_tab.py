import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from fakedb import connect_db

# Font Default
def set_font(size, weight):
  return tkFont.Font(family="Ubuntu", size=size, weight=weight)

def records_tab(main_frame):
  records_frame = tk.Frame(main_frame, width=900, height=800, bg=main_frame["bg"])
  records_frame.propagate(False)
  records_frame.pack(padx=40, pady=40)

  tk.Label(records_frame, text="Student Records", font=set_font(40, "bold"), bg=records_frame["bg"], fg="#d8d8d8").pack(anchor="w", pady=[0, 30])
  
  # Table Frame (tree + scrollbar)
  table_frame = tk.Frame(records_frame, bg=records_frame["bg"])
  table_frame.pack(fill="both", expand=True)

  # Table
  tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Course", "Year", "Image"), height=10, show="headings")
  tree.heading("ID", text="ID")
  tree.heading("Name", text="Name", anchor="w")
  tree.heading("Course", text="Course", anchor="w")
  tree.heading("Year", text="Year", anchor="w")
  tree.heading("Image", text="Image", anchor="w")

  tree.column("ID", width=80, anchor="center")
  tree.column("Name", width=420)
  tree.column("Course", width=100)
  tree.column("Year", width=100)
  tree.column("Image", width=100)

  # Scrollbar
  scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
  tree.configure(yscrollcommand = scrollbar.set)
  
  # Styling
  style = ttk.Style()
  style.theme_use("default")

  # Tree Rows and Columns Styling
  style.configure(
    "Treeview",
    background=table_frame["bg"],
    foreground="#adadad",
    fieldbackground=records_frame["bg"],
    font=("Ubuntu Mono", 14, "normal"),
    borderwidth=0,
    rowheight=50,
    )
  
  style.map(
    "Treeview",
    background=[("selected", "#E36A00")],
    foreground=[("selected", "#d8d8d8")]
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
    background="#444",
    arrowcolor=table_frame["bg"],
    borderwidth=0,
    troughcolor=table_frame["bg"]
  )

  style.map(
    "Vertical.TScrollbar",
    background=[("active", "#E36A00"), ("!active", "#444")]
  )

  # Pack scrollbar and tree
  tree.pack(side="left", fill="both", expand=True)
  scrollbar.pack(side="right", fill="y")

  # Display Database
  def show_records():
    for row in tree.get_children():
      tree.delete(row)
      
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT rowid, name, course, year FROM registered_students")
    rows = cursor.fetchall()
    for row in rows:
      tree.insert("", "end", values=row)

  show_records() 