import React, { useEffect, useState } from 'react';
import "./BookAppointment.css";
import { useNavigate, useParams } from 'react-router-dom';
import UserNav from "./UserNav";

export default function BookAppointment() {

  const navigate = useNavigate();

  const { userId } = useParams();

  const [doctors, setDoctors] = useState([]);
  const [selctedDoctor, setSelectedDocctor] = useState();
  const [doctorDetails, setDoctorDetails] = useState([]);

  const [slots, setSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState();

  const [year, setYear] = useState('2024');
  const [month, setMonth] = useState('Jan');
  const [day, setDay] = useState('01');

  const [doc_id, setDoc_id] = useState(0);
  const [date, setDate] = useState();

  const years = [];
  for (let year = 2024; year <= 2024; year++) {
    years.push(year);
  }
  const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
  const days = [];
  for (let day = 1; day <= 31; day++) {
    days.push(day);
  }

  useEffect(() => {
    const fetchAllDoctors = async () => {
      try {
        const responce = await fetch('http://localhost:5000/doctor/all', {
          method: "GET",
          headers: {
            'Content-Type': 'application/json'
          }
        });

        const responce_data = await responce.json();
        setDoctors(await responce_data.map((key) => { return key['name'] }));
        setDoctorDetails(await responce_data);
        setSelectedDocctor(await responce_data[0]['name']);
      }
      catch (error) {
        console.log(error);
      }
    }

    fetchAllDoctors();
  }, [userId]);

  const changeDoctorname = (event) => {
    setSelectedDocctor(event.target.value);
  }

  const changeSlot = (event) => {
    setSelectedSlot(event.target.value);
  }

  const changeYear = (event) => {
    setYear(event.target.value);
  }
  const changeMonth = (event) => {
    setMonth(event.target.value);
  }
  const changeDay = (event) => {
    if (event.target.value.length === 1) {
      setDay("0" + event.target.value);
    }
    else {
      setDay(event.target.value);
    }
  }

  useEffect(() => {
    if (doctorDetails) {
      if (selctedDoctor) {
        const months_value = {
          'Jan': "01",
          "Feb": "02",
          "Mar": "03",
          "Apr": "04",
          "May": "05",
          "Jun": "06",
          "Jul": "07",
          "Aug": "08",
          "Sep": "09",
          "Oct": "10",
          "Nov": "11",
          "Dec": "12"
        }
        let doctor_id = 0;
        doctorDetails.map((key) => {
          if (key['name'] === selctedDoctor) {
            doctor_id = key['id'];
            setDoc_id(doctor_id);
          }
          return 0;
        })
        const date_var = year + months_value[month] + day;
        setDate(date_var);

        const fetchSlots = async () => {

          try {
            const responce = await fetch('http://localhost:5000/patient/view/availableslots', {
              method: "POST",
              headers: {
                'Content-Type': 'application/json'
              },
              body: JSON.stringify({
                "date": date_var,
                "doc_id": doctor_id
              })
            });

            const responce_data = await responce.json();
            setSlots(await responce_data['available_slots']);
            setSelectedSlot(await responce_data['available_slots'][0]);
          }
          catch (error) {
            console.log(error)
          }
        }

        fetchSlots();
      }
    }

  }, [year, month, day, selctedDoctor, doctorDetails]);


  const bookAppointment = async () => {
    try {
      const responce = await fetch('http://localhost:5000/patient/appiontment/book', {
        method: "POST",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "date": date,
          "doc_id": doc_id,
          "pat_id": userId,
          "time_slot": selectedSlot
        })
      });

      if (responce.status === 200) {
        alert("Appointment is book");
        navigate(`/users/${userId}`);
      }
    }
    catch (error) {
      console.log(error)
    }
  }

  return (
    <section id='bookappointment'>
      <UserNav id={userId} />
      <div className='center_div'>
        <label>Doctor :
          <select onChange={changeDoctorname} value={selctedDoctor}>
            {doctors.map((doctor) => { return <option key={doctor} value={doctor}>{doctor}</option> })}
          </select>
        </label>
        <label>
          Date :
          <div>
            <select value={year} onChange={changeYear}>
              {years.map((key) => { return <option key={key} value={key}>{key}</option> })}
            </select>
            <select value={month} onChange={changeMonth}>
              {months.map((key) => { return <option key={key} value={key}>{key}</option> })}
            </select>
            <select value={day} onChange={changeDay}>
              {days.map((key) => { return <option key={key} value={key}>{key}</option> })}
            </select>
          </div>
        </label>
        <label>Time Slot :
          <select onChange={changeSlot} value={selectedSlot}>
            {slots.map((slot) => { return <option key={slot} value={slot}>{slot}</option> })}
          </select>
        </label>
        <button onClick={bookAppointment}>Book Appointment</button>
      </div>
    </section>
  )
}
