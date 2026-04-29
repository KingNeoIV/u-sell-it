import { useState } from "react";
import { useAuth } from "../hooks/useAuth";
import { useNavigate, Link } from "react-router-dom";
// Importing the Register wallpaper
import registerBg from "../../assets/CustomerService.jpg";

export default function Register() {
  const { login } = useAuth();
  const navigate = useNavigate();

  const [form, setForm] = useState({ email: "", password: "" });
  const [error, setError] = useState<string | null>(null);
  const [success, setSuccess] = useState<string | null>(null);
  const [isSubmitting, setIsSubmitting] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);
    setSuccess(null);
    setIsSubmitting(true);

    try {
      const res = await fetch("http://localhost:8000/auth/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(form),
      });

      const data = await res.json();

      if (!res.ok) {
        setError(data.detail || "Registration failed. Please check your info.");
        setIsSubmitting(false);
        return;
      }

      setSuccess("Success! Your account has been created.");
      
      setTimeout(() => {
        login(data.access_token, data.refresh_token || "", data.user);
        navigate("/dashboard");
      }, 2000);

    } catch (err) {
      setError("Unable to connect to the server.");
      setIsSubmitting(false);
    }
  };

  return (
    <div style={styles.pageWrapper}>
      <div style={styles.container}>
        {/* Title updated to Link Blue, Subtitle to Solid Black */}
        <h1 style={styles.title}>Create Account</h1>
        <p style={styles.text}>Start showcasing your items to your local area.</p>

        {success && <div style={styles.successBanner}>{success}</div>}
        {error && <div style={styles.errorBanner}>{error}</div>}

        {!success ? (
          <form onSubmit={handleSubmit} style={styles.form}>
            <input
              name="email"
              type="email"
              placeholder="Your Email Address"
              value={form.email}
              onChange={(e) => setForm({ ...form, email: e.target.value })}
              style={styles.input}
              required
            />
            <input
              name="password"
              type="password"
              placeholder="Choose a Strong Password"
              value={form.password}
              onChange={(e) => setForm({ ...form, password: e.target.value })}
              style={styles.input}
              required
            />
            <button 
              type="submit" 
              disabled={isSubmitting} 
              style={isSubmitting ? styles.buttonDisabled : styles.button}
            >
              {isSubmitting ? "Generating Account..." : "Create Account"}
            </button>
          </form>
        ) : (
          <div style={styles.simulationBox}>
            <p style={styles.label}>Redirecting to your dashboard...</p>
            <div style={styles.loaderBar}></div>
          </div>
        )}

        <div style={styles.footer}>
          <Link to="/login" style={styles.backLink}>Already have an account? Login</Link>
        </div>
      </div>
    </div>
  );
}

const styles = {
  pageWrapper: {
    height: "100vh",
    width: "100vw",
    backgroundImage: `url(${registerBg})`,
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
    background: "rgba(255, 255, 255, 0.15)", 
    backdropFilter: "blur(20px)",
    border: "1px solid rgba(255, 255, 255, 0.2)",
    boxShadow: "0 15px 45px rgba(0,0,0,0.4)", 
    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif",
    textAlign: "center" as const,
  } as const,
  title: { 
    textAlign: "center", 
    color: "#007bff", // Colored like a link (Brand Blue)
    fontSize: "36px", 
    fontWeight: "800", 
    margin: "0 0 10px 0",
    letterSpacing: "-0.5px",
  } as const,
  text: { 
    textAlign: "center", 
    fontSize: "15px", 
    color: "#000000", // Solid Black for contrast
    marginBottom: "35px",
    fontWeight: "500", // Slightly bolder to stand out on glass
  } as const,
  form: { display: "flex", flexDirection: "column" as const, gap: "18px" } as const,
  input: { 
    padding: "16px", 
    borderRadius: "10px", 
    border: "none", 
    background: "rgba(240, 248, 255, 0.95)",
    fontSize: "16px", 
    width: "100%", 
    boxSizing: "border-box" as const,
    color: "#333",
    outline: "none",
  } as const,
  button: { 
    padding: "16px", 
    background: "#007bff", 
    color: "white", 
    border: "none", 
    borderRadius: "10px", 
    cursor: "pointer", 
    fontWeight: "bold", 
    fontSize: "16px", 
    boxShadow: "0 8px 25px rgba(0, 123, 255, 0.4)",
    marginTop: "10px",
  } as const,
  buttonDisabled: { 
    padding: "16px", 
    background: "rgba(0, 123, 255, 0.5)", 
    color: "rgba(255, 255, 255, 0.8)", 
    border: "none", 
    borderRadius: "10px", 
    cursor: "not-allowed",
    marginTop: "10px",
  } as const,
  successBanner: { 
    background: "rgba(220, 252, 231, 0.9)", 
    color: "#166534", 
    padding: "14px", 
    borderRadius: "10px", 
    textAlign: "center", 
    marginBottom: "15px", 
    fontSize: "14px",
    fontWeight: "bold",
  } as const,
  errorBanner: { 
    background: "rgba(254, 226, 226, 0.9)", 
    color: "#dc2626", 
    padding: "14px", 
    borderRadius: "10px", 
    textAlign: "center", 
    marginBottom: "15px", 
    fontSize: "14px",
    fontWeight: "bold",
  } as const,
  simulationBox: { background: "rgba(255, 255, 255, 0.05)", padding: "20px", borderRadius: "12px", border: "1px dashed #000", marginTop: "10px", textAlign: "center" as const },
  label: { fontSize: "13px", fontWeight: "bold", color: "#000", marginBottom: "12px" } as const,
  loaderBar: { height: "4px", width: "100%", background: "#000", borderRadius: "2px" }, 
  footer: { marginTop: "30px", textAlign: "center" } as const,
  backLink: { 
    color: "#0423c18c", // Set "Already have an account?" text to black for consistency
    textDecoration: "none", 
    fontSize: "14px", 
    fontWeight: "600" 
  } as const,
};