import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import RegisterTeacher from './pages/RegisterTeacher';
import Login from './pages/Login';
import TeacherDashboard from './pages/TeacherDashboard';
// other imports...

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/register-teacher" element={<RegisterTeacher />} />
        <Route path="/login" element={<Login />} />
        <Route path="/teacher-dashboard" element={<TeacherDashboard />} />
     
      </Routes>
    </Router>
  );
}

//export default App;

// import React, { useState } from 'react';

// function App() {
//   const [date, setDate] = useState('');

//   const handleSubmit = async (e) => {
//     e.preventDefault();
//     try {
//       const response = await fetch('http://127.0.0.1:8000/homework/api/create-daily-homework/', {
//         method: 'POST',
//         headers: {
//           'Content-Type': 'application/json'
//         },
//         credentials: 'include', // to send Django session cookie if you’re logged in
//         body: JSON.stringify({ date })
//       });
//       if (response.ok) {
//         alert('Homework created!');
//       } else {
//         alert('Error creating homework');
//       }
//     } catch (error) {
//       console.error(error);
//       alert('Network error');
//     }
//   };

//   return (
//     <div>
//       <h1>Teacher Create Homework (React)</h1>
//       <form onSubmit={handleSubmit}>
//         <label>Date:</label>
//         <input
//           type="date"
//           value={date}
//           onChange={(e) => setDate(e.target.value)}
//         />
//         <button type="submit">Create</button>
//       </form>
//     </div>
//   );
// }

export default App;

// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

// export default App;
