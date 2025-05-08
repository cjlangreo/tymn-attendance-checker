from PIL import Image
import customtkinter as ctk
import tkinter as tk

calendar_tone = ctk.CTkImage(
  light_image=Image.open("src/gui/assets/nav_icons/calendar.png"),
  size=(20, 20)
)
calendar_light = ctk.CTkImage(
  light_image=Image.open("src/gui/assets/nav_icons/calendar-light.png"),
  size=(20, 20)
)
students_tone = ctk.CTkImage(
  light_image=Image.open("src/gui/assets/nav_icons/users.png"),
  size=(20, 20)
)
students_light = ctk.CTkImage(
  light_image=Image.open("src/gui/assets/nav_icons/users-light.png"),
  size=(20, 20)
)
add_stud_tone = ctk.CTkImage(
  light_image=Image.open("src/gui/assets/nav_icons/add-user.png"),
  size=(20, 20)
)
add_stud_light = ctk.CTkImage(
  light_image=Image.open("src/gui/assets/nav_icons/add-user-light.png"),
  size=(20, 20)
)

typog_logo = ctk.CTkImage(
  light_image=Image.open("src/gui/assets/brand_icons/icon_0.png"),
  size=(256, 67)
)

favicon = ctk.CTkImage(
  light_image=Image.open("src/gui/assets/brand_icons/icon_1.png"),
  size=(30, 30)
)

name = ctk.CTkImage(
  light_image=Image.open("src/gui/assets/form_icons/name.png"),
  size=(24, 24)
)
face = ctk.CTkImage(
  light_image=Image.open("src/gui/assets/form_icons/face.png"),
  size=(24, 24)
)
fingerprint = ctk.CTkImage(
  light_image=Image.open("src/gui/assets/form_icons/fingerprint.png"),
  size=(24, 24)
)
id = ctk.CTkImage(
  light_image=Image.open("src/gui/assets/form_icons/id.png"),
  size=(24, 24)
)
course = ctk.CTkImage(
  light_image=Image.open("src/gui/assets/form_icons/course.png"),
  size=(24, 24)
)
year = ctk.CTkImage(
  light_image=Image.open("src/gui/assets/form_icons/year.png"),
  size=(24, 24)
)