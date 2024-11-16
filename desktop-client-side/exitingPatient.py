import tkinter as tk
from functions import clearFrame
import requests
from tkinter import messagebox

def showDetails(frame, pat_id, doc_id, date, time_slot):
    clearFrame(frame)

    try:
        responce = requests.post("http://localhost:5000/patient/appiontment/book", json={
            "pat_id" : pat_id,
            "doc_id" : doc_id,
            "date" : date,
            "time_slot" : time_slot
        })

        if responce.status_code == 200 :
            messagebox.showinfo(title="Successful!", message="Appointment is Booked Susscessfully!")
            clearFrame(frame)
        else :
            messagebox.showerror(title="Unsuccessful!", message="Unadle to Book appointment!")
    except :
        messagebox.showwarning(title="Unsuccessful!", message="network error!")

def fetchSlots(frame):
    fetch_button.destroy()

    typed_patientname = str(patientname.get())
    typed_docname = str(doctorname.get())
    typed_date = str(year.get()) + ("0" + str(month.get()) if len(str(month.get())) == 1 else str(month.get())) + ("0" + str(day.get()) if len(str(day.get())) == 1 else str(day.get()))

    for i in doc_responce_data:
        if i['name'] == typed_docname :
            doc_id = i['id']

    for i in pat_responce_data:
        if i['name'] == typed_patientname :
            pat_id = i['id']

    try :
        slots_responce = requests.post('http://localhost:5000/patient/view/availableslots', json={
            "date" : typed_date,
            "doc_id" : doc_id
        })
        if slots_responce.status_code == 200 :
            slots_responce_data = slots_responce.json()
            timeSlots = slots_responce_data['available_slots']

        else :
            messagebox.showwarning(title="Unsuccessful!", message="Unadle to fetch data!")    
    except :
        messagebox.showwarning(title="Unsuccessful!", message="network error!")

    if len(timeSlots) == 0 :
        messagebox.showerror(title="Empty Data", message="There are no time slots available!")
        clearFrame(frame)
    else:
        tk.Label(frame, text="Time Slots: ").grid(column=0, row=3, padx=30, pady=15)
        timeSlot = tk.StringVar(frame)
        timeSlot.set('Select Time Slot')
        timeSlot_dropdown = tk.OptionMenu(frame, timeSlot, *timeSlots)
        timeSlot_dropdown.grid(row=3, column=1)
        timeSlot_dropdown.config(width=30) 

        tk.Button(frame, text="Submit", width=10, command=lambda : showDetails(frame, pat_id, doc_id, typed_date, str(timeSlot.get()))).grid(column=1, row=4)

def searchPatient(frame):
    global pat_responce_data, fetch_button, year, month, day, patientname, doctorname, doc_responce_data
    clearFrame(frame)

    years = [i for i in range(2024, 2025)]
    months = [i for i in range(1, 13)]
    days = [i for i in range(1, 32)]

    try :
        pat_responce = requests.get('http://localhost:5000/patient/all')
        if pat_responce.status_code == 200 :
            pat_responce_data = pat_responce.json()
            patient_names = [i['name'] for i in pat_responce_data]

        else :
            messagebox.showwarning(title="Unsuccessful!", message="Unadle to fetch data!")    
    except :
        messagebox.showwarning(title="Unsuccessful!", message="network error!")

    if len(pat_responce_data) == 0 :
        messagebox.showerror(title="Empty Data", message="There are no patient available!")
        clearFrame(frame)
    else:
        tk.Label(frame, text="Patient Name: ").grid(column=0, row=0, padx=30, pady=15)
        patientname = tk.StringVar(frame)
        patientname.set('Select Name of Patient')
        patientname_dropdown = tk.OptionMenu(frame, patientname, *patient_names)
        patientname_dropdown.grid(row=0, column=1)
        patientname_dropdown.config(width=30)

        try :
            doc_responce = requests.get('http://localhost:5000/doctor/all')
            if doc_responce.status_code == 200 :
                doc_responce_data = doc_responce.json()
                doctor_names = [i['name'] for i in doc_responce_data]

            else :
                messagebox.showwarning(title="Unsuccessful!", message="Unadle to fetch data!")    
        except :
            messagebox.showwarning(title="Unsuccessful!", message="network error!")

        if len(doc_responce_data) == 0 :
            messagebox.showerror(title="Empty Data", message="There are no doctors available!")
            clearFrame(frame)
        else:
            tk.Label(frame, text="Doctor Name: ").grid(column=0, row=1, padx=30, pady=15)
            doctorname = tk.StringVar(frame)
            doctorname.set('Select Name of doctor')
            doctorname_dropdown = tk.OptionMenu(frame, doctorname, *doctor_names)
            doctorname_dropdown.grid(row=1, column=1)
            doctorname_dropdown.config(width=30)

            tk.Label(frame, text="Date : ").grid(column=0, row=2, padx=30, pady=15)
            year = tk.StringVar(frame)
            year.set('Select year')
            year_dropdown = tk.OptionMenu(frame, year, *years)
            year_dropdown.grid(row=2, column=1)
            month = tk.StringVar(frame)
            month.set('Select Month')
            month_dropdown = tk.OptionMenu(frame, month, *months)
            month_dropdown.grid(row=2, column=2)
            day = tk.StringVar(frame)
            day.set('Select Day')
            day_dropdown = tk.OptionMenu(frame, day, *days)
            day_dropdown.grid(row=2, column=3)

            fetch_button = tk.Button(frame, text="Fetch Time Slots", width=10, command=lambda : fetchSlots(frame))
            fetch_button.grid(column=1, row=3)
