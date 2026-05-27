import { useState } from "react";
import { NavLink } from "react-router-dom";
import {
  FaHome,
  FaUpload,
  FaMagic,
  FaChartBar,
  FaCommentDots,
  FaUser,
  FaBars
} from "react-icons/fa";

import "../styles/sidebar.css";

const Sidebar = () => {
  const [open, setOpen] = useState(false);

  return (
    <div className={`sidebar ${open ? "open" : ""}`}>
      {/* Changed to use a proper icon and centering */}
      <div className="toggle-btn" onClick={() => setOpen(!open)}>
        <FaBars style={{ margin: "0 auto" }} />
      </div>

      <nav className="nav-links">
        <NavLink to="/dashboard" className="nav-item">
          <FaHome size={20} />
          {open && <span>Dashboard</span>}
        </NavLink>

        <NavLink to="/upload" className="nav-item">
          <FaUpload size={20} />
          {open && <span>Upload</span>}
        </NavLink>

        <NavLink to="/generate" className="nav-item">
          <FaMagic size={20} />
          {open && <span>Generate</span>}
        </NavLink>

        <NavLink to="/analytics" className="nav-item">
          <FaChartBar size={20} />
          {open && <span>Analytics</span>}
        </NavLink>

        <NavLink to="/feedback" className="nav-item">
          <FaCommentDots size={20} />
          {open && <span>Feedback</span>}
        </NavLink>

        <NavLink to="/profile" className="nav-item">
          <FaUser size={20} />
          {open && <span>Profile</span>}
        </NavLink>
      </nav>
    </div>
  );
};

export default Sidebar;