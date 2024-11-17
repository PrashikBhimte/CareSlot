import './App.css';
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from './Components/LoginPage';
import UserHome from './Components/UserHome';
import SignupPage from './Components/SignupPage';
import PersonalDetails from './Components/PersonalDetails';
import HomePage from './Components/HomePage';
import UserAccount from './Components/UserAccount';
import DeleteAccount from './Components/DeleteAccount';
import AppointmentHistory from './Components/AppointmentHistory';
import BookAppointment from './Components/BookAppointment';
import MedicalHistory from './Components/MedicalHistory';
import CancelAppointment from './Components/CancelAppointment';

function App() {
  return (
    <Routes>
      <Route path='/' element={<HomePage />} />
      <Route path='/signup' element={<SignupPage />} />
      <Route path='/login' element={<LoginPage />} />
      <Route path='*' element={<Navigate to='/' replace />} />
      <Route path='/users/:userId' element={<UserHome />} />
      <Route path='/users/:userId/personaldetails' element={<PersonalDetails />} />
      <Route path='/users/:userId/accountdetails' element={<UserAccount />} />
      <Route path='/users/:userId/deleteaccount' element={<DeleteAccount />} />
      <Route path='/users/:userId/appointmenthistory' element={<AppointmentHistory />} />
      <Route path='/users/:userId/medicationhistory' element={<MedicalHistory />} />
      <Route path='/users/:userId/bookappointment' element={<BookAppointment />} />
      <Route path='/users/:userId/cancelappointment' element={<CancelAppointment />} />
    </Routes>
  );
}

export default App;
