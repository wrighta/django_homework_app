import React from 'react';
import { Link } from 'react-router-dom'; // if using react-router

function LandingPage() {
  return (
    <div>
      <h1>Welcome to the Homework Tracker</h1>
      <p>Track and manage homework with ease!</p>
      <Link to="/register-teacher">Register as a Teacher</Link>
      <Link to="/login">Login</Link>
    </div>
  );
}

export default LandingPage;
