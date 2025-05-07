from PIL import Image
import customtkinter as ctk

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