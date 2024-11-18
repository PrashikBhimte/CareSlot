import React, { useEffect, useState } from 'react';
import "./CancelAppointment.css";
import { useNavigate, useParams } from 'react-router-dom';
import UseNav from "./UserNav";

export default function CancelAppointment() {

  const navigate = useNavigate();

  const { userId } = useParams();

  const [dates, setDates] = useState([]);
  const [selectedDate, setSelectedDate] = useState();
  const [appointmentDetails, setAppointmentDetails] = useState([]);
  const [slots, setSlots] = useState([]);
  const [selectedSlot, setSelectedSlot] = useState();

  useEffect(() => {
    const fetchAllAppointment = async () => {
      try {
        const responce = await fetch('http://localhost:5000/patient/view/appointment/cancel', {
          method: "POST",
          headers: {
            'Content-Type': 'application/json'
          },
          body: JSON.stringify({
            "pat_id": userId
          })
        });

        const responce_data = await responce.json();
        setDates([...new Set(responce_data.map((key) => { return key['date'] }))]);
        setAppointmentDetails(responce_data);
        setSelectedDate(responce_data[0]['date']);
      }
      catch (error) {
        console.log(error);
      }
    }

    fetchAllAppointment();
  }, [userId]);

  useEffect(() => {
    let slots = [];
    appointmentDetails.map((key) => {
      if (key['date'] === selectedDate) {
        slots.push(key['time_slot']);
      }
      return 0;
    });
    setSlots(slots);
    setSelectedSlot(slots[0]);
  }, [selectedDate, appointmentDetails]);

  const onChangeDate = (event) => {
    setSelectedDate(event.target.value);
  }

  const onChangeSlot = (event) => {
    setSelectedSlot(event.target.value);
  }

  const cancelAppointment = async () => {
    let app_id = 0;
    appointmentDetails.map((key) => {
      if (key['date'] === selectedDate) {
        if (key['time_slot'] === selectedSlot) {
          app_id = key['app_id']
        }
      }
      return 0;
    });

    try {
      const responce = await fetch('http://localhost:5000/patient/appiontment/cancel', {
        method: "DELETE",
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "app_id": app_id
        })
      });

      const responce_data = responce.json();

      console.log(responce_data['status']);

      alert("Appointment is Canceled");
      navigate(`/users/${userId}`);
    }
    catch (error) {
      console.log(error)
    }
  }

  return (
    <section>
      <UseNav id={userId} />
      <div className='center_div'>
        {dates.length !== 0 ? <label>Date :
          <select onChange={onChangeDate} value={selectedDate}>
            {dates.map((date) => { return <option key={date} value={date}>{date}</option> })}
          </select>
        </label> : <h1>No data</h1>}
        {slots.length !== 0 ? <label>Time Slot :
          <select onChange={onChangeSlot} value={selectedSlot}>
            {slots.map((slot) => { return <option key={slot} value={slot}>{slot}</option> })}
          </select>
        </label> : <h1>No data</h1>}
        <button onClick={cancelAppointment}>Cancel Appointment</button>
      </div>
    </section>
  )
}
