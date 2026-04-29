import { useState } from "react";
import { forgotPassword } from "../api/auth";
import { Link } from "react-router-dom";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  // Keep the token and the full link separate
  const [token, setToken] = useState<string | null>(null);
  const [generatedLink, setGeneratedLink] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);
    setGeneratedLink(null);
    setToken(null);

    try {
      const result = await forgotPassword({ email });
      
      // result.token might contain characters like #, &, or ^
      // encodeURIComponent converts them to URL-safe codes (e.g., # becomes %23)
      const safeToken = encodeURIComponent(result.token);
      
      const resetUrl = `${window.location.origin}/reset-password?token=${safeToken}`;
      
      // We store the original token for logic, but the safe link for the UI
      setToken(result.token);
      setGeneratedLink(resetUrl);
      setMessage("Simulation: Password reset token generated successfully!");
    } catch (err: any) {
      setError(err.message || "Something went wrong. Please try again.");
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Reset Password</h1>
      <p style={styles.text}>Enter your email to generate a simulation reset link.</p>

      {message && <div style={styles.successBanner}>{message}</div>}
      {error && <div style={styles.errorBanner}>{error}</div>}

      {generatedLink && (
        <div style={styles.simulationBox}>
          <p style={styles.label}>Copy/Paste this simulation link:</p>
          <code style={styles.codeBlock}>{generatedLink}</code>
          
          <div style={{ marginTop: "15px" }}>
            {/* Using the token state directly makes TypeScript happy */}
            <Link 
              to={`/reset-password?token=${token}`} 
              style={styles.actionButton}
            >
              Go to Reset Page →
            </Link>
          </div>
        </div>
      )}

      {!generatedLink && (
        <form onSubmit={handleSubmit} style={styles.form}>
          <input
            type="email"
            placeholder="Email Address"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            style={styles.input}
            required
          />
          <button type="submit" style={styles.button}>
            Generate Reset Link
          </button>
        </form>
      )}

      <div style={styles.footer}>
        <Link to="/login" style={styles.backLink}>Back to Login</Link>
      </div>
    </div>
  );
}

const styles = {
  container: { maxWidth: "450px", margin: "80px auto", padding: "30px", borderRadius: "12px", background: "#fff", boxShadow: "0 4px 20px rgba(0,0,0,0.08)", fontFamily: "sans-serif" } as const,
  title: { textAlign: "center", color: "#333", marginBottom: "10px" } as const,
  text: { textAlign: "center", fontSize: "14px", color: "#666", marginBottom: "20px" } as const,
  form: { display: "flex", flexDirection: "column" as const, gap: "15px" } as const,
  input: { padding: "12px", borderRadius: "6px", border: "1px solid #ddd", fontSize: "16px" } as const,
  button: { padding: "12px", background: "#007bff", color: "white", border: "none", borderRadius: "6px", cursor: "pointer", fontWeight: "bold" } as const,
  simulationBox: { background: "#f0f7ff", padding: "20px", borderRadius: "8px", border: "1px dashed #007bff", marginTop: "10px", textAlign: "center" as const },
  label: { fontSize: "12px", fontWeight: "bold", color: "#0056b3", marginBottom: "8px" } as const,
  codeBlock: { display: "block", padding: "10px", background: "#fff", border: "1px solid #cce3ff", borderRadius: "4px", fontSize: "13px", wordBreak: "break-all" as const, color: "#333" },
  actionButton: { display: "inline-block", padding: "10px 20px", background: "#28a745", color: "white", textDecoration: "none", borderRadius: "6px", fontSize: "14px", fontWeight: "bold" } as const,
  successBanner: { background: "#dcfce7", color: "#166534", padding: "12px", borderRadius: "6px", textAlign: "center", marginBottom: "15px", fontSize: "14px" } as const,
  errorBanner: { background: "#fee2e2", color: "#dc2626", padding: "12px", borderRadius: "6px", textAlign: "center", marginBottom: "15px", fontSize: "14px" } as const,
  footer: { marginTop: "25px", textAlign: "center" } as const,
  backLink: { color: "#007bff", textDecoration: "none", fontSize: "14px" } as const,
};