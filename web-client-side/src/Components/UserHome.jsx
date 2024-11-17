import React, { useState, useEffect } from 'react';
import "./UserHome.css";
import { useNavigate, useParams } from 'react-router-dom';

export default function UserHome() {

  const navigate = useNavigate();

    const { userId } = useParams();

    const [ name, setName ] = useState();

    useEffect( () => {
      async function fetchData() {
          try {
              const responce = await fetch("http://localhost:5000/patient/veiw/personal", {
                  method : "POST",
                  headers: {
                      'Content-Type': 'application/json'
                  },
                  body : JSON.stringify({
                      "id" : userId
                  })
              });

              const responce_data = await responce.json();

              setName(responce_data['name']);

          }
          catch (error) {
              console.log(error);
          }
      };
      fetchData();
  }, [userId]);

  const clickAccount = () => {
    navigate(`/users/${userId}/accountdetails`);
  }

  const clickBookAppointment = () => {
    navigate(`/users/${userId}/bookappointment`);
  }

  const clickCancelAppointment = () => {
    navigate(`/users/${userId}/cancelappointment`);
  }

  const clickHistoryMedication = () => {
    navigate(`/users/${userId}/medicationhistory`);
  }

  const clickHistoryAppointment = () => {
    navigate(`/users/${userId}/appointmenthistory`);
  }

  const clickDelete = () => {
    navigate(`/users/${userId}/deleteaccount`);
  }

    return (
    <div id='userhome'>
        <h1>Hello {name} </h1>
        <div id='useroptions'>
          <button onClick={clickAccount}>My Account</button>
          <button onClick={clickBookAppointment}>Book Appointment</button>
          <button onClick={clickCancelAppointment}>Cancel Appointment</button>
          <button onClick={clickHistoryMedication}>Veiw Medical History</button>
          <button onClick={clickHistoryAppointment}>Veiw Appointment History</button>
          <button onClick={clickDelete}>Delete My Account</button>
        </div>
    </div>
  )
}
