import React from 'react';
import "./DeleteAccount.css";
import { useNavigate, useParams } from 'react-router-dom';
import UserNav from './UserNav';

export default function DeleteAccount() {

    const navigate = useNavigate();

    const { userId } = useParams();

    const deleteAccount = async (e) => {
        e.preventDefault();

        try {
            const responce = await fetch('http://localhost:5000/patient/delete', {
                method : "POST",
                headers: {
                    'Content-Type': 'application/json'
                },
                body : JSON.stringify({
                    "id" : userId
                })
            });

            const responce_data = responce.json();

            console.log(responce_data['status']);

            navigate(`/`);
        }
        catch (error) {
            console.log(error)
        }
    }

  return (
    <section>
        <UserNav id={userId} />
        <div className="center_div" id='deleteaccount'>
            <h2>Are you sure! you want to Delete Account</h2>
            <p><span>Note : </span>You won't be able to recover the account.</p>
            <button onClick={deleteAccount}>Delete</button>
        </div>
    </section>
  )
}
