// src/App.jsx
import { Routes, Route, Navigate } from "react-router-dom";

import Sidebar from "./components/Sidebar";
import ProtectedRoute from "./components/ProtectedRoute";

import Home from "./pages/Home";        // ✅ Added
import Dashboard from "./pages/Dashboard";
import UploadContent from "./pages/UploadContent";
import Generate from "./pages/Generate";
import Analytics from "./pages/Analytics";
import Feedback from "./pages/Feedback";
import Login from "./pages/Login";
import Register from "./pages/Register";
import Profile from "./pages/Profile";

import "./styles/main.css";

function App() {
  return (
    <Routes>

      {/* Public Routes */}
      <Route path="/" element={<Home />} />   {/* ✅ Home page */}
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<Register />} />

      {/* Protected Routes */}
      <Route
        path="/*"
        element={
          <ProtectedRoute>
            <div className="app-container">
              <Sidebar />

              <div className="main-content">
                <Routes>
                  <Route path="/dashboard" element={<Dashboard />} />
                  <Route path="/upload" element={<UploadContent />} />
                  <Route path="/generate" element={<Generate />} />
                  <Route path="/analytics" element={<Analytics />} />
                  <Route path="/feedback" element={<Feedback />} />
                  <Route path="/profile" element={<Profile />} />
                </Routes>
              </div>
            </div>
          </ProtectedRoute>
        }
      />

    </Routes>
  );
}

export default App;