import { useState } from "react";
import { loginUser } from "../api/auth";
import { useAuthContext } from "../context/AuthContext";
import { useNavigate, Link } from "react-router-dom";
// Importing your AI background
import welcomeBg from "../../assets/WelcomeUI.jpg"; 

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
    <div style={styles.pageWrapper}>
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
    </div>
  );
}

const styles = {
  pageWrapper: {
    height: "100vh",
    width: "100vw",
    backgroundImage: `url(${welcomeBg})`,
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
    // STYLE SYNC: 15% opacity and high blur
    background: "rgba(255, 255, 255, 0.15)", 
    backdropFilter: "blur(20px)",
    border: "1px solid rgba(255, 255, 255, 0.2)",
    boxShadow: "0 15px 45px rgba(0,0,0,0.4)",
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
  } as const,

  title: {
    textAlign: "center" as const,
    margin: "0",
    color: "#007bff", // STYLE SYNC: Link blue branding
    fontSize: "42px",
    fontWeight: "800",
    letterSpacing: "-1px",
  } as const,

  subtitle: {
    textAlign: "center" as const,
    marginBottom: "30px",
    fontSize: "16px",
    color: "#000000", // STYLE SYNC: Solid black contrast
    fontWeight: "600",
  } as const,

  form: {
    display: "flex",
    flexDirection: "column" as const,
    gap: "18px",
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
    color: "#001aff", // STYLE SYNC: Subtle black for auxiliary links
    textDecoration: "underline",
    fontWeight: "500",
  } as const,

  input: {
    padding: "16px",
    fontSize: "16px",
    borderRadius: "10px",
    border: "none",
    width: "100%",
    boxSizing: "border-box" as const,
    // STYLE SYNC: Clean off-white high-opacity fill
    background: "rgba(240, 248, 255, 0.95)",
    color: "#333",
    outline: "none",
  } as const,

  button: {
    padding: "16px",
    fontSize: "16px",
    fontWeight: "bold",
    background: "#007bff",
    color: "white",
    border: "none",
    borderRadius: "10px",
    cursor: "pointer",
    marginTop: "10px",
    boxShadow: "0 8px 25px rgba(0, 123, 255, 0.4)",
  } as const,

  errorBanner: {
    background: "rgba(254, 226, 226, 0.9)",
    color: "#dc2626",
    padding: "12px",
    borderRadius: "10px",
    marginBottom: "15px",
    fontSize: "14px",
    textAlign: "center" as const,
    border: "1px solid #fecaca",
    fontWeight: "600",
  } as const,

  footer: {
    marginTop: "30px",
    textAlign: "center" as const,
    fontSize: "14px",
    color: "#000000", // STYLE SYNC: Solid black
    fontWeight: "500",
  } as const,

  signUpLink: {
    color: "#007bff",
    textDecoration: "none",
    fontWeight: "800",
  } as const,
};