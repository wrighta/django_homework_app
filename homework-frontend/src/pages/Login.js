import React, { useState } from 'react';

function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/users/api/login/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({ username, password })
      });

      if (response.ok) {
        // The backend can return JSON containing the user's role or a redirect URL.
        const data = await response.json();
        const userRole = data.role;

        // Option A: The backend might directly tell you where to go next:
        // e.g., data might be { role: "teacher", redirectUrl: "/teacher-dashboard" }
        // If so, you can:
        // window.location.href = data.redirectUrl;

        // Option B: You switch on the user role yourself:
        if (userRole === 'teacher') {
          window.location.href = '/teacher-dashboard';
        } else if (userRole === 'parent') {
          window.location.href = '/parent-dashboard';
        } else if (userRole === 'child') {
          window.location.href = '/child-dashboard';
        } else {
          // fallback if unknown role
          alert('Unknown user role!');
        }

      } else {
        const data = await response.json();
        setErrorMsg(data.error || 'Login failed.');
      }
    } catch (err) {
      console.error(err);
      setErrorMsg('Network error in Login.js.');
    }
  };

  return (
    <div className="container mt-5">
      <h2>Login</h2>
      {errorMsg && <div className="alert alert-danger">{errorMsg}</div>}
      <form onSubmit={handleSubmit}>
        <div className="mb-3">
          <label className="form-label">Username</label>
          <input
            type="text"
            className="form-control"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
          />
        </div>

        <div className="mb-3">
          <label className="form-label">Password</label>
          <input
            type="password"
            className="form-control"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
          />
        </div>

        <button type="submit" className="btn btn-primary">Log In</button>
      </form>
    </div>
  );
}

export default Login;
