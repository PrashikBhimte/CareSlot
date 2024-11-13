import './App.css';
import { Routes, Route, Navigate } from "react-router-dom";
import LoginPage from './Components/LoginPage';
import UserHome from './Components/UserHome';
import SignupPage from './Components/SignupPage';
import PersonalDetails from './Components/PersonalDetails';

function App() {
  return (
    <Routes>
      <Route path='/signup' element={<SignupPage />} />
      <Route path='/login' element={<LoginPage />} />
      <Route path='*' element={<Navigate to='/' replace />} />
      <Route path='/users/:userId' element={<UserHome />} />
      <Route path='/users/:userId/personaldetails' element={<PersonalDetails />} />
    </Routes>
  );
}

export default App;
