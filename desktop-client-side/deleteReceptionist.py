import tkinter as tk
from functions import clearFrame, initFrame
import requests
from tkinter import messagebox

def showDetails(frame, username):
    clearFrame(frame)

    try :
        responce = requests.delete('http://localhost:5000/admin/login/delete', json={
            "username" : username
        })
        if responce.status_code == 200 :
            messagebox.showinfo(title="Successfull!", message="Data is Deleted successfully!")
            initFrame(frame)
        else :
            messagebox.showerror(title="Unsuccessful!", message="Unadle to Delete")
    except :
        messagebox.showwarning(title="Unsuccessful!", message="network error!")


def searchReceptionistToDelete(frame):
    global responce_data, receptionistname
    clearFrame(frame)

    try :
        responce = requests.get('http://localhost:5000/admin/view/usernames')
        if responce.status_code == 200 :
            responce_data = responce.json()
            receptionist_names = responce_data['usernames']

        else :
            messagebox.showwarning(title="Unsuccessful!", message="Unadle to fetch data!")    
    except :
        messagebox.showwarning(title="Unsuccessful!", message="network error!")

    tk.Label(frame, text="Receptionist Name: ").grid(column=0, row=2, padx=30, pady=15)
    receptionistname = tk.StringVar(frame)
    receptionistname.set('Select Name of Receptionist')
    receptionistname_dropdown = tk.OptionMenu(frame, receptionistname, *receptionist_names)
    receptionistname_dropdown.grid(row=2, column=1)
    receptionistname_dropdown.config(width=30)

    tk.Button(frame, text="Submit", width=10, command=lambda : showDetails(frame, str(receptionistname.get()))).grid(column=1, row=9)