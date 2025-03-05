import React, { useState, useEffect } from 'react';

function TeacherDashboard() {
  const [childUsername, setChildUsername] = useState('');
  const [childPassword, setChildPassword] = useState('');
  const [parentUsername, setParentUsername] = useState('');
  const [parentPassword, setParentPassword] = useState('');
  const [selectedParent, setSelectedParent] = useState('');
  const [existingParents, setExistingParents] = useState([]);
  const [errorMsg, setErrorMsg] = useState('');

  // Fetch existing parents when the component mounts
  useEffect(() => {
    fetchExistingParents();
  }, []);

  // Fetch existing parents from the backend
  const fetchExistingParents = async () => {
    try {
      const response = await fetch('http://127.0.0.1:8000/users/api/existing-parents/', {
        method: 'GET',
        credentials: 'include',
      });
      if (response.ok) {
        const data = await response.json();
        setExistingParents(data);
      } else {
        setErrorMsg('Failed to fetch existing parents.');
      }
    } catch (err) {
      console.error(err);
      setErrorMsg('Network error. Check console.');
    }
  };

  // Handle child user creation
  const handleCreateChild = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch('http://127.0.0.1:8000/users/api/create-child/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          child_username: childUsername,
          child_password: childPassword,
          parent_username: parentUsername,
          parent_password: parentPassword,
          selected_parent: selectedParent,
        }),
      });

      if (response.ok) {
        alert('Child user created successfully!');
        setChildUsername('');
        setChildPassword('');
        setParentUsername('');
        setParentPassword('');
        setSelectedParent('');
      } else {
        const data = await response.json();
        setErrorMsg(data.error || 'Failed to create child user.');
      }
    } catch (err) {
      console.error(err);
      setErrorMsg('Network error. Check console.');
    }
  };

  return (
    <div>
      <h1>Teacher Dashboard</h1>
      <p>You are now logged in as a Teacher!</p>

      <h2>Create Child User</h2>
      {errorMsg && <p style={{ color: 'red' }}>{errorMsg}</p>}
      <form onSubmit={handleCreateChild}>
        <div>
          <label>Child Username:</label>
          <input
            type="text"
            value={childUsername}
            onChange={(e) => setChildUsername(e.target.value)}
            required
          />
        </div>
        <div>
          <label>Child Password:</label>
          <input
            type="password"
            value={childPassword}
            onChange={(e) => setChildPassword(e.target.value)}
            required
          />
        </div>

        <h3>Link to Parent</h3>
        <div>
          <label>Create New Parent:</label>
          <input
            type="text"
            value={parentUsername}
            onChange={(e) => setParentUsername(e.target.value)}
            placeholder="Parent Username"
          />
          <input
            type="password"
            value={parentPassword}
            onChange={(e) => setParentPassword(e.target.value)}
            placeholder="Parent Password"
          />
        </div>
        <div>
          <label>Or Select Existing Parent:</label>
          <select
            value={selectedParent}
            onChange={(e) => setSelectedParent(e.target.value)}
          >
            <option value="">Select a parent</option>
            {existingParents.map((parent) => (
              <option key={parent.id} value={parent.id}>
                {parent.username}
              </option>
            ))}
          </select>
        </div>

        <button type="submit">Create Child User</button>
      </form>
    </div>
  );
}

export default TeacherDashboard;