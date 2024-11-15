import React, { useState, useEffect } from 'react';
import "./UserAccount.css";
import { useNavigate, useParams } from 'react-router-dom';

export default function UserAccount() {

    const { userId } = useParams();

    const navigate = useNavigate();

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

  const handleClick = () => {
    navigate(`/users/${userId}/personaldetails`);
  }

  return (
    <div id='useraccount'>
        <div id='useraccdetails' >
            <p><span>Name : </span>{name}</p>
            <p><span>Gender : </span>{gender}</p>
            <p><span>Date of Birth : </span>{dob}</p>
            <p><span>Phone Number : </span>{phoneNo}</p>
            <p><span>Address : </span>{address}</p>
            <p><span>Email : </span>{email}</p>
            <button onClick={handleClick}>Edit</button>
        </div>
    </div>
  )
}
