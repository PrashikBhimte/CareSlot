import React, { useEffect, useState } from 'react';
import "./PersonalDetails.css";
import { useNavigate, useParams } from 'react-router-dom';

export default function PersonalDetails() {


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
  
    const changeName = (event) => {
        setName(event.target.value);
    }

    const changeGender = (event) => {
        setGender(event.target.value);
    }

    const changeAddress = (event) => {
        setAddress(event.target.value);
    }

    const changeEmail = (event) => {
        setEmail(event.target.value);
    }

    const changeDob = () => {
        setDob(year + month + day);
        console.log(year + month + day)
    }

    const changeYear = (event) => {
        setYear(event.target.value);
        changeDob();
    }
    const changeMonth = (event) => {
        setMonth(event.target.value);
        changeDob();
    }
    const changeDay = (event) => {
        setDay(event.target.value);
        changeDob();
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

    const months_value = {
        'Jan' : "01",
        "Feb" : "02",
        "Mar" : "03",
        "Apr" : "04",
        "May" : "05",
        "Jun" : "06",
        "Jul" : "07",
        "Aug" : "08",
        "Sep" : "09",
        "Oct" : "10",
        "Nov" : "11",
        "Dec" : "12"
    }

    const submit = async (e) => {
        e.preventDefault();
        changeDob();

        try {
            const responce = await fetch('http://localhost:5000/patient/add', {
                method : "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body : JSON.stringify({
                    "id" : userId,
                    "name" : name,
                    "gender" : gender,
                    "dob" : year + months_value[month] + day,
                    "phoneNo" : phoneNo,
                    "address" : address,
                    "email" : email
                })
            });

            const responce_data = responce.json();

            console.log(responce_data['status']);

            navigate(`/users/${userId}`);
        }
        catch (error) {
            console.log(error)
        }
    }

  return (
    <section id='personaldetails'>
        <form id='personaldetailsform' >
            <label>
                Name : <input type='text' value={name} name='name' onChange={changeName} required/>
            </label>
            <label>
                Gender: <div>
                    <input required className='gender_input' type='radio' name='gender' value='M' onChange={changeGender} checked={gender === 'M'} /><label>Male</label>
                    <input required className='gender_input' type='radio' name='gender' value='F' onChange={changeGender} checked={gender === 'F'} /><label>Felmale</label>
                </div>
            </label>
            <label>
                Date of Birth : 
                <div>
                    <select value={year} onChange={changeYear}>
                        {years.map((key) => { return <option  value={key}>{key}</option> })}
                    </select>
                    <select value={month} onChange={changeMonth}>
                        {months.map((key) => { return <option value={key}>{key}</option> })}
                    </select>
                    <select value={day} onChange={changeDay}>
                        {days.map((key) => { return <option value={key}>{key}</option> })}
                    </select>
                </div>
            </label>
            <label>
                Phone Number : <input required type='number' name='phoneNo' min={1000000000} max={9999999999} value={phoneNo} />
            </label>
            <label>
                Address : <textarea required type='text' name='address' value={address} onChange={changeAddress} />
            </label>
            <label>
                Email : <input required type='email' name='email' value={email} onChange={changeEmail}/>
            </label>
            <button type='submit' onClick={submit}>Update</button>
        </form>
    </section>
  )
}
