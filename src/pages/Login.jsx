import { useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

export default function Login() {
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);

  const handleLogin = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const res = await api.post("/auth/login", { email, password });
      localStorage.setItem("token", res.data.access_token);
      navigate("/dashboard");
    } catch (err) {
      alert(err.response?.data?.detail || "Login failed");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <style>{`
  @import url('https://fonts.googleapis.com/css2?family=Roboto&display=swap');

  .page {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    background: #f1f3f4; /* light gray instead of pure white */
    font-family: 'Roboto', Arial, sans-serif;
  }

  .card {
    width: 100%;
    max-width: 380px;
    padding: 40px;
    border: 1px solid #ccc;
    border-radius: 10px;
    background: #fff;
  }

  .title {
    font-size: 24px;
    font-weight: 500;
    color: #111; /* darker */
    margin-bottom: 6px;
    text-align: center; /* 👈 add this */
  }

  .subtitle {
    font-size: 14px;
    color: #333; /* darker for readability */
    margin-bottom: 24px;
  }

  .field {
    margin-bottom: 18px;
  }

  .label {
    display: block;
    font-size: 13px;
    color: #222; /* darker */
    margin-bottom: 6px;
  }

  .input {
    width: 100%;
    padding: 10px;
    border: 1px solid #bbb; /* stronger border */
    border-radius: 6px;
    font-size: 14px;
    outline: none;
    background: #fff;
    color: #000;
  }

  .input:focus {
    border: 1px solid #1a73e8;
  }

  .btn {
    width: 100%;
    padding: 10px;
    background: #1a73e8;
    color: #fff;
    border: none;
    border-radius: 6px;
    font-size: 14px;
    cursor: pointer;
    margin-top: 10px;
  }

  .footer {
    margin-top: 20px;
    font-size: 13px;
    color: #333; /* darker */
    text-align: center;
  }

  .link {
    color: #1a73e8;
    cursor: pointer;
    font-weight: 500;
  }
`}</style>

      <div className="card">
        <div className="title">Sign in</div>
        <form onSubmit={handleLogin}>
          <div className="field">
            <label className="label">Email</label>
            <input
              className="input"
              type="email"
              value={email}
              onChange={(e)=>setEmail(e.target.value)}
              required
            />
          </div>

          <div className="field">
            <label className="label">Password</label>
            <input
              className="input"
              type="password"
              value={password}
              onChange={(e)=>setPassword(e.target.value)}
              required
            />
          </div>

          <button className="btn" type="submit" disabled={loading}>
            {loading ? "Signing in..." : "Sign in"}
          </button>
        </form>

        <div className="footer">
          Don’t have an account?{" "}
          <span className="link" onClick={()=>navigate("/register")}>
            Create account
          </span>
        </div>
      </div>
    </div>
  );
}