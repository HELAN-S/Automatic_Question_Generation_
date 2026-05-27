import { useEffect, useState } from "react";
import api from "../services/api";
import "../styles/profile.css";

function Profile() {
  const [user, setUser] = useState(null);

  useEffect(() => {
    const token = localStorage.getItem("token");

    api.get("/profile/me", {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => setUser(res.data))
    .catch(err => {
      console.error(err);
      alert("Unauthorized. Please login again.");
    });
  }, []);

  if (!user) return <p className="loading">Loading...</p>;

  const initial = user.name.charAt(0).toUpperCase();

// ... imports stay the same

  return (
    <div className="profile-page">
      <div className="profile-header">
        <button
          className="logout-btn"
          onClick={() => {
            localStorage.removeItem("token");
            window.location.href = "/login";
          }}
        >
          Logout
        </button>
        <div className="avatar">{initial}</div>
        <div className="user-info">
          <h2>{user.name}</h2>
          <p>{user.email}</p>
        </div>
      </div>

      <div className="profile-body">
        <div className="profile-section">
          <h3>Account Information</h3>
          <div className="info-card">
            <div className="info-row">
              <span className="info-label">Full Name</span>
              <span className="info-value">{user.name}</span>
            </div>
            <div className="info-row">
              <span className="info-label">Email Address</span>
              <span className="info-value">{user.email}</span>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Profile;