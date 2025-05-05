import os, sys
import customtkinter as ctk
from tkinter import ttk

parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(parent_dir)

from lib.db_interface import pull_from_db

# Font Default
def set_font(size, weight):
  return ctk.CTkFont(family="Ubuntu", size=size, weight=weight)

def display_list(main_frame):
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
  def relative_width(event):
    tree_width = tree.winfo_width()

    tree.column("ID", width=int(tree_width * 0.1), anchor="center")
    tree.column("Name", width=int(tree_width * 0.35))
    tree.column("Image", width=int(tree_width * 0.2))
    tree.column("Course", width=int(tree_width * 0.15))
    tree.column("Year", width=int(tree_width * 0.15))

  tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Image", "Course", "Year"), show="headings")
  tree.heading("ID", text="ID")
  tree.heading("Name", text="Name", anchor="w")
  tree.heading("Image", text="Image", anchor="w")
  tree.heading("Course", text="Course", anchor="w")
  tree.heading("Year", text="Year", anchor="w")

  tree.bind("<Configure>", relative_width)

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
    foreground="#adadad",
    fieldbackground="transparent",
    font=("Ubuntu Mono", 14, "normal"),
    rowheight=50,
    borderwidth=0,
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

  # Display Database
  def show_records():
    for row in tree.get_children():
      tree.delete(row)
    
    rows = pull_from_db()
    # print(rows)
    for row in rows:
      tree.insert("", "end", values=row)

  show_records()