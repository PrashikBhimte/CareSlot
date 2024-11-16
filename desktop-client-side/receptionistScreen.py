import tkinter as tk
from tkinter import messagebox
from functions import initFrame
from exitingPatient import searchPatient
from newPatient import addNewPatient


def exit():
    var = messagebox.askquestion("Exit", "Do you want to exit?")
    if var == "yes":
        root.destroy()

def mainframe(frame, sideFrame):
    tk.Button(frame, text="Exiting Patient", width=30, height=1, command=lambda : searchPatient(sideFrame)).pack(padx=30, pady=15)
    tk.Button(frame, text="New Patient", width=30, height=1, command=lambda : addNewPatient(sideFrame)).pack(padx=30, pady=15)
    tk.Button(frame, text="Exit", width=30, height=1, command=exit).pack(padx=30, pady=15)

def receptionistScreen():
    global root

    root = tk.Tk()
    root.title("Hospital Management System PPMD")
    root.attributes('-fullscreen', True)

    screen_width = root.winfo_width()
    screen_height = root.winfo_height()
 
    frame = tk.Frame(root, bg='blue', width=screen_width//3, height=screen_height)
    frame.pack(side=tk.LEFT, fill=tk.BOTH)

    sideFrame = tk.Frame(root, width=2*(screen_width//3), height=screen_height)
    sideFrame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    topFrame = tk.Frame(sideFrame, width=2*(screen_width//3), height=screen_height//3)
    topFrame.pack(side=tk.TOP, fill=tk.NONE)

    bottomFrame = tk.Frame(sideFrame, width=2*(screen_width//3), height=2*(screen_height//3))
    bottomFrame.pack(side=tk.BOTTOM, fill=tk.NONE, expand=True)

    mainframe(frame, bottomFrame)
    initFrame(topFrame)

    root.mainloop()