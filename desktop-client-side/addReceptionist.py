import tkinter as tk
from tkinter import messagebox
from functions import clearFrame, initFrame
import requests

def setUsernameAndPassword(frame):
    typed_username = str(username.get())
    typed_password = str(password.get())
    typed_ConformPassword = str(conform_password.get())

    if typed_password == typed_ConformPassword :
        try:
            responce = requests.post("http://localhost:5000/admin/add_login", json={
                "username" : typed_username,
                "password" : typed_password
            })

            if responce.status_code == 200 :
                messagebox.showinfo(title="Successful!", message="Username and Password are set successfully!")
                clearFrame(frame)
                initFrame(frame)
            elif responce.status_code == 409:
                messagebox.showerror(title="Unsuccessful!", message="Username Already exits!")
            else :
                messagebox.showerror(title="Unsuccessful!", message="Unadle to set!")
        except :
            messagebox.showwarning(title="Unsuccessful!", message="network error!")
    else: 
        messagebox.showerror(title="Unsuccessful!", message="Password does't match with conform password!")

def addReceptionist(frame):
    global username, password, conform_password
    clearFrame(frame)

    tk.Label(frame, text="Username: ").grid(column=0, row=0, padx=30, pady=15)
    username =  tk.Entry(frame, width=50)
    username.grid(column=1, row=0, padx=30, pady=15)

    tk.Label(frame, text="Password: ").grid(column=0, row=1, padx=30, pady=15)
    password =  tk.Entry(frame, width=50, show="*")
    password.grid(column=1, row=1, padx=30, pady=15)

    tk.Label(frame, text="Conform Password: ").grid(column=0, row=2, padx=30, pady=15)
    conform_password =  tk.Entry(frame, width=50, show="*")
    conform_password.grid(column=1, row=2, padx=30, pady=15)

    tk.Button(frame, text="Submit", width=10, command=lambda :setUsernameAndPassword(frame)).grid(column=1, row=3)