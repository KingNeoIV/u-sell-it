import { useState } from "react";
import { Link, useLocation } from "react-router-dom";
import { useAuth } from "../hooks/useAuth";

export default function Navbar() {
  const { user, isAuthenticated, logout } = useAuth();
  const [isDropdownOpen, setIsDropdownOpen] = useState(false);
  const location = useLocation();

  if (location.pathname === "/login" || location.pathname === "/register") {
    return null;
  }

  return (
    <nav style={styles.topBar}>
      {/* BRAND / LOGO */}
      <div style={styles.left}>
        <Link to="/dashboard" style={styles.brand}>
          U-SELL-IT
        </Link>
      </div>

      {/* SEARCH PILL */}
      <div style={styles.center}>
        <input type="text" placeholder="Search marketplace..." style={styles.searchInput} />
      </div>

      {/* USER PROFILE & DROPDOWN */}
      {isAuthenticated && (
        <div style={styles.right}>
          <div 
            style={styles.profilePill} 
            onClick={() => setIsDropdownOpen(!isDropdownOpen)}
          >
            <div style={styles.avatar}></div>
            <div style={styles.userInfo}>
              <span style={styles.userName}>{user?.email?.split('@')[0]}</span>
              <span style={styles.userRole}>Pro Seller</span>
            </div>
            <span style={styles.chevron}>{isDropdownOpen ? "▴" : "▾"}</span>

            {/* THE DROPDOWN MENU */}
            {isDropdownOpen && (
              <div style={styles.dropdown}>
                <Link to="/dashboard" style={styles.dropLink}>Dashboard</Link>
                <Link to="/profile" style={styles.dropLink}>Profile Settings</Link>
                <Link to="/listings" style={styles.dropLink}>My Listings</Link>
                <Link to="/listings/create" style={styles.dropLink}>+ Create Listing</Link>
                <div style={styles.dropDivider}></div>
                <button style={styles.logoutBtn} onClick={logout}>Logout</button>
              </div>
            )}
          </div>
        </div>
      )}
    </nav>
  );
}

const styles = {
  topBar: {
    height: "70px",
    width: "100%",
    background: "#ffffff",
    borderBottom: "1px solid #eee",
    display: "flex",
    alignItems: "center",
    justifyContent: "space-between",
    padding: "0 5px",
    position: "fixed" as const,
    top: 0,
    left: 0,
    zIndex: 1000,
  } as const,

  left: { display: "flex", alignItems: "center" },
  brand: { color: "#007bff", fontSize: "20px", fontWeight: "900", textDecoration: "none", letterSpacing: "-1px" },

  center: { flex: 1, display: "flex", justifyContent: "center", padding: "0 40px" },
  searchInput: { 
    width: "100%", maxWidth: "500px", padding: "10px 20px", borderRadius: "50px", 
    border: "1px solid #f0f0f0", background: "#f8f9fa", outline: "none" 
  },

  right: { position: "relative" as const },
  profilePill: { 
    display: "flex", alignItems: "center", gap: "10px", padding: "5px 15px", 
    borderRadius: "50px", border: "1px solid #eee", cursor: "pointer", background: "#fff",
    userSelect: "none" as const
  },
  avatar: { width: "30px", height: "30px", borderRadius: "50%", background: "#007bff" },
  userInfo: { display: "flex", flexDirection: "column" as const },
  userName: { fontSize: "13px", fontWeight: "700", color: "#333" },
  userRole: { fontSize: "10px", color: "#007bff", fontWeight: "800" },
  chevron: { fontSize: "12px", color: "#ccc", marginLeft: "5px" },

  dropdown: {
    position: "absolute" as const, top: "120%", right: 0, width: "200px", 
    background: "#fff", borderRadius: "12px", border: "1px solid #eee", 
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)", padding: "10px", display: "flex", flexDirection: "column" as const
  },
  dropLink: { 
    padding: "10px", textDecoration: "none", color: "#555", fontSize: "14px", 
    fontWeight: "600", borderRadius: "8px", transition: "0.2s" 
  },
  dropDivider: { height: "1px", background: "#f5f5f5", margin: "8px 0" },
  logoutBtn: { 
    padding: "10px", border: "none", background: "none", color: "#dc3545", 
    fontWeight: "700", textAlign: "left" as const, cursor: "pointer", fontSize: "14px"
  }
};