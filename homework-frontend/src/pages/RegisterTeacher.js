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
        // 'credentials: "include"' ensures cookies (the session cookie)
        // are included in the request, so Django can set a session if it wants.
        credentials: 'include',
        body: JSON.stringify({
          username,
          email,
          password
        }),
      });

      if (response.ok) {
        // If the response is 201 or 200, it means success
        // The user is now logged in (session cookie is set)
        // We can redirect them to the teacher dashboard
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
    <div>
      <h2>Register as a Teacher</h2>
      {errorMsg && <p style={{ color: 'red' }}>{errorMsg}</p>}
      <form onSubmit={handleSubmit}>
        <div>
          <label>Username:</label>
          <input
            type="text"
            value={username}
            onChange={e => setUsername(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Email:</label>
          <input
            type="email"
            value={email}
            onChange={e => setEmail(e.target.value)}
            required
          />
        </div>

        <div>
          <label>Password:</label>
          <input
            type="password"
            value={password}
            onChange={e => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit">Register</button>
      </form>
    </div>
  );
}

export default RegisterTeacher;
