import { useState } from "react";
import { forgotPassword } from "../api/auth";
import { Link } from "react-router-dom";
// Importing your security-themed background image
import forgotBg from "../../assets/ForgotPassword.jpg";

export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  
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
      const safeToken = encodeURIComponent(result.token);
      const resetUrl = `${window.location.origin}/reset-password?token=${safeToken}`;
      
      setToken(result.token);
      setGeneratedLink(resetUrl);
      setMessage("Simulation: Password reset token generated successfully!");
    } catch (err: any) {
      setError(err.message || "Something went wrong. Please try again.");
    }
  };

  return (
    <div style={styles.pageWrapper}>
      <div style={styles.container}>
        {/* STYLE SYNC: Title is Brand Blue, Subtitle is Solid Black */}
        <h1 style={styles.title}>Reset Password</h1>
        <p style={styles.text}>Enter your email to generate a simulation reset link.</p>

        {message && <div style={styles.successBanner}>{message}</div>}
        {error && <div style={styles.errorBanner}>{error}</div>}

        {generatedLink && (
          <div style={styles.simulationBox}>
            <p style={styles.label}>Copy/Paste this simulation link:</p>
            <code style={styles.codeBlock}>{generatedLink}</code>
            
            <div style={{ marginTop: "15px" }}>
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
              placeholder="Your Email Address"
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
    </div>
  );
}

const styles = {
  pageWrapper: {
    height: "100vh",
    width: "100vw",
    backgroundImage: `url(${forgotBg})`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
    margin: 0,
    padding: 0,
    overflow: "hidden",
  } as const,
  // STYLE SYNC: High blur, 15% opacity container
  container: { 
    maxWidth: "450px", 
    width: "90%",
    padding: "45px", 
    borderRadius: "24px", 
    background: "rgba(255, 255, 255, 0.15)", 
    backdropFilter: "blur(20px)",
    boxShadow: "0 15px 45px rgba(0,0,0,0.4)", 
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    border: "1px solid rgba(255, 255, 255, 0.2)",
    textAlign: "center" as const,
  } as const,
  // STYLE SYNC: Brand Blue title
  title: { textAlign: "center", color: "#007bff", margin: "0 0 10px 0", fontSize: "36px", fontWeight: "800", letterSpacing: "-0.5px" } as const,
  // STYLE SYNC: Solid Black text
  text: { textAlign: "center", fontSize: "15px", color: "#000000", marginBottom: "30px", fontWeight: "500" } as const,
  form: { display: "flex", flexDirection: "column" as const, gap: "18px" } as const,
  // STYLE SYNC: Refined high-opacity off-white inputs
  input: { padding: "16px", borderRadius: "10px", border: "none", fontSize: "16px", width: "100%", boxSizing: "border-box" as const, background: "rgba(240, 248, 255, 0.95)", color: "#333", outline: "none" } as const,
  button: { padding: "16px", background: "#007bff", color: "white", border: "none", borderRadius: "10px", cursor: "pointer", fontWeight: "bold", fontSize: "16px", boxShadow: "0 8px 25px rgba(0, 123, 255, 0.4)" } as const,
  // STYLE SYNC: Translucent simulation box for better glass blending
  simulationBox: { background: "rgba(255, 255, 255, 0.1)", padding: "20px", borderRadius: "12px", border: "1px dashed #000", marginTop: "10px", textAlign: "center" as const },
  label: { fontSize: "13px", fontWeight: "bold", color: "#000", marginBottom: "8px" } as const,
  codeBlock: { display: "block", padding: "10px", background: "#fff", border: "1px solid #cce3ff", borderRadius: "4px", fontSize: "13px", wordBreak: "break-all" as const, color: "#333" },
  actionButton: { display: "inline-block", padding: "12px 24px", background: "#28a745", color: "white", textDecoration: "none", borderRadius: "10px", fontSize: "14px", fontWeight: "bold", boxShadow: "0 4px 10px rgba(40, 167, 69, 0.3)" } as const,
  successBanner: { background: "rgba(220, 252, 231, 0.9)", color: "#166534", padding: "14px", borderRadius: "10px", textAlign: "center", marginBottom: "15px", fontSize: "14px", fontWeight: "bold", border: "1px solid #bbf7d0" } as const,
  errorBanner: { background: "rgba(254, 226, 226, 0.9)", color: "#dc2626", padding: "14px", borderRadius: "10px", textAlign: "center", marginBottom: "15px", fontSize: "14px", fontWeight: "bold", border: "1px solid #fecaca" } as const,
  footer: { marginTop: "30px", textAlign: "center" } as const,
  // STYLE SYNC: Black back link for consistency
  backLink: { color: "#0026fa", textDecoration: "none", fontSize: "14px", fontWeight: "600" } as const,
};