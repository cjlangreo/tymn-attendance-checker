import os, sys
import customtkinter as ctk
from components import assets
from components import palette
# parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
# sys.path.append(parent_dir)


class TabButton(ctk.CTkButton):
  def __init__(self, master, text, command, image, **kwargs):
    super().__init__(
      master,
      text=text,
      command=command,
      image=image,
      font=set_font(20, "bold"),
      text_color=palette.TEXT_1, 
      fg_color="transparent",
      hover_color=palette.PRIMARY_1,
      border_width=0,
      corner_radius=8,
      height=50,
      compound="left",
      anchor="w",
      **kwargs)


# Font Default
def set_font(size, weight):
  return ctk.CTkFont(family="Ubuntu", size=size, weight=weight)

def set_nav(nav_frame, main_frame, display_log, display_list, display_form):

  # Active Tab
  def active(btn, tab):

    reset_text()
    btn.configure(text_color=palette.TONE_1)
    if btn == attendance_btn:
      btn.configure(image=assets.calendar_tone)
    if btn == list_btn:
      btn.configure(image=assets.students_tone)
    if btn == add_btn:
      btn.configure(image=assets.add_stud_tone)

    del_tabs()
    tab(main_frame)

  # Hide Bar
  def reset_text():
    btns = [attendance_btn, list_btn, add_btn]

    for btn in btns:
      btn.configure(text_color=palette.TEXT_1)

    btns[0].configure(image=assets.calendar_light)
    btns[1].configure(image=assets.students_light)
    btns[2].configure(image=assets.add_stud_light)

  def del_tabs():
    for tab in main_frame.winfo_children():
      tab.destroy()
  

  attendance_btn = TabButton(master=nav_frame, text="  Attendance", command=lambda: active(attendance_btn, display_log), image=assets.calendar_light)
  attendance_btn.place(relx=0.5, y=50, relwidth=0.9, anchor="c")

  list_btn = TabButton(master=nav_frame, text="  Student Records", command=lambda: active(list_btn, display_list), image=assets.students_light)
  list_btn.place(relx=0.5, y=100, relwidth=0.9, anchor="c")

  add_btn = TabButton(master=nav_frame, text="  Add Student", command=lambda: active(add_btn, display_form), image=assets.add_stud_light)
  add_btn.place(relx=0.5, y=150, relwidth=0.9, anchor="c")

  return active, attendance_btn