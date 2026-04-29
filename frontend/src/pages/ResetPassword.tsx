import { useState } from "react";
import { useSearchParams, useNavigate } from "react-router-dom";
import { resetPassword } from "../api/auth";

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

  if (isSuccess) {
    return (
      <div style={styles.container}>
        <h2 style={{ color: "green" }}>Success!</h2>
        <p>Your password has been updated. Redirecting you to login...</p>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>New Password</h1>
      <p style={styles.text}>Please enter your new password below.</p>

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
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "400px",
    margin: "80px auto",
    padding: "30px",
    borderRadius: "12px",
    background: "#fff",
    boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
  } as const,
  title: { textAlign: "center" as const, marginBottom: "10px" },
  text: { textAlign: "center" as const, color: "#666", marginBottom: "20px" },
  form: { display: "flex", flexDirection: "column" as const, gap: "15px" },
  input: { padding: "12px", borderRadius: "6px", border: "1px solid #ddd" },
  button: { 
    padding: "12px", 
    background: "#28a745", 
    color: "white", 
    border: "none", 
    borderRadius: "6px", 
    cursor: "pointer",
    fontWeight: "bold" 
  } as const,
  errorBanner: {
    background: "#fee2e2",
    color: "#dc2626",
    padding: "10px",
    borderRadius: "6px",
    marginBottom: "15px",
    textAlign: "center" as const,
    fontSize: "14px",
  } as const,
};