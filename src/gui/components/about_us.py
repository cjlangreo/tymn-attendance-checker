import customtkinter as ctk
from gui.components import assets
from gui.components import palette

# Font Default
def set_font(size, weight):
  return ctk.CTkFont(family="Ubuntu", size=size, weight=weight)

def set_font_mono(size, weight):
  return ctk.CTkFont(family="Ubuntu Mono", size=size, weight=weight)

def display_about(main_frame):
  main = ctk.CTkFrame(master=main_frame, fg_color=main_frame.cget("fg_color"))
  main.place(relx=0.5, rely=0.5, anchor="c", relheight=0.85)

  ctk.CTkLabel(master=main, text="", image=assets.typog_logo).pack(anchor="c", pady=36)
  ctk.CTkLabel(master=main, text="Tymn: An AI-based Face Recognition\nStudent Attendance Checker", text_color=palette.TEXT_1, font=set_font(28, "bold")).pack(anchor="c")
  ctk.CTkLabel(master=main, text="Developed by:", text_color=palette.TEXT_1, font=set_font(20, "normal")).pack(anchor="w", pady=(64, 16))
  ctk.CTkLabel(
    master=main, 
    text="Chanz Jryko F. Langreo\n" \
    "Donna S. Birol\n" 
    "Shem E. Mariano",
    text_color=palette.TEXT_1, 
    font=set_font_mono(24, "normal")
  ).pack(anchor="c",pady=(0, 48))
  resized = ctk.CTkImage(light_image=assets.favicon._light_image, size=(64, 64))
  ctk.CTkLabel(master=main, text="", image=resized).pack(anchor="c")
  ctk.CTkLabel(master=main, text="All Rights Reserved © 2025", font=set_font(16, "normal"), text_color=palette.TONE_2).pack(anchor="c", pady=(64, 0))
