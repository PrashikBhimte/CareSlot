import tkinter as tk
from functions import clearFrame, initFrame, is_aplha_with_space
import requests
from tkinter import messagebox


def updateDetails(frame, id):
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
                    typed_doj = str(joining_year.get()) + ("0" + str(joining_month.get()) if len(str(joining_month.get())) == 1 else str(joining_month.get())) + ("0" + str(joining_day.get()) if len(str(joining_day.get())) == 1 else str(joining_day.get()))
                    typed_qualifictaion = str(qualifictaion.get())
                    typed_designation = str(designation.get())

                    try :
                        responce = requests.post('http://localhost:5000/admin/employee/update_details', json={
                            "id" : id,
                            "name" : typed_name,
                            "gender" : typed_gender,
                            "dob" : typed_bod,
                            "phoneno" : typed_phoneNo,  
                            "address" : typed_address,
                            "email" : typed_email,
                            "doj" : typed_doj,
                            "qualification" : typed_qualifictaion,
                            "designation" : typed_designation
                        })

                        if responce.status_code == 200 :
                            messagebox.showinfo(title="Successful!", message="Personal Details are updated successfully!")
                            initFrame(frame)
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

def fillDetails(frame, res_name):
    global name, gender, birth_year, birth_month, birth_day, phoneNo, address, email, joining_year, joining_month, joining_day, qualifictaion, designation
    clearFrame(frame)

    month_index = {'Jan' : "01", "Feb" : "02", "Mar" : "03", "Apr" : "04", "May" : "05", "Jun" : "06", "Jul" : "07", "Aug" : "08", "Sep" : "09", "Oct" : "10", "Nov" : "11", "Dec" : "12"}

    for  i in responce_data:
        if i['name'] == res_name:
            emp_id = i['id']
            emp_name = i['name']
            emp_gender = i['gender']
            emp_dob = i['dob']
            emp_phoneNo = i['phoneNo']
            emp_address = i['address']
            emp_email = i['email']
            emp_doj = i['doj']
            emp_qualification = i['qualification']
            emp_designation = i['designation']

            years = [i for i in range(1990, 2025)]
            months = [i for i in range(1, 13)]
            days = [i for i in range(1, 32)]

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

            tk.Label(frame, text="Date of joining: ").grid(column=0, row=6, padx=30, pady=15)
            joining_year = tk.StringVar(frame)
            joining_year.set('Select year')
            joining_year_dropdown = tk.OptionMenu(frame, joining_year, *years)
            joining_year_dropdown.grid(row=6, column=1)
            joining_month = tk.StringVar(frame)
            joining_month.set('Select Month')
            joining_month_dropdown = tk.OptionMenu(frame, joining_month, *months)
            joining_month_dropdown.grid(row=6, column=2)
            joining_day = tk.StringVar(frame)
            joining_day.set('Select Day')
            joining_day_dropdown = tk.OptionMenu(frame, joining_day, *days)
            joining_day_dropdown.grid(row=6, column=3)

            tk.Label(frame, text="Qualifictaion: ").grid(column=0, row=7, padx=30, pady=15)
            qualifictaion =  tk.Entry(frame, width=50)
            qualifictaion.grid(column=1, row=7, padx=30, pady=15)

            tk.Label(frame, text="Designation: ").grid(column=0, row=8, padx=30, pady=15)
            designation =  tk.Entry(frame, width=50)
            designation.grid(column=1, row=8, padx=30, pady=15)

            splitted_dob = str(emp_dob).split(" ")
            emp_dob_year = splitted_dob[3]
            emp_dob_month = month_index[splitted_dob[2]]
            emp_dob_day = splitted_dob[1]

            splitted_doj = str(emp_doj).split(" ")
            emp_doj_year = splitted_doj[3]
            emp_doj_month = month_index[splitted_doj[2]]
            emp_doj_day = splitted_doj[1]

            name.insert(0,  emp_name)
            if emp_gender == 'M' :
                male_radio.invoke()
            elif emp_gender == 'F' :
                female_radio.invoke()
            birth_year.set(emp_dob_year)
            birth_month.set(emp_dob_month)
            birth_day.set(emp_dob_day)
            phoneNo.insert(0, str(emp_phoneNo))
            address.insert(0, emp_address)
            email.insert(0, emp_email)
            joining_year.set(emp_doj_year)
            joining_month.set(emp_doj_month)
            joining_day.set(emp_doj_day)
            qualifictaion.insert(0, emp_qualification)
            designation.insert(0, emp_designation)

            tk.Button(frame, text="Submit", width=10, command=lambda : updateDetails(frame, emp_id)).grid(column=1, row=9)

def updateEmployee(frame):
    global responce_data
    clearFrame(frame)

    try :
        responce = requests.get('http://localhost:5000/employees/all')
        if responce.status_code == 200 :
            responce_data = responce.json()
            employee_names = [i['name'] for i in responce_data]

        else :
            messagebox.showwarning(title="Unsuccessful!", message="Unadle to fetch data!")
            initFrame(frame)
    except :
        messagebox.showwarning(title="Unsuccessful!", message="network error!")
        initFrame(frame)

    tk.Label(frame, text="Employee Name: ").grid(column=0, row=2, padx=30, pady=15)
    employeename = tk.StringVar(frame)
    employeename.set('Select Name of Employee')
    employeename_dropdown = tk.OptionMenu(frame, employeename, *employee_names)
    employeename_dropdown.grid(row=2, column=1)
    employeename_dropdown.config(width=30)

    tk.Button(frame, text="Submit", width=10, command=lambda : fillDetails(frame, str(employeename.get()))).grid(column=1, row=9)
