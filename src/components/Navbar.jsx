//Navbar.jsx
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <h2>AI Question Generator</h2>
      <Link to="/">Home</Link>
    </nav>
  );
}

export default Navbar;
