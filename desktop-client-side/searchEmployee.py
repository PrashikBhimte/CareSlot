import tkinter as tk
from functions import clearFrame
import requests
from tkinter import messagebox

def showDetails(frame, res_name):
    clearFrame(frame)
    for  i in responce_data:
        if i['name'] == res_name:
            name = i['name']
            gender = i['gender']
            dob = i['dob']
            phoneNo = i['phoneNo']
            address = i['address']
            email = i['email']
            doj = ['doj']
            qualification = i['qualification']
            designation = i['designation']

            tk.Label(frame, text="Name: ").grid(column=0, row=0, padx=30, pady=15)
            tk.Label(frame, text=name).grid(column=1, row=0, padx=30, pady=15)
            
            tk.Label(frame, text="Gender:").grid(column=0, row=1)
            tk.Label(frame, text=gender).grid(column=1, row=1)

            tk.Label(frame, text="Date od Birth: ").grid(column=0, row=2, padx=30, pady=15)
            tk.Label(frame, text=dob).grid(row=2, column=1)

            tk.Label(frame, text="Phone Number: ").grid(column=0, row=3, padx=30, pady=15)
            tk.Label(frame, text=phoneNo).grid(column=1, row=3, padx=30, pady=15)

            tk.Label(frame, text="Address: ").grid(column=0, row=4, padx=30, pady=15)
            tk.Label(frame, text=address).grid(column=1, row=4, padx=30, pady=15)

            tk.Label(frame, text="Email: ").grid(column=0, row=5, padx=30, pady=15)
            tk.Label(frame, text=email).grid(column=1, row=5, padx=30, pady=15)

            tk.Label(frame, text="Date of joining: ").grid(column=0, row=6, padx=30, pady=15)
            tk.Label(frame, text=doj).grid(row=6, column=1)

            tk.Label(frame, text="Qualifictaion: ").grid(column=0, row=7, padx=30, pady=15)
            tk.Label(frame, text=qualification).grid(column=1, row=7, padx=30, pady=15)

            tk.Label(frame, text="Designation: ").grid(column=0, row=8, padx=30, pady=15)
            tk.Label(frame, text=designation).grid(column=1, row=8, padx=30, pady=15)

def searchEmployee(frame):
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

    tk.Label(frame, text="Employee Name: ").grid(column=0, row=2, padx=30, pady=15)
    employeename = tk.StringVar(frame)
    employeename.set('Select Name of Employee')
    employeename_dropdown = tk.OptionMenu(frame, employeename, *employee_names)
    employeename_dropdown.grid(row=2, column=1)
    employeename_dropdown.config(width=30)

    tk.Button(frame, text="Submit", width=10, command=lambda : showDetails(frame, str(employeename.get()))).grid(column=1, row=9)