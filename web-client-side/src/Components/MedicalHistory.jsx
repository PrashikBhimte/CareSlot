import React, { useEffect, useState } from 'react';
import "./MedicalHistory.css";
import { useNavigate, useParams } from 'react-router-dom';

export default function MedicalHistory() {
    const { userId } = useParams();
    const navigate = useNavigate();

    const [history, setHistory] = useState([]);

    useEffect(() => {
        async function fetchData() {
            try {
                const responce = await fetch("http://localhost:5000/patient/veiw/medication", {
                    method: "POST",
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        "id": userId
                    })
                });

                const responce_data = await responce.json();

                setHistory(responce_data);
            }
            catch (error) {
                console.log(error);
            }
        };
        fetchData();
    }, [userId]);

    const handleClose = () => {
        document.getElementById('apphistoryerror').style.display = 'none';
        navigate(`/users/${userId}`);
    }

    return (
        <div id='appointmenthistory'>
            {history.length !== 0 ?
                <ul id="showhistory">
                    {history.map((key) => { return <li><p>Date : {key['date']}</p> <p>Medication : {key['medication']}</p><p>Advise : {key['advise']}</p><p>Symptoms : {key['symptoms']}</p></li> })}
                </ul> : <div className='errorbox' id='apphistoryerror'>
                    <p>There is no History!</p>
                    <button onClick={handleClose}>Close</button>
                </div>}
        </div>
    )
}
