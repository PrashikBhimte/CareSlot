import React from 'react';
import { useNavigate } from 'react-router-dom';

export default function UserNav(props) {

    const userId = props.id;

    const navigate = useNavigate();

    const clickHome = () => {
      navigate(`/users/${userId}`);
    }

    const clickAccount = () => {
        navigate(`/users/${userId}/accountdetails`);
      }
    
      const clickBookAppointment = () => {
        navigate(`/users/${userId}/bookappointment`);
      }
    
      const clickCancelAppointment = () => {
        navigate(`/users/${userId}/cancelappointment`);
      }
    
      const clickHistoryMedication = () => {
        navigate(`/users/${userId}/medicationhistory`);
      }
    
      const clickHistoryAppointment = () => {
        navigate(`/users/${userId}/appointmenthistory`);
      }
    
      const clickDelete = () => {
        navigate(`/users/${userId}/deleteaccount`);
      }

      const clickLogout = () => {
        navigate(`/`);
      } 

  return (
    <div id='useroptions'>
          <button onClick={clickHome}>Home</button>
          <button onClick={clickAccount}>My Account</button>
          <button onClick={clickBookAppointment}>Book Appointment</button>
          <button onClick={clickCancelAppointment}>Cancel Appointment</button>
          <button onClick={clickHistoryMedication}>Veiw Medical History</button>
          <button onClick={clickHistoryAppointment}>Veiw Appointment History</button>
          <button onClick={clickDelete}>Delete My Account</button>
          <button onClick={clickLogout}>Logout</button>
    </div>
  )
}
