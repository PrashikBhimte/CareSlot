import React, { useState, useEffect } from 'react';
import "./UserHome.css";
import { useNavigate, useParams } from 'react-router-dom';

export default function UserHome() {

  const navigate = useNavigate();

    const { userId } = useParams();

    const [ name, setName ] = useState();
    const [ gender, setGender ] = useState();
    const [ dob, setDob ] = useState();
    const [ phoneNo, setPhoneNo ] = useState();
    const [ address, setAddress ] = useState();
    const [ email, setEmail ] = useState();

    const [ year, setYear ] = useState();
    const [ month, setMonth ] = useState()
    const [ day, setDay ] = useState();

    const years = [];
    for (let year = 1990; year <= 2024; year++) {
        years.push(year);
    }
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const days = [];
    for (let day = 1; day <=31; day++) {
        days.push(day);
    }

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
              setGender(responce_data['gender']);
              setDob(responce_data['dob']);
              const x = responce_data['dob'].split(" ")
              setYear(x[3]);
              setDay(x[1]);
              setMonth(x[2]);
              setPhoneNo(responce_data['phoneNo']);
              setAddress(responce_data['address']);
              setEmail(responce_data['email']);

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

  const clickHistoryAppointment = () => {
    navigate(`/user/${userId}/appointmenthistory`);
  }

  const clickDelete = () => {
    navigate(`/users/${userId}/deleteaccount`);
  }

    return (
    <div id='userhome'>
        <h1>Hello {name} </h1>
        <div id='useroptions'>
          <button onClick={clickAccount}>My Account</button>
          <button>Book Appointment</button>
          <button>Veiw Medical History</button>
          <button onClick={clickHistoryAppointment}>Veiw Appointment History</button>
          <button onClick={clickDelete}>Delete My Account</button>
        </div>
    </div>
  )
}
