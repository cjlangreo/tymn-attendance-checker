import tkinter as tk
import tkinter.font as tkFont

# Font Default
def set_font(size, weight):
  return tkFont.Font(family="Ubuntu", size=size, weight=weight)

def set_nav(nav_frame, main_frame, records_tab, addrec_tab):

  # Active Tab
  def active(bar, tab):
    hide_bar()
    bar.config(bg="#E36A00")
    del_tabs()
    tab(main_frame)

  def hide_bar():
    records_bar.config(bg="#1a1a1a")
    addrec_bar.config(bg="#1a1a1a")

  def del_tabs():
    for tab in main_frame.winfo_children():
      tab.destroy()
  
  # Nav Buttons
  records_btn = tk.Button(
    nav_frame, 
    text="Student Records", 
    font=set_font(16, "bold"),
    height=1,
    fg="#d8d8d8", 
    bg="#1a1a1a",
    activeforeground="#d8d8d8",
    activebackground="#1a1a1a",
    bd=0,
    highlightthickness=0,
    anchor="w",
    padx=20,
    pady=20,
    command=lambda: active(records_bar, records_tab)
  )
  records_btn.place(x=20, y=100, width=300)

  addrecds_btn = tk.Button(
    nav_frame, 
    text="Add Student Record", 
    font=set_font(16, "bold"),
    height=1,
    fg="#d8d8d8", 
    bg="#1a1a1a",
    activeforeground="#d8d8d8",
    activebackground="#1a1a1a",
    bd=0,
    highlightthickness=0,
    anchor="w",
    padx=20,
    pady=20,
    command=lambda: active(addrec_bar, addrec_tab)
  )
  addrecds_btn.place(x=20, y=170, width=300)

  # Active Button Bar
  global records_bar, addrec_bar

  records_bar = tk.Label(nav_frame, text="", bg="#1a1a1a")
  records_bar.place(x=2, y=110, width=10, height=50)

  addrec_bar = tk.Label(nav_frame, text="", bg="#1a1a1a")
  addrec_bar.place(x=2, y=180, width=10, height=50)

  return active, records_bar