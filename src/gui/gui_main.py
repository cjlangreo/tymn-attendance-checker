import tkinter as tk
from tkinter import ttk
import tkinter.font as tkFont
from fakedb import conn, cursor
from components.nav import set_nav
from components.records_tab import records_tab
from components.addrec_tab import addrec_tab


# Create a window
window = tk.Tk()
window.title("Apprizz")
window.geometry("1200x800")
window.configure(background="#222222")
window.resizable(False, False)

# Navigation Bar Frame
nav_frame = tk.Frame(window, bg="#1a1a1a", width=300, height=800)
nav_frame.pack(side="left")
nav_frame.propagate(False)

# Main Frame
main_frame = tk.Frame(window, bg="#222")
main_frame.pack(side="right")
main_frame.propagate(False)
main_frame.configure(width=900, height=800)

set_nav(nav_frame, main_frame, records_tab, addrec_tab)

# Run the app
active, records_bar = set_nav(nav_frame, main_frame, records_tab, addrec_tab)
active(records_bar, records_tab)
window.mainloop()
