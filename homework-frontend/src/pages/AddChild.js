import React, { useState, useEffect } from 'react';

function AddChild() {
  const [childUsername, setChildUsername] = useState('');
  const [childPassword, setChildPassword] = useState('');
  const [existingParents, setExistingParents] = useState([]);
  const [selectedParent, setSelectedParent] = useState('');
  const [newParentUsername, setNewParentUsername] = useState('');
  const [newParentPassword, setNewParentPassword] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  // Optional: fetch existing parents for the dropdown
  // useEffect(() => {
  //   fetchParents();
  // }, []);

  // const fetchParents = async () => {
  //   try {
  //     const response = await fetch('http://127.0.0.1:8000/users/api/existing-parents/', {
  //       method: 'GET',
  //       credentials: 'include',
  //     });
  //     if (response.ok) {
  //       const data = await response.json();
  //       setExistingParents(data);
  //     } else {
  //       setErrorMsg('Failed to fetch existing parents.');
  //     }
  //   } catch (err) {
  //     console.error(err);
  //     setErrorMsg('Network error.');
  //   }
  // };

  // Submit to create child
  const handleCreateChild = async (e) => {
    e.preventDefault();
    try {
      const response = await fetch('http://127.0.0.1:8000/users/api/create-child/', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        credentials: 'include',
        body: JSON.stringify({
          child_username: childUsername,
          child_password: childPassword,
          selected_parent: selectedParent,
          new_parent_username: newParentUsername,
          new_parent_password: newParentPassword,
        }),
      });
      if (response.ok) {
        alert('Child created successfully!');
        // Reset the form
        setChildUsername('');
        setChildPassword('');
        setNewParentUsername('');
        setNewParentPassword('');
        setSelectedParent('');
      } else {
        const data = await response.json();
        setErrorMsg(data.error || 'Failed to create child.');
      }
    } catch (err) {
      console.error(err);
      setErrorMsg('Network error.');
    }
  };

  return (
    <div className="container mt-4">
      <h1>Add Child</h1>
      {errorMsg && <div className="alert alert-danger">{errorMsg}</div>}
      <form onSubmit={handleCreateChild}>
        <div className="mb-3">
          <label className="form-label">Child Username</label>
          <input
            type="text"
            className="form-control"
            value={childUsername}
            onChange={(e) => setChildUsername(e.target.value)}
            required
          />
        </div>
        <div className="mb-3">
          <label className="form-label">Child Password</label>
          <input
            type="password"
            className="form-control"
            value={childPassword}
            onChange={(e) => setChildPassword(e.target.value)}
            required
          />
        </div>

        <h3>Link to Existing Parent</h3>
        <div className="mb-3">
          <label className="form-label">Select Existing Parent</label>
          <select
            className="form-select"
            value={selectedParent}
            onChange={(e) => setSelectedParent(e.target.value)}
          >
            <option value="">None</option>
            {existingParents.map((parent) => (
              <option key={parent.id} value={parent.id}>
                {parent.username}
              </option>
            ))}
          </select>
        </div>

        <h3>Or Create a New Parent</h3>
        <div className="mb-3">
          <label className="form-label">New Parent Username</label>
          <input
            type="text"
            className="form-control"
            value={newParentUsername}
            onChange={(e) => setNewParentUsername(e.target.value)}
          />
        </div>
        <div className="mb-3">
          <label className="form-label">New Parent Password</label>
          <input
            type="password"
            className="form-control"
            value={newParentPassword}
            onChange={(e) => setNewParentPassword(e.target.value)}
          />
        </div>

        <button type="submit" className="btn btn-primary">Create Child</button>
      </form>
    </div>
  );
}

export default AddChild;
