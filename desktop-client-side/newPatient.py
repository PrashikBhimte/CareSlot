import tkinter as tk
from functions import clearFrame, is_aplha_with_space
import requests
from tkinter import messagebox

def bookSlot(frame, pat_id, doc_id, date, time_slot):
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

def fetchSlots(frame, pat_id):
    fetch_button.destroy()

    typed_docname = str(doctorname.get())
    typed_date = str(year.get()) + ("0" + str(month.get()) if len(str(month.get())) == 1 else str(month.get())) + ("0" + str(day.get()) if len(str(day.get())) == 1 else str(day.get()))

    for i in doc_responce_data:
        if i['name'] == typed_docname :
            doc_id = i['id']

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

        tk.Button(frame, text="Submit", width=10, command=lambda : bookSlot(frame, pat_id, doc_id, typed_date, str(timeSlot.get()))).grid(column=1, row=4)

def bookingAppointment(frame, pat_id):
    clearFrame(frame)
    global fetch_button, doctorname, doc_responce_data, year, month, day

    years = [i for i in range(2024, 2025)]
    months = [i for i in range(1, 13)]
    days = [i for i in range(1, 32)]

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
        tk.Label(frame, text="Doctor Name: ").grid(column=0, row=0, padx=30, pady=15)
        doctorname = tk.StringVar(frame)
        doctorname.set('Select Name of doctor')
        doctorname_dropdown = tk.OptionMenu(frame, doctorname, *doctor_names)
        doctorname_dropdown.grid(row=0, column=1)
        doctorname_dropdown.config(width=30)

        tk.Label(frame, text="Date : ").grid(column=0, row=1, padx=30, pady=15)
        year = tk.StringVar(frame)
        year.set('Select year')
        year_dropdown = tk.OptionMenu(frame, year, *years)
        year_dropdown.grid(row=1, column=1)
        month = tk.StringVar(frame)
        month.set('Select Month')
        month_dropdown = tk.OptionMenu(frame, month, *months)
        month_dropdown.grid(row=1, column=2)
        day = tk.StringVar(frame)
        day.set('Select Day')
        day_dropdown = tk.OptionMenu(frame, day, *days)
        day_dropdown.grid(row=1, column=3)

        fetch_button = tk.Button(frame, text="Fetch Time Slots", width=10, command=lambda : fetchSlots(frame, pat_id))
        fetch_button.grid(column=1, row=2)

def addDetails(frame, id):
    typed_name = str(name.get())
    if is_aplha_with_space(typed_name):
        typed_gender = str(gender.get())
        typed_bod = str(birth_year.get()) + ("0" + str(birth_month.get()) if len(str(birth_month.get())) == 1 else str(birth_month.get())) + ("0" + str(birth_day.get()) if len(str(birth_day.get())) == 1 else str(birth_day.get()))
        try :
            typed_phoneNo = str(phoneNo.get())
            if len(typed_phoneNo) == 10:
                typed_address = str(address.get())
                typed_email = str(email.get())
                if ("@" in typed_email and ("." in typed_email and (not typed_email.isspace()))):

                    try :
                        responce = requests.post('http://localhost:5000/patient/add', json={
                            "id" : id,
                            "name" : typed_name,
                            "gender" : typed_gender,
                            "dob" : typed_bod,
                            "phoneNo" : typed_phoneNo,  
                            "address" : typed_address,
                            "email" : typed_email,
                        })

                        if responce.status_code == 200 :
                            messagebox.showinfo(title="Successful!", message="Patient Details are added successfully!")
                            bookingAppointment(frame, id)
                        else: 
                            messagebox.showerror(title="Unsuccessful!", message="Unadle to add Details!")
                    except :
                        messagebox.showwarning(title="Unsuccessful!", message="network error!")

                else :
                    messagebox.showerror(title="Unsuccessful!", message="Email should valid!")
            else :
                messagebox.showerror(title="Unsuccessful!", message="Phone number should valid number!")
        except :
            messagebox.showerror(title="Unsuccessful!", message="Phone number should valid number!")
    else: 
        messagebox.showerror(title="Unsuccessful!", message="Name should have only Alphabets!")

def addNewPatient(frame):
    global name, gender, birth_year, birth_month, birth_day, phoneNo, address, email
    clearFrame(frame)

    years = [i for i in range(1990, 2025)]
    months = [i for i in range(1, 13)]
    days = [i for i in range(1, 32)]

    try :
        newid_responce = requests.get('http://localhost:5000/addnewid')
        if newid_responce.status_code == 200 :
            newid_responce_data = newid_responce.json()
            newId = newid_responce_data['id']

        else :
            messagebox.showwarning(title="Unsuccessful!", message="Unadle to fetch New Id!")    
    except :
        messagebox.showwarning(title="Unsuccessful!", message="network error!")

    tk.Label(frame, text="Name: ").grid(column=0, row=0, padx=30, pady=15)
    name =  tk.Entry(frame, width=50)
    name.grid(column=1, row=0, padx=30, pady=15)

    gender = tk.StringVar()
    tk.Label(frame, text="Gender:").grid(column=0, row=1)
    male_radio = tk.Radiobutton(frame, text="Male", variable=gender, value="M")
    male_radio.grid(column=1, row=1)
    female_radio = tk.Radiobutton(frame, text="Female", variable=gender, value="F")
    female_radio.grid(column=2, row=1)

    tk.Label(frame, text="Date od Birth: ").grid(column=0, row=2, padx=30, pady=15)
    birth_year = tk.StringVar(frame)
    birth_year.set('Select year')
    birth_year_dropdown = tk.OptionMenu(frame, birth_year, *years)
    birth_year_dropdown.grid(row=2, column=1)
    birth_month = tk.StringVar(frame)
    birth_month.set('Select Month')
    birth_month_dropdown = tk.OptionMenu(frame, birth_month, *months)
    birth_month_dropdown.grid(row=2, column=2)
    birth_day = tk.StringVar(frame)
    birth_day.set('Select Day')
    birth_day_dropdown = tk.OptionMenu(frame, birth_day, *days)
    birth_day_dropdown.grid(row=2, column=3)

    tk.Label(frame, text="Phone Number: ").grid(column=0, row=3, padx=30, pady=15)
    phoneNo =  tk.Entry(frame, width=50)
    phoneNo.grid(column=1, row=3, padx=30, pady=15)

    tk.Label(frame, text="Address: ").grid(column=0, row=4, padx=30, pady=15)
    address =  tk.Entry(frame, width=50)
    address.grid(column=1, row=4, padx=30, pady=15)

    tk.Label(frame, text="Email: ").grid(column=0, row=5, padx=30, pady=15)
    email =  tk.Entry(frame, width=50)
    email.grid(column=1, row=5, padx=30, pady=15)

    tk.Button(frame, text="Submit", width=10, command=lambda : addDetails(frame, newId)).grid(column=1, row=6)
