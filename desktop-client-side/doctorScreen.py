import tkinter as tk
from tkinter import messagebox
from functions import initFrame
from fetchPatients import fetchPatientDetails

def exit():
    var = messagebox.askquestion("Exit", "Do you want to exit?")
    if var == "yes":
        root.destroy()

def mainframe(frame, sideFrame, id):
    tk.Button(frame, text="Fetch all patient details", width=30, height=1, command=lambda : fetchPatientDetails(sideFrame, id)).pack(padx=30, pady=15)
    tk.Button(frame, text="Exit", width=30, height=1, command=exit).pack(padx=30, pady=15)

def doctorScreen(id):
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

    mainframe(frame, bottomFrame, id)
    initFrame(topFrame)

    root.mainloop()