//home.jsx
import { Link } from "react-router-dom";
import "../styles/home.css";

export default function Home() {
  return (
    <div className="home-container">

      <div className="overlay">

        <h1 className="title">
          Automatic Question Generation System
        </h1>

        <p className="subtitle">
          
        </p>

        <div className="buttons">

          <Link to="/login" className="btn login-btn">
            Login
          </Link>

          <Link to="/register" className="btn register-btn">
            Register
          </Link>

        </div>

      </div>

    </div>
  );
}