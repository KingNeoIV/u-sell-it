import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { resetPassword } from "../api/auth";
// Importing the specific New Password background
import newPasswordBg from "../../assets/NewPassword.jpg";

export default function ResetPassword() {
  const [searchParams] = useSearchParams();
  // This looks for "?token=..." in the browser address bar
  const token = searchParams.get("token") || ""; 
  
  const [newPassword, setNewPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isSuccess, setIsSuccess] = useState(false);

  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    if (newPassword !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    try {
      await resetPassword({ token, new_password: newPassword });
      setIsSuccess(true);
      // Give them a moment to see the success message before moving to login
      setTimeout(() => navigate("/login"), 3000);
    } catch (err: any) {
      setError(err.message || "Failed to reset password. The token may be expired.");
    }
  };

  return (
    <div style={styles.pageWrapper}>
      <div style={styles.container}>
        {isSuccess ? (
          <div style={{ textAlign: "center" }}>
            <h2 style={styles.successTitle}>Success!</h2>
            <p style={styles.text}>Your password has been updated. Redirecting you to login...</p>
            <div style={styles.loaderBar}></div>
          </div>
        ) : (
          <>
            <h1 style={styles.title}>New Password</h1>
            <p style={styles.text}>Please enter your new password below to secure your account.</p>

            {error && <div style={styles.errorBanner}>{error}</div>}

            <form onSubmit={handleSubmit} style={styles.form}>
              <input
                type="password"
                placeholder="New Password"
                value={newPassword}
                onChange={(e) => setNewPassword(e.target.value)}
                style={styles.input}
                required
              />
              <input
                type="password"
                placeholder="Confirm New Password"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                style={styles.input}
                required
              />
              <button type="submit" style={styles.button}>
                Update Password
              </button>
            </form>
          </>
        )}
      </div>
    </div>
  );
}

const styles = {
  pageWrapper: {
    height: "100vh",
    width: "100vw",
    backgroundImage: `url(${newPasswordBg})`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    margin: 0,
    padding: 0,
    overflow: "hidden",
  } as const,
  container: {
    maxWidth: "420px",
    width: "90%",
    padding: "45px",
    borderRadius: "24px",
    // STYLE SYNC: 15% white opacity for the glass
    background: "rgba(255, 255, 255, 0.15)",
    // STYLE SYNC: High 20px blur
    backdropFilter: "blur(20px)",
    boxShadow: "0 15px 45px rgba(0,0,0,0.4)",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    border: "1px solid rgba(255, 255, 255, 0.2)",
  } as const,
  title: { 
    textAlign: "center" as const, 
    margin: "0 0 10px 0",
    color: "#007bff", // STYLE SYNC: Brand Blue
    fontSize: "36px",
    fontWeight: "800",
    letterSpacing: "-0.5px"
  },
  text: { 
    textAlign: "center" as const, 
    color: "#000000", // STYLE SYNC: Solid Black contrast
    marginBottom: "30px",
    fontSize: "15px",
    fontWeight: "500"
  },
  successTitle: { 
    color: "#28a745", 
    fontSize: "32px", 
    fontWeight: "800", 
    textAlign: "center" as const,
    marginBottom: "10px" 
  },
  form: { display: "flex", flexDirection: "column" as const, gap: "18px" },
  input: { 
    padding: "16px", 
    borderRadius: "10px", 
    border: "none",
    fontSize: "16px",
    width: "100%",
    boxSizing: "border-box" as const,
    // STYLE SYNC: Soft off-white high-opacity fill
    background: "rgba(240, 248, 255, 0.95)",
    color: "#333",
    outline: "none"
  },
  button: { 
    padding: "16px", 
    background: "#28a745", 
    color: "white", 
    border: "none", 
    borderRadius: "10px", 
    cursor: "pointer",
    fontWeight: "bold",
    fontSize: "16px",
    boxShadow: "0 8px 25px rgba(40, 167, 69, 0.3)",
    marginTop: "10px"
  } as const,
  errorBanner: {
    background: "rgba(254, 226, 226, 0.9)",
    color: "#dc2626",
    padding: "14px",
    borderRadius: "10px",
    marginBottom: "15px",
    textAlign: "center" as const,
    fontSize: "14px",
    fontWeight: "bold",
    border: "1px solid #fecaca",
  } as const,
  loaderBar: { 
    height: "4px", 
    width: "100%", 
    background: "#28a745", 
    borderRadius: "2px",
    marginTop: "20px"
  },
};