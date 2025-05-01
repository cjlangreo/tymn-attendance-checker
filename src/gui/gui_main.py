import customtkinter as ctk
from components.nav import set_nav
from components.records_tab import records_tab
from components.addrec_tab import addrec_tab
from components.attendance import attendance_tab

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

# set_nav(nav_frame, main_frame, records_tab, addrec_tab)

# Run the app
"""
Destructure set_nav() into active and init_bar: 
  => set_nav(x, y) where: active_fn = x, init_bar = y 
"""
active_fn, init_bar = set_nav(nav_frame, main_frame, attendance_tab, records_tab, addrec_tab)

active_fn(init_bar, attendance_tab)

window.mainloop()
