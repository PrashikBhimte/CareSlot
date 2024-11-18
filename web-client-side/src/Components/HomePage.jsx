import React from 'react';
import "./HomePage.css";
import { useNavigate } from 'react-router-dom';

export default function HomePage() {

    const navigate = useNavigate();

    const handleLogin = () => {
        navigate('/login');
    }

    const handlesignup = () => {
        navigate('signup')
    }

  return (
    <section id='homepage'>
        <div id="navbar">
            <p>CareSLOT</p>
            <div>
                <button onClick={handleLogin} >Login</button>
                <button onClick={handlesignup} >Signup</button>
            </div>
        </div>
        <div id="homepage_contain">
            <h1>Welcome To The CareSlot!</h1>
            <p>Seamless Appointment Booking Platform.</p>
        </div>
    </section>
  )
}
