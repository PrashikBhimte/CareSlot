import React, { useState } from 'react';
import "./SignupPage.css";
import { useNavigate } from 'react-router-dom';

export default function SignupPage() {

    const naviagte = useNavigate();

    const [ phoneNo, setPhoneNo ] = useState();
    const [ otp, setOtp ] = useState();
    const [ username, setUsername ] = useState();
    const [ password, setPassword ] = useState(); 

    const [ message, setMessage ] = useState();

    const handelChangePhoneNo = (event) => {
        setPhoneNo(event.target.value);
    }
    const handleChangeOtp = (event) => {
        setOtp(event.target.value);
    }
    const handleChangeUsername = (event) => {
        setUsername(event.target.value);
    }
    const handleChangePassword = (event) => {
        setPassword(event.target.value);
    }

    const sendOtp = async (e) => {
        if (phoneNo) {
            e.preventDefault();

            try {
                const responce = await fetch('http://localhost:5000/signup', {
                    method : "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body : JSON.stringify({
                        "phoneNo" : phoneNo
                    })
                });
                const responce_data = await responce.json();
                console.log(responce_data);

                document.getElementById('verifyotp').style.display = 'flex';
            }
            catch (error) {
                console.log(error)
            }
        }
    }

    const handleVerify = async (e) => {
        e.preventDefault();

        try {
            const responce = await fetch('http://localhost:5000/signup/otp', {
                method : "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body : JSON.stringify({
                    "phoneNo" : phoneNo,
                    "otp" : otp
                })
            });
            const responce_data = await responce.json();
            console.log(responce_data['status']);

            if (responce_data['status'] === "sucessfully!") {
                document.getElementById('signupformotp').style.display = 'none';
                document.getElementById('signupformuser').style.display = 'flex';
            }
            else if (responce_data['status'] === 'wrong otp!') {
                document.getElementById('error_signup').style.display = 'flex';
                setMessage('Worng OTP!');
            }
            else if (responce_data['status' === 'time out!']) {
                document.getElementById('error_signup').style.display = 'flex';
                setMessage('Time is out!');
            }
        }
        catch (error) {
            console.log(error)
        }
    }

    const handleClose = (e) => {
        e.preventDefault();
        document.getElementById('signupformotp').style.display = 'flex';
        document.getElementById('signupformuser').style.display = 'none';
        document.getElementById('error_signup').style.display = 'none';
    }

    const handleClick = async (e) => {
        e.preventDefault();

        try {
            const responce = await fetch('http://localhost:5000/signup/details', {
                method : "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body : JSON.stringify({
                    "phoneNo" : phoneNo,
                    "username" : username,
                    "password" : password
                })
            });
            const responce_data = await responce.json();

            if (responce_data['error'] === "Username allready exits!") {
                document.getElementById('username_error').style.display = 'flex';
            }
        
            console.log(responce_data);
            naviagte(`/users/${responce_data['id']}/personaldetails`);
        }
        catch (error) {
            console.log(error)
        }
    }

    const handleCloseUsernameError = (e) => {
        e.preventDefault();
        document.getElementById('username_error').style.display = "none";
        document.getElementById('verifyotp').style.display = 'none';
    }


  return (
    <section id='signpage'>
        <form id='signupformotp'>
            <input required type='number' min={1000000000} max={9999999999} name='signpu_phoneno' placeholder='Phone Number' value={phoneNo} onChange={handelChangePhoneNo}/>
            <button onClick={sendOtp} type='submit'>Send OTP</button>
            <div id="verifyotp">
                <input required type='text' name='signup_otp' placeholder='OTP' value={otp} onChange={handleChangeOtp} />
                <button onClick={handleVerify}>Verify</button>
            </div>
        </form>
        <div className="errorbox" id='error_signup'>
            <p>{message}</p>
            <button onClick={handleClose}>Close</button>
        </div>
        <form id="signupformuser">
            <input required type='text' name='signup_username' placeholder='Username' value={username} onChange={handleChangeUsername}/>
            <input required type='password' name='signup_password' placeholder='Password' value={password} onChange={handleChangePassword}/>
            <button type='submit' onClick={handleClick}>Signup</button>
        </form>
        <div className="errorbox" id='username_error'>
            <p>Username already exits...</p>
            <button onClick={handleCloseUsernameError}>Close</button>
        </div>
    </section>
  )
}
