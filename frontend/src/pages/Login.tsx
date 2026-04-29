import { useState } from "react";
import { loginUser } from "../api/auth";
import { useAuthContext } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const { login } = useAuthContext();
  const navigate = useNavigate();

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setIsLoading(true);

    try {
      const result = await loginUser({ email, password });
      login(result.access_token, result.refresh_token, result.user);
      navigate("/dashboard");
    } catch (err: any) {
      setError(err.message || "Login failed. Please try again.");
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>u-sell-it</h1>
      <h2 style={styles.subtitle}>Login to your account</h2>

      {error && <div style={styles.errorBanner}>{error}</div>}

      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="email"
          placeholder="Email Address"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={styles.input}
          required
        />

        <div style={styles.passwordWrapper}>
          <input
            type="password"
            placeholder="Password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            style={styles.input}
            required
          />
          {/* Forgot Password Link Added Here */}
          <div style={styles.forgotPasswordLinkContainer}>
            <Link to="/forgot-password" style={styles.forgotLink}>
              Forgot password?
            </Link>
          </div>
        </div>

        <button 
          type="submit" 
          style={isLoading ? {...styles.button, opacity: 0.7} : styles.button}
          disabled={isLoading}
        >
          {isLoading ? "Logging in..." : "Login"}
        </button>
      </form>

      <div style={styles.footer}>
        Don't have an account? <Link to="/register" style={styles.signUpLink}>Sign Up</Link>
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "400px",
    margin: "80px auto",
    padding: "30px",
    borderRadius: "12px",
    background: "#ffffff",
    boxShadow: "0 4px 20px rgba(0,0,0,0.08)",
    fontFamily: "sans-serif",
  } as const,

  title: {
    textAlign: "center",
    margin: "0",
    color: "#007bff",
    fontSize: "28px",
  } as const,

  subtitle: {
    textAlign: "center",
    marginBottom: "24px",
    fontSize: "16px",
    color: "#666",
  } as const,

  form: {
    display: "flex",
    flexDirection: "column" as const,
    gap: "15px",
  } as const,

  passwordWrapper: {
    display: "flex",
    flexDirection: "column" as const,
    gap: "8px",
  } as const,

  forgotPasswordLinkContainer: {
    textAlign: "right" as const,
  },

  forgotLink: {
    fontSize: "13px",
    color: "#007bff",
    textDecoration: "none",
  } as const,

  input: {
    padding: "12px",
    fontSize: "16px",
    borderRadius: "6px",
    border: "1px solid #ddd",
    width: "100%",
    boxSizing: "border-box" as const,
  } as const,

  button: {
    padding: "12px",
    fontSize: "16px",
    fontWeight: "bold",
    background: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "6px",
    cursor: "pointer",
    marginTop: "10px",
  } as const,

  errorBanner: {
    background: "#fee2e2",
    color: "#dc2626",
    padding: "10px",
    borderRadius: "6px",
    marginBottom: "15px",
    fontSize: "14px",
    textAlign: "center",
    border: "1px solid #fecaca",
  } as const,

  footer: {
    marginTop: "20px",
    textAlign: "center",
    fontSize: "14px",
    color: "#666",
  } as const,

  signUpLink: {
    color: "#007bff",
    textDecoration: "none",
    fontWeight: "bold",
  } as const,
};