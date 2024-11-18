import React, { useState, useEffect } from 'react';
import "./UserHome.css";
import { useNavigate, useParams } from 'react-router-dom';
import UserNav from './UserNav';

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

    return (
    <section id='userhome'>
        <h1>Hello {name} </h1>
        <UserNav id={userId} />
    </section>
  )
}
