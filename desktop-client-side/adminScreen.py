import tkinter as tk
from tkinter import messagebox
from addNewDoctor import addNewDoctor
from functions import initFrame
from addNewEmployee import addNewEmplyee
from searchDoctor import searchDoctor
from searchEmployee import searchEmployee
from updateDoctor import updateDoctor
from updateEmployee import updateEmployee
from deleteDoctor import searchDoctorToDelete
from deleteEmployee import searchEmployeeToDelete
from addReceptionist import addReceptionist
from deleteReceptionist import searchReceptionistToDelete

def exit():
    var = messagebox.askquestion("Exit", "Do you want to exit?")
    if var == "yes":
        root.destroy()

def mainframe(frame, sideFrame):
    tk.Button(frame, text="Add new Doctor", width=30, height=1, command=lambda :addNewDoctor(sideFrame)).pack(padx=30, pady=15)
    tk.Button(frame, text="Show Doctor Details", width=30, height=1, command=lambda : searchDoctor(sideFrame)).pack(padx=30, pady=15)
    tk.Button(frame, text="Update Doctor Details", width=30, height=1, command=lambda: updateDoctor(sideFrame)).pack(padx=30, pady=15)
    tk.Button(frame, text="Delete Doctor Details", width=30, height=1, command=lambda : searchDoctorToDelete(sideFrame)).pack(padx=30, pady=15)
    tk.Button(frame, text="Add new Employee", width=30, height=1, command=lambda : addNewEmplyee(sideFrame)).pack(padx=30, pady=15)
    tk.Button(frame, text="Show Employee Details", width=30, height=1, command=lambda : searchEmployee(sideFrame)).pack(padx=30, pady=15)
    tk.Button(frame, text="Update Employeeq Details", width=30, height=1, command=lambda : updateEmployee(sideFrame)).pack(padx=30, pady=15)
    tk.Button(frame, text="Delete Employeeq Details", width=30, height=1, command=lambda : searchEmployeeToDelete(sideFrame)).pack(padx=30, pady=15)
    tk.Button(frame, text="Add New Receptionist", width=30, height=1, command=lambda : addReceptionist(sideFrame)).pack(padx=30, pady=15)
    tk.Button(frame, text="Delete Receptionist", width=30, height=1, command=lambda : searchReceptionistToDelete(sideFrame)).pack(padx=30, pady=15)
    tk.Button(frame, text="Exit", width=30, height=1, command=exit).pack(padx=30, pady=15)

def adminScreen():
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