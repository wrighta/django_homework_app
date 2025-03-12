import React from 'react';
import { Link } from 'react-router-dom';

function LandingPage() {
  return (
    <div className="container d-flex flex-column align-items-center justify-content-center mt-5">
      <h1 className="mb-4">Welcome to the Homework Tracker</h1>
      <p className="mb-4 text-center">Track and manage homework with ease!</p>

      <div>
        <Link to="/register-teacher" className="btn btn-primary me-3">
          Register as a Teacher
        </Link>
        <Link to="/login" className="btn btn-secondary">
          Login
        </Link>
      </div>
    </div>
  );
}

export default LandingPage;
