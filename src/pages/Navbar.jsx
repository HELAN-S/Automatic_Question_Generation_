import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const isLoggedIn = localStorage.getItem("token");

  return (
    <>
      <style>{`
        .navbar {
          height: 60px;
          display: flex;
          align-items: center;
          justify-content: space-between;
          padding: 0 30px;
          border-bottom: 1px solid #e0e0e0;
          background: #fff;
          position: sticky;
          top: 0;
          z-index: 1000;
          font-family: Roboto, Arial, sans-serif;
        }

        .logo {
          font-size: 18px;
          font-weight: 500;
          color: #111;
          cursor: pointer;
        }

        .nav-right {
          display: flex;
          align-items: center;
          gap: 16px;
        }

        .link {
          font-size: 14px;
          color: #444;
          cursor: pointer;
        }

        .link:hover {
          color: #000;
        }

        .btn {
          padding: 6px 14px;
          border-radius: 6px;
          border: none;
          background: #1a73e8;
          color: #fff;
          font-size: 14px;
          cursor: pointer;
        }

        .btn-outline {
          padding: 6px 14px;
          border-radius: 6px;
          border: 1px solid #dadce0;
          background: #fff;
          color: #1a73e8;
          font-size: 14px;
          cursor: pointer;
        }
      `}</style>

      <div className="navbar">
        <div className="logo" onClick={() => navigate("/")}>
          MyApp
        </div>

        <div className="nav-right">
          {!isLoggedIn ? (
            <>
              <span className="link" onClick={() => navigate("/login")}>
                Sign in
              </span>
              <button className="btn" onClick={() => navigate("/register")}>
                Create account
              </button>
            </>
          ) : (
            <>
              <span className="link" onClick={() => navigate("/profile")}>
                Profile
              </span>
              <button
                className="btn-outline"
                onClick={() => {
                  localStorage.removeItem("token");
                  navigate("/login");
                }}
              >
                Logout
              </button>
            </>
          )}
        </div>
      </div>
    </>
  );
}