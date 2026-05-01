/**
 * @fileoverview Password Recovery Request View.
 * Facilitates the "Forgot Password" flow by allowing users to request a reset token.
 * Note: Includes simulation logic to display tokens directly for development purposes.
 */

import { useState, useEffect } from "react";
import { forgotPassword } from "../api/auth";
import { Link } from "react-router-dom";
import forgotBg from "../../assets/ForgotPassword.jpg";

/**
 * ForgotPassword Component.
 * Workflow:
 * 1. User submits email address.
 * 2. API generates a reset token and expiration timestamp.
 * 3. Component calculates remaining time and starts a countdown.
 * 4. User is provided a direct link to the ResetPassword view.
 */
export default function ForgotPassword() {
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  
  // State for simulated recovery flow
  const [token, setToken] = useState<string | null>(null);
  const [generatedLink, setGeneratedLink] = useState<string | null>(null);
  const [timeLeft, setTimeLeft] = useState<number | null>(null);

  // Countdown Timer Effect 
  useEffect(() => {
    if (timeLeft === null || timeLeft <= 0) return;

    const intervalId = setInterval(() => {
      setTimeLeft((prev) => (prev !== null ? prev - 1 : null));
    }, 1000);

    return () => clearInterval(intervalId);
  }, [timeLeft]);

  // Formatter (converts seconds to MM:SS)
  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins}:${secs < 10 ? "0" : ""}${secs}`;
  };

  /**
   * Handles the password reset request.
   * Calculates the expiry offset based on server-provided timestamp.
   */
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setMessage(null);
    setGeneratedLink(null);
    setToken(null);
    setTimeLeft(null);

    try {
      const result = await forgotPassword({ email });
      
      // 1. Get the server's expiry time
      const expiryDate = new Date(result.expires_at);
      
      // 2. Get the current time but explicitly adjust it to UTC 
      // This cancels out the 5-hour offset in Victoria, TX
      const now = new Date();
      const utcNow = Date.UTC(
        now.getUTCFullYear(),
        now.getUTCMonth(),
        now.getUTCDate(),
        now.getUTCHours(),
        now.getUTCMinutes(),
        now.getUTCSeconds()
      );

      // 3. Calculate difference using the UTC-specific timestamp
      const secondsRemaining = Math.floor((expiryDate.getTime() - utcNow) / 1000);
      
      const safeToken = encodeURIComponent(result.token);
      const resetUrl = `${window.location.origin}/reset-password?token=${safeToken}`;
      
      // Safety check: if it's still weirdly high, cap it at 15 mins for the UI
      const finalSeconds = secondsRemaining > 900 ? 900 : secondsRemaining;
      
      setTimeLeft(finalSeconds > 0 ? finalSeconds : 0);
      setToken(result.token);
      setGeneratedLink(resetUrl);
      setMessage("Simulation: Password reset token generated successfully!");
    } catch (err: any) {
      setError(err.message || "No account found with that email address.");
    }
  };

  return (
    <div style={styles.pageWrapper} role="main">
      <div style={styles.container}>
        <h1 style={styles.title}>Reset Password</h1>
        <p style={styles.text}>Enter your email to generate a simulation reset link.</p>

        {message && <div style={styles.successBanner} role="alert">{message}</div>}
        {error && <div style={styles.errorBanner} role="alert">{error}</div>}

        {generatedLink && (
          <div style={styles.simulationBox}>
            <p style={styles.timerText}>
              Token Expires In: <span style={{ color: "#d9534f" }}>{timeLeft !== null ? formatTime(timeLeft) : "0:00"}</span>
            </p>

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
              aria-label="Email Address"
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
    position: "fixed" as const,
    top: 0, bottom: 0, left: 0, right: 0,
    height: "100vh", width: "100vw", 
    backgroundImage: `url(${forgotBg})`,
    backgroundSize: "cover",
    backgroundPosition: "center",
    backgroundRepeat: "no-repeat",
    display: "flex",
    alignItems: "center",
    justifyContent: "center",
  } as const,

  container: { 
    maxWidth: "450px", width: "90%",
    padding: "45px", borderRadius: "24px", 
    background: "rgba(255, 255, 255, 0.15)", 
    backdropFilter: "blur(20px)",
    boxShadow: "0 15px 45px rgba(0,0,0,0.4)", 
    fontFamily: "system-ui, -apple-system, sans-serif",
    border: "1px solid rgba(255, 255, 255, 0.2)",
    textAlign: "center" as const,
  } as const,

  title: { color: "#007bff", margin: "0 0 10px 0", fontSize: "36px", fontWeight: "800" } as const,

  text: { fontSize: "15px", color: "#000000", marginBottom: "30px", fontWeight: "500" } as const,

  form: { display: "flex", flexDirection: "column" as const, gap: "18px" } as const,

  input: { 
    padding: "16px", borderRadius: "10px", border: "none", fontSize: "16px", 
    width: "100%", boxSizing: "border-box" as const, 
    background: "rgba(240, 248, 255, 0.95)", color: "#333", outline: "none" 
  } as const,

  button: { 
    padding: "16px", background: "#007bff", color: "white", border: "none", 
    borderRadius: "10px", cursor: "pointer", fontWeight: "bold", fontSize: "16px", 
    boxShadow: "0 8px 25px rgba(0, 123, 255, 0.4)" 
  } as const,

  simulationBox: { 
    background: "rgba(255, 255, 255, 0.1)", padding: "20px", borderRadius: "12px", 
    border: "1px dashed #000", marginTop: "10px", textAlign: "center" as const 
  },

  timerText: {
    fontSize: "16px", fontWeight: "bold", color: "#000", marginBottom: "15px",
    padding: "8px", background: "rgba(255, 255, 255, 0.4)", borderRadius: "8px",
    display: "inline-block",
  } as const,

  label: { fontSize: "13px", fontWeight: "bold", color: "#000", marginBottom: "8px" } as const,

  codeBlock: { 
    display: "block", padding: "10px", background: "#fff", border: "1px solid #cce3ff", 
    borderRadius: "4px", fontSize: "13px", wordBreak: "break-all" as const, color: "#333" 
  },

  actionButton: { 
    display: "inline-block", padding: "12px 24px", background: "#28a745", color: "white", 
    textDecoration: "none", borderRadius: "10px", fontSize: "14px", fontWeight: "bold", 
    boxShadow: "0 4px 10px rgba(40, 167, 69, 0.3)" 
  } as const,

  successBanner: { 
    background: "rgba(220, 252, 231, 0.9)", color: "#166534", padding: "14px", 
    borderRadius: "10px", marginBottom: "15px", fontSize: "14px", fontWeight: "bold", 
    border: "1px solid #bbf7d0" 
  } as const,

  errorBanner: { 
    background: "rgba(254, 226, 226, 0.9)", color: "#dc2626", padding: "14px", 
    borderRadius: "10px", marginBottom: "15px", fontSize: "14px", fontWeight: "bold", 
    border: "1px solid #fecaca" 
  } as const,

  footer: { marginTop: "30px", textAlign: "center" } as const,

  backLink: { color: "#0026fa", textDecoration: "none", fontSize: "14px", fontWeight: "600" } as const,
};