/**
 * @fileoverview User Profile View.
 * Displays the authenticated user's account details and provides 
 * a foundation for account management settings.
 */

import { useAuth } from "../hooks/useAuth";

/**
 * Profile Component.
 * * * Features:
 * - Read-only display of core user data (Email, ID).
 * - Responsive container that clears the global fixed Navbar.
 * - Integration with `useAuth` hook for real-time user state.
 * * @returns {JSX.Element} The rendered Profile view.
 */
export default function Profile() {
  const { user } = useAuth();

  return (
    <main style={styles.container} aria-labelledby="profile-heading">
      <h1 id="profile-heading" style={styles.title}>
        Account Profile
      </h1>

      <div style={styles.card}>
        <section aria-label="Personal Information">
          <p style={styles.label}>Email Address</p>
          <p style={styles.value}>{user?.email || "Not available"}</p>

          <p style={styles.label}>Unique User ID</p>
          <p style={styles.value}>{user?.id || "Generating..."}</p>
        </section>
        
        {/* Placeholder for future actions */}
        <div style={styles.footer}>
          <button style={styles.secondaryBtn} disabled>
            Edit Profile (Coming Soon)
          </button>
        </div>
      </div>
    </main>
  );
}

/**
 * Component Styles.
 * Synced with the application's card-based layout guidelines.
 */
const styles = {
  container: {
    maxWidth: "600px",
    margin: "100px auto 40px", // Margin-top adjusted for fixed Navbar
    padding: "20px",
  } as const,

  title: {
    textAlign: "center" as const,
    marginBottom: "30px",
    fontSize: "32px",
    fontWeight: "800",
    color: "#333",
    letterSpacing: "-0.5px",
  },

  card: {
    padding: "40px",
    background: "white",
    borderRadius: "16px",
    border: "1px solid #eee",
    boxShadow: "0 10px 30px rgba(0,0,0,0.05)",
    display: "flex",
    flexDirection: "column" as const,
    gap: "8px",
  } as const,

  label: {
    fontWeight: "700",
    fontSize: "12px",
    textTransform: "uppercase" as const,
    color: "#888",
    letterSpacing: "0.5px",
    marginBottom: "4px",
  } as const,

  value: {
    fontSize: "18px",
    color: "#1a1a1a",
    marginBottom: "24px",
    wordBreak: "break-all" as const, // Ensures long IDs or emails don't break the layout
  } as const,

  footer: {
    marginTop: "10px",
    paddingTop: "20px",
    borderTop: "1px solid #f5f5f5",
    textAlign: "center" as const,
  },

  secondaryBtn: {
    background: "none",
    border: "1px solid #ddd",
    color: "#999",
    padding: "10px 20px",
    borderRadius: "8px",
    fontSize: "14px",
    cursor: "not-allowed",
  }
};