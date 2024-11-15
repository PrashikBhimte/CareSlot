import tkinter as tk
from functions import clearFrame, initFrame
import requests
from tkinter import messagebox

def showDetails(frame, res_name):
    clearFrame(frame)
    for  i in responce_data:
        if i['name'] == res_name:
            id = i['id']

            try :
                responce = requests.delete('http://localhost:5000/admin/employee/delete', json={
                    "id" : id
                })
                if responce.status_code == 200 :
                    messagebox.showinfo(title="Successfull!", message="Data is Deleted successfully!")
                    initFrame(frame)
                else :
                    messagebox.showerror(title="Unsuccessful!", message="Unadle to Delete")
            except :
                messagebox.showwarning(title="Unsuccessful!", message="network error!")


def searchEmployeeToDelete(frame):
    global responce_data
    clearFrame(frame)

    try :
        responce = requests.get('http://localhost:5000/employees/all')
        if responce.status_code == 200 :
            responce_data = responce.json()
            employee_names = [i['name'] for i in responce_data]

        else :
            messagebox.showwarning(title="Unsuccessful!", message="Unadle to fetch data!")    
    except :
        messagebox.showwarning(title="Unsuccessful!", message="network error!")

    tk.Label(frame, text="Doctor Name: ").grid(column=0, row=2, padx=30, pady=15)
    employeename = tk.StringVar(frame)
    employeename.set('Select Name of doctor')
    employeename_dropdown = tk.OptionMenu(frame, employeename, *employee_names)
    employeename_dropdown.grid(row=2, column=1)
    employeename_dropdown.config(width=30)

    tk.Button(frame, text="Submit", width=10, command=lambda : showDetails(frame, str(employeename.get()))).grid(column=1, row=9)