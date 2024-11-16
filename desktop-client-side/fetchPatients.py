import tkinter as tk
import requests
from tkinter import messagebox
from functions import clearFrame
from addMedication import addMedication


class Button:
    def __init__(self, frame, data, i):
        self.frame = frame
        self.data = data
        self.i = i

    def createbutton(self):
        tk.Button(self.frame, text=self.data['time_slot'], width=10, command=lambda : self.showDetailsAndMakeForm()).grid(column=self.i, row=0)

    def showDetailsAndMakeForm(self):
        try :
            patient_responce = requests.post('http://localhost:5000/patient/veiw/personal', json={
                "id" : self.data['pat_id']
            })
            if patient_responce.status_code == 200 :
                patient_responce_data = patient_responce.json()
                showDetails(patient_responce_data)

            else :
                messagebox.showwarning(title="Unsuccessful!", message="Unadle to fetch data!")    
        except :
            messagebox.showwarning(title="Unsuccessful!", message="network error!")


def showDetails(i):
    
    clearFrame(DetailsFrame)

    name = i['name']
    gender = i['gender']
    dob = i['dob']
    phoneNo = i['phoneNo']
    address = i['address']
    email = i['email']

    tk.Label(DetailsFrame, text="Name: ").grid(column=0, row=0, padx=30, pady=15)
    tk.Label(DetailsFrame, text=name).grid(column=1, row=0, padx=30, pady=15)
    
    tk.Label(DetailsFrame, text="Gender:").grid(column=0, row=1)
    tk.Label(DetailsFrame, text=gender).grid(column=1, row=1)

    tk.Label(DetailsFrame, text="Date od Birth: ").grid(column=0, row=2, padx=30, pady=15)
    tk.Label(DetailsFrame, text=dob).grid(row=2, column=1)

    tk.Label(DetailsFrame, text="Phone Number: ").grid(column=0, row=3, padx=30, pady=15)
    tk.Label(DetailsFrame, text=phoneNo).grid(column=1, row=3, padx=30, pady=15)

    tk.Label(DetailsFrame, text="Address: ").grid(column=0, row=4, padx=30, pady=15)
    tk.Label(DetailsFrame, text=address).grid(column=1, row=4, padx=30, pady=15)

    tk.Label(DetailsFrame, text="Email: ").grid(column=0, row=5, padx=30, pady=15)
    tk.Label(DetailsFrame, text=email).grid(column=1, row=5, padx=30, pady=15)

    addMedication(MedFrame, i['id'], typed_date)


def showSlots(frame):
    global DetailsFrame, MedFrame
    clearFrame(frame)

    topFrame = tk.Frame(frame)
    topFrame.pack(side=tk.TOP, fill=tk.NONE)

    bottomFrame = tk.Frame(frame)
    bottomFrame.pack(side=tk.BOTTOM, fill=tk.NONE, expand=True)

    DetailsFrame = tk.Frame(bottomFrame)
    DetailsFrame.pack(side=tk.TOP, fill=tk.NONE)

    MedFrame = tk.Frame(bottomFrame)
    MedFrame.pack(side=tk.BOTTOM, fill=tk.NONE, expand=True)

    buttons = []
    for i in range(0, len(appointments_responce_data)):
        data = appointments_responce_data[i]
        buttons.append(Button(topFrame, data, i))
    for i in buttons:
        i.createbutton()

def fetchAppiontments(frame, id):
    global appointments_responce_data, typed_date
    
    typed_date = str(year.get()) + ("0" + str(month.get()) if len(str(month.get())) == 1 else str(month.get())) + ("0" + str(day.get()) if len(str(day.get())) == 1 else str(day.get()))

    try :
        appointments_responce = requests.post('http://localhost:5000/doctor/view/appointments', json={
            "date" : typed_date,
            "doc_id" : id
        })
        if appointments_responce.status_code == 200 :
            appointments_responce_data = appointments_responce.json()
            clearFrame(frame)
            showSlots(frame)

        else :
            messagebox.showwarning(title="Unsuccessful!", message="Unadle to fetch data!")    
    except :
        messagebox.showwarning(title="Unsuccessful!", message="network error!")

def fetchPatientDetails(frame, id):
    global year, month, day

    clearFrame(frame)

    years = [i for i in range(2024, 2025)]
    months = [i for i in range(1, 13)]
    days = [i for i in range(1, 32)]
    
    tk.Label(frame, text="Date : ").grid(column=0, row=0, padx=30, pady=15)
    year = tk.StringVar(frame)
    year.set('Select year')
    year_dropdown = tk.OptionMenu(frame, year, *years)
    year_dropdown.grid(row=0, column=1)
    month = tk.StringVar(frame)
    month.set('Select Month')
    month_dropdown = tk.OptionMenu(frame, month, *months)
    month_dropdown.grid(row=0, column=2)
    day = tk.StringVar(frame)
    day.set('Select Day')
    day_dropdown = tk.OptionMenu(frame, day, *days)
    day_dropdown.grid(row=0, column=3)

    fetch_button = tk.Button(frame, text="Fetch Patients", width=10, command=lambda : fetchAppiontments(frame, id))
    fetch_button.grid(column=1, row=1)