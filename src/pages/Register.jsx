import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Register() {
  const navigate = useNavigate();

  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleRegister = async (e) => {
    e.preventDefault();

    try {
      await api.post("/auth/register", { name, email, password });
      navigate("/login");
    } catch (err) {
      alert(err.response?.data?.detail || "Registration failed");
    }
  };

  const styles = {
    page: {
      height: "100vh",
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      background: "#fff",
      fontFamily: "Roboto, Arial, sans-serif"
    },

    container: {
      width: "380px",
      padding: "40px",
      border: "1px solid #dadce0",
      borderRadius: "8px"
    },

    title: {
      fontSize: "24px",
      fontWeight: "400",
      marginBottom: "8px",
      color: "#202124"
    },

    subtitle: {
      fontSize: "14px",
      color: "#5f6368",
      marginBottom: "24px"
    },

    field: {
      marginBottom: "18px"
    },

    label: {
      display: "block",
      fontSize: "13px",
      color: "#5f6368",
      marginBottom: "6px"
    },

    input: {
      width: "100%",
      padding: "10px",
      border: "1px solid #dadce0",
      borderRadius: "6px",
      fontSize: "14px",
      outline: "none"
    },

    button: {
      width: "100%",
      padding: "10px",
      background: "#1a73e8",
      color: "#fff",
      border: "none",
      borderRadius: "6px",
      fontSize: "14px",
      cursor: "pointer",
      marginTop: "10px"
    },

    footer: {
      marginTop: "20px",
      fontSize: "13px",
      color: "#5f6368",
      textAlign: "center"
    },

    link: {
      color: "#1a73e8",
      cursor: "pointer",
      fontWeight: "500"
    }
  };

  return (
    <div style={styles.page}>
      <div style={styles.container}>

        <div style={styles.title}>Create your Google Account</div>
        <div style={styles.subtitle}>to continue to your app</div>

        <form onSubmit={handleRegister}>

          <div style={styles.field}>
            <label style={styles.label}>Full name</label>
            <input
              type="text"
              value={name}
              onChange={(e)=>setName(e.target.value)}
              required
              style={styles.input}
              onFocus={(e)=>e.target.style.border="1px solid #1a73e8"}
              onBlur={(e)=>e.target.style.border="1px solid #dadce0"}
            />
          </div>

          <div style={styles.field}>
            <label style={styles.label}>Email</label>
            <input
              type="email"
              value={email}
              onChange={(e)=>setEmail(e.target.value)}
              required
              style={styles.input}
              onFocus={(e)=>e.target.style.border="1px solid #1a73e8"}
              onBlur={(e)=>e.target.style.border="1px solid #dadce0"}
            />
          </div>

          <div style={styles.field}>
            <label style={styles.label}>Password</label>
            <input
              type="password"
              value={password}
              onChange={(e)=>setPassword(e.target.value)}
              required
              style={styles.input}
              onFocus={(e)=>e.target.style.border="1px solid #1a73e8"}
              onBlur={(e)=>e.target.style.border="1px solid #dadce0"}
            />
          </div>

          <button type="submit" style={styles.button}>
            Create account
          </button>

        </form>

        <div style={styles.footer}>
          Already have an account?{" "}
          <span
            style={styles.link}
            onClick={()=>navigate("/login")}
          >
            Sign in
          </span>
        </div>

      </div>
    </div>
  );
}