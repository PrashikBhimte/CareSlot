import tkinter as tk

def clearFrame(frame):
    for widget in frame.winfo_children():
        widget.destroy()

def is_aplha_with_space(string):
    for char in string:
        if not (char.isalpha() or char.isspace()):
            return False
    return True 

def initFrame(frame):
    clearFrame(frame)
    tk.Label(frame, text="Welcome to CareSLOT.", font=("Arial", 25)).pack(padx=150)
