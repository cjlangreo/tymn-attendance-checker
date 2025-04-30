import customtkinter as ctk

# Font Default
def set_font(size, weight):
  return ctk.CTkFont(family="Ubuntu", size=size, weight=weight)

def set_nav(nav_frame, main_frame, records_tab, addrec_tab):

  # Active Tab
  def active(bar, tab):

    hide_bar()
    bar.configure(fg_color="#E36A00")

    del_tabs()
    tab(main_frame)

  # Hide Bar
  def hide_bar():
    records_bar.configure(fg_color="#1a1a1a")
    addrec_bar.configure(fg_color="#1a1a1a")

  def del_tabs():
    for tab in main_frame.winfo_children():
      tab.destroy()
  
  # Nav Buttons
  records_btn = ctk.CTkButton(
    master=nav_frame, 
    text="Student Records", 
    font=set_font(16, "bold"),
    height=50,
    text_color="#d8d8d8", 
    fg_color="transparent",
    border_width=0,
    anchor="w",
    command=lambda: active(records_bar, records_tab)
  )
  records_btn.place(x=10, y=100, relwidth=1.0)

  addrecds_btn = ctk.CTkButton(
    master=nav_frame, 
    text="Add Student Record", 
    font=set_font(16, "bold"),
    text_color="#d8d8d8", 
    fg_color="transparent",
    border_width=0,
    height=50,
    anchor="w",
    command=lambda: active(addrec_bar, addrec_tab)
  )
  addrecds_btn.place(x=10, y=150, relwidth=1.0)

  # Active Button Bar
  global records_bar, addrec_bar

  records_bar = ctk.CTkLabel(master=nav_frame, text="", fg_color="#1a1a1a", width=10, height=50)
  records_bar.place(x=2, y=100, )

  addrec_bar = ctk.CTkLabel(master=nav_frame, text="", fg_color="#1a1a1a", width=10, height=50)
  addrec_bar.place(x=2, y=150)

  return active, records_bar