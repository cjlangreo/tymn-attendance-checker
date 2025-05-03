import os, sys
import customtkinter as ctk
from tkinter import *
from tkinter import ttk
import datetime as dt


parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(parent_dir)

from lib.db_interface import pull_from_db

# Font Default
def set_font(size, weight):
  return ctk.CTkFont(family="Ubuntu", size=size, weight=weight)

def attendance_tab(main_frame):
  main = ctk.CTkFrame(master=main_frame, fg_color=main_frame.cget("fg_color"))
  main.propagate(False)
  main.place(relx=0.5, rely=0.5, relwidth=0.9, relheight=0.9, anchor="c")


  date = ctk.CTkLabel(master=main, text=f"{dt.datetime.now():%A, %B %d, %Y}", font=set_font(24, "bold"))
  date.pack()

  time = ctk.CTkLabel(master=main, font=set_font(32, "bold"))
  time.pack(pady=10)

  def clock():
    datetime = dt.datetime.now() 
    this_time = f"{datetime:%H:%M:%S}"
    time.configure(text=this_time)
    time.after(500, clock)

  clock()

  table_frame = ctk.CTkFrame(
    master=main, 
    fg_color="#2a2a2a",
    corner_radius=16,
  )
  table_frame.place(relx=0.5, rely=0.5, relwidth=0.95, relheight=0.7, anchor="c")

  tree = ttk.Treeview(master=table_frame, columns=("Name", "Date", "Time"), show="headings")
  
  def relative_width(event):
    tree_width = tree.winfo_width()

    tree.column("Name", width=int(tree_width * 0.4))
    tree.column("Time", width=int(tree_width * 0.3))
    tree.column("Date", width=int(tree_width * 0.3))

  tree.heading("Name", text="Name")
  tree.heading("Time", text="Time")
  tree.heading("Date", text="Date")

  tree.bind("<Configure>", relative_width)

  style = ttk.Style()
  style.theme_use("default")

  style.configure(
    "Treeview",
    background="red",
    foreground="#adadad",
    fieldbackground="transparent",
    font=("Ubuntu Mono", 14, "normal"),
    rowheight=50,
    borderwidth=0,
  )

  style.configure(
    "Treeview.Heading",
    font=("Ubuntu", 16, "bold"),
    relief="flat",
    borderwidth=0,
    height=50,
    background="#1a1a1a",
    foreground="#d8d8d8"
  )

  tree.pack(
    side="top",
    expand=True,
    fill="y",
    pady=20,
  )

  scan_btn = ctk.CTkButton(
    master=main,
    text="Scan",
    font=set_font(20, "bold"),
    fg_color="#E36A00",
    text_color="#d8d8d8",
    border_width=0,
    cursor="hand2",
    height=50,
    corner_radius=25
  )
  scan_btn.place(relx=0.5, rely=0.95, anchor="c")

