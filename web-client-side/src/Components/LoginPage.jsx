import React, { useState } from 'react';
import "./LoginPage.css";
import { useNavigate } from 'react-router-dom';

export default function LoginPage() {

  const navigate = useNavigate();

  const [ username, setUsername ] = useState('');
  const [ password, setPassword ] = useState('');

  const handleChangeUsername = (event) => {
    setUsername(event.target.value);
  }

  const handleChangePassword = (event) => {
    setPassword(event.target.value);
  }

  const handleClick = async (e) => {
    e.preventDefault();

    try {
      const responce = await fetch('http://localhost:5000/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          "role" : "patient",
          "username" : username,
          "password" : password
        })
      });

      const responce_data = await responce.json();

      console.log(responce_data['loginSuccess'])

      if  (responce_data['loginSuccess'] === 'True') {
        navigate(`/users/${responce_data['id']}`);
      }
      else {
        document.getElementById('error_login').style.display = "flex";
      }
    } 
    catch (e) {
      console.log(e)
    }
  }

  const handleClose = () => {
    document.getElementById('error_login').style.display = "none";
  }

  return (
    <section id='loginpage'>
      <form id="loginbox">
        <input required type='text' name='login_username' placeholder='Username' value={username} onChange={handleChangeUsername}/>
        <input required type='password' name='login_password' placeholder='Password' value={password} onChange={handleChangePassword}/>
        <button type='submit' onClick={handleClick}>Login</button>
      </form>
      <div className="errorbox" id='error_login'>
        <p>Username or Password is worng!</p>
        <button onClick={handleClose}>Close</button>
      </div>
    </section>
  )
}
