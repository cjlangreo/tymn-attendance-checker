import customtkinter as ctk
from components import palette

class TabButton(ctk.CTkButton):
  def __init__(self, master, text, command, **kwargs):
    super().__init__(
      master,
      text=text,
      command=command,
      font=set_font(16, "bold"),
      text_color=palette.TEXT_1, 
      fg_color="transparent",
      hover_color=palette.PRIMARY_1,
      border_width=0,
      corner_radius=0,
      height=50,
      anchor="w",
      **kwargs)


# Font Default
def set_font(size, weight):
  return ctk.CTkFont(family="Ubuntu", size=size, weight=weight)

def set_nav(nav_frame, main_frame, display_log, display_list, display_form):

  # Active Tab
  def active(bar, tab):

    hide_bar()
    bar.configure(fg_color=palette.TONE_1)

    del_tabs()
    tab(main_frame)

  # Hide Bar
  def hide_bar():
    attendance_bar.configure(fg_color="transparent")
    records_bar.configure(fg_color="transparent")
    addrec_bar.configure(fg_color="transparent")

  def del_tabs():
    for tab in main_frame.winfo_children():
      tab.destroy()
  

  attendance_btn = TabButton(master=nav_frame, text="          Attendance Logs", command=lambda: active(attendance_bar, display_log))
  attendance_btn.place(x=0, y=50, relwidth=1.0)

  list_btn = TabButton(master=nav_frame, text="          Student List", command=lambda: active(records_bar, display_list))
  list_btn.place(x=0, y=100, relwidth=1.0)

  add_btn = TabButton(master=nav_frame, text="          Add Student Data", command=lambda: active(addrec_bar, display_form))
  add_btn.place(x=0, y=150, relwidth=1.0)

  # Active Button Bar
  global attendance_bar, records_bar, addrec_bar

  attendance_bar = ctk.CTkLabel(master=nav_frame, text="", width=10, height=50)
  attendance_bar.place(x=0, y=50)

  records_bar = ctk.CTkLabel(master=nav_frame, text="", width=10, height=50)
  records_bar.place(x=0, y=100, )

  addrec_bar = ctk.CTkLabel(master=nav_frame, text="", width=10, height=50)
  addrec_bar.place(x=0, y=150)

  return active, attendance_bar