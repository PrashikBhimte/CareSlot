import tkinter as tk
from tkinter import messagebox
import requests
from adminScreen import adminScreen

def login():
    username = userName.get()
    password = passWord.get()
    role = role_var.get()

    responce = requests.post('http://localhost:5000/login', json={
        "role" : role,
        "username" : username,
        "password" : password
    })

    responce_data = responce.json()

    if responce_data['loginSuccess'] == 'True':
        window.destroy() 
        if role == "doctor":
            doctor_window = tk.Tk()
            doctor_window.title('Doctor login')
        elif role == "admin" or role == "receptionist":
            if responce_data['authority'] == 'A':
                adminScreen()
            elif responce_data['authority'] == 'R':
                receptionist_window = tk.Tk()
                receptionist_window.title('receptionist login')

    else:
        messagebox.showerror("Error", "Invalid username or password")


window = tk.Tk()
window.title('Login....')
window.geometry('350x200')
window.resizable(False, False)

role_var = tk.StringVar(window)
role_var.set("doctor") 
role_label = tk.Label(window, text="Select Role : ")
role_label.grid(row=0, column=0, padx=40, pady=20)
role_dropdown = tk.OptionMenu(window, role_var, "doctor", "admin", "receptionist")
role_dropdown.grid(row=0, column=1)
    
tk.Label(window, text='UserName : ').grid(column= 0, row= 1, padx=40, pady=20)
userName = tk.Entry(window)
userName.grid(column= 1, row= 1)
tk.Label(window, text='Password : ').grid(column= 0, row= 2, padx=40, pady=2)
passWord = tk.Entry(window, show="*")
passWord.grid(column= 1, row= 2)

submit = tk.Button(window, text='Submit', width=10, height=1, command=login)
submit.grid(column=1, row=3, pady=10)

window.mainloop()