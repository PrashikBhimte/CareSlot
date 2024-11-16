import tkinter as tk
from functions import clearFrame
import requests
from tkinter import messagebox

def postDetails(frame, id, date):

    typed_medication = str(medication.get())
    typed_advise = str(advise.get())
    typed_symptoms = str(symptoms.get())

    try :
        responce = requests.post('http://localhost:5000/doctor/addmedication', json={
            "id" : id,
            "date" : date,
            "medication" : typed_medication,
            "advise" : typed_advise,  
            "symptoms" : typed_symptoms
        })

        if responce.status_code == 200 :
            messagebox.showinfo(title="Successful!", message="Mediaction Details are added successfully!")
            clearFrame(frame)
        else :
            messagebox.showerror(title="Unsuccessful!", message="unable to add data!")
    except :
        messagebox.showwarning(title="Unsuccessful!", message="network error!")
    



def addMedication(frame, id, date):
    global medication, advise, symptoms
    clearFrame(frame)

    tk.Label(frame, text="Medication: ").grid(column=0, row=0, padx=30, pady=15)
    medication =  tk.Entry(frame, width=50)
    medication.grid(column=1, row=0, padx=30, pady=15)

    tk.Label(frame, text="Advise: ").grid(column=0, row=1, padx=30, pady=15)
    advise =  tk.Entry(frame, width=50)
    advise.grid(column=1, row=1, padx=30, pady=15)

    tk.Label(frame, text="Symptoms: ").grid(column=0, row=2, padx=30, pady=15)
    symptoms =  tk.Entry(frame, width=50)
    symptoms.grid(column=1, row=2, padx=30, pady=15)

    tk.Button(frame, text="Submit", width=10, command=lambda : postDetails(frame, id, date)).grid(column=1, row=3)