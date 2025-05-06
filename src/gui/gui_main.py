import customtkinter as ctk
from components.nav import set_nav
from components.student_list import display_list
from components.student_form import display_form
from components.attendance_log import display_log
from lib.img_manip import create_temp_folder, bytes_to_image
from lib.db_interface import pull_from_db, RegStdsColumns, Tables

# Create the temp folder and load all images
create_temp_folder()
records = pull_from_db(table=(Tables.REGISTERED_STUDENTS, ), values=(RegStdsColumns.ID, RegStdsColumns.IMAGE_ARRAY))
for record in records:
    # print(record)
    bytes_to_image(record[1], record[0])

# Create a window
window = ctk.CTk()
window.title("Apprizz")
window.geometry("1366x768")
window.configure(background="#222222")
window.resizable(False, False)

# Navigation Bar Frame
nav_frame = ctk.CTkFrame(window, fg_color="#1a1a1a")
nav_frame.place(relx = 0.0, relwidth=0.2, relheight=1.0)
nav_frame.propagate(False)

# Main Frame
main_frame = ctk.CTkFrame(window, fg_color="#222")
main_frame.place(relx=0.2, relwidth=0.8, relheight=1.0)
main_frame.propagate(False)

class GUIController:
  def __init__(self, main_frame, nav_frame, display_log, display_list, display_form):
    self.main_frame = main_frame
    self.nav_frame = nav_frame
    self.display_log = display_log
    self.display_list = display_list
    self.display_form = display_form
    """
    Destructure set_nav() into active and init_bar: 
    => set_nav(x, y) where: active_fn = x, init_bar = y 
    """
    self.active_fn, self.init_bar = set_nav(nav_frame, main_frame, display_log, display_list, display_form)

  def refresh_attendance(self):
        self.active_fn(self.init_bar, self.display_log)

controller = GUIController(main_frame, nav_frame, display_log, display_list, display_form)
controller.refresh_attendance()

window.mainloop()

  

