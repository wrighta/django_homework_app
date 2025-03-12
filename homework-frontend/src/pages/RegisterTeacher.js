import React, { useState } from 'react';

function RegisterTeacher() {
  // Local component state to hold form data:
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  // This function runs when the user presses "Register"
  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      // We do a POST request to our Django endpoint:
      const response = await fetch('http://127.0.0.1:8000/users/api/register-teacher/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          username,
          email,
          password
        }),
      });

      if (response.ok) {
        // If the response is 201 or 200, it means success.
        // The user is now logged in (session cookie set).
        // We can redirect them to the Teacher Dashboard.
        window.location.href = '/teacher-dashboard';
      } else {
        // If there's an error, parse the JSON and display it
        const data = await response.json();
        setErrorMsg(JSON.stringify(data));
      }
    } catch (err) {
      console.error(err);
      setErrorMsg('Network error. Check console.');
    }
  };

  return (
    <div className="container mt-5" style={{ maxWidth: '600px' }}>
      <h2 className="mb-4">Register as a Teacher</h2>
      {errorMsg && <div className="alert alert-danger">{errorMsg}</div>}

      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Username:</label>
          <input
            type="text"
            className="form-control"
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Email:</label>
          <input
            type="email"
            className="form-control"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Password:</label>
          <input
            type="password"
            className="form-control"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="btn btn-primary">Register</button>
      </form>
    </div>
  );
}

export default RegisterTeacher;
