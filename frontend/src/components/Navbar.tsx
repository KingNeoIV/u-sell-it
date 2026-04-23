import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Navbar() {
  const { isAuthenticated, logout } = useAuth();
  const location = useLocation();

  // Hide navbar on login/register
  if (location.pathname === "/login" || location.pathname === "/register") {
    return null;
  }

  return (
    <nav style={styles.nav}>
      <div style={styles.left}>
        <Link to="/dashboard" style={styles.brand}>
          U-Sell-It
        </Link>
      </div>

      {isAuthenticated && (
        <div style={styles.right}>
          <Link to="/dashboard" style={styles.link}>
            Dashboard
          </Link>

          <Link to="/profile" style={styles.link}>
            Profile
          </Link>

          <button style={styles.logout} onClick={logout}>
            Logout
          </button>
        </div>
      )}
    </nav>
  );
}

const styles = {
  nav: {
    width: "100%",
    padding: "12px 2px",
    background: "#007bff",
    color: "white",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
  } as const,

  left: {
    display: "flex",
    alignItems: "center",
  } as const,

  brand: {
    color: "white",
    fontSize: "20px",
    textDecoration: "none",
    fontWeight: "bold",
  } as const,

  right: {
    display: "flex",
    gap: "16px",
    alignItems: "center",
    paddingRight: "12px",
  } as const,

  link: {
    color: "white",
    textDecoration: "none",
    fontSize: "16px",
  } as const,

  logout: {
    background: "#dc3545",
    border: "none",
    padding: "8px 12px",
    color: "white",
    cursor: "pointer",
  } as const,
};
