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
    <div id='homepage'>
        <div id="navbar">
            <button onClick={handleLogin} >Login</button>
            <button onClick={handlesignup} >Signup</button>
        </div>
    </div>
  )
}
