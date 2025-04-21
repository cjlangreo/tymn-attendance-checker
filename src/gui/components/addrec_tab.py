import tkinter as tk
from fakedb import conn, cursor

def addrec_tab(main_frame):
  addrec_frame = tk.Frame(main_frame)
  addrec_label = tk.Label(addrec_frame, text="Add New Student Record", font=("Ubuntu", 32))
  addrec_label.pack()
  addrec_frame.pack()