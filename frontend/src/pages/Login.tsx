import { useState } from "react";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    console.log("Login attempt:", { email, password });
  };

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Login</h1>

      <form onSubmit={handleSubmit} style={styles.form}>
        <input
          type="email"
          placeholder="Email"
          value={email}
          onChange={(e) => setEmail(e.target.value)}
          style={styles.input}
        />

        <input
          type="password"
          placeholder="Password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          style={styles.input}
        />

        <button type="submit" style={styles.button}>
          Login
        </button>
      </form>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "400px",
    margin: "80px auto",
    padding: "20px",
    borderRadius: "8px",
    background: "#f5f5f5",
    boxShadow: "0 0 10px rgba(0,0,0,0.1)",
  } as const,

  title: {
    textAlign: "center",
    marginBottom: "20px",
  } as const,

  form: {
    display: "flex",
    flexDirection: "column" as const,
    gap: "12px",
  } as const,

  input: {
    padding: "10px",
    fontSize: "16px",
  } as const,

  button: {
    padding: "10px",
    fontSize: "16px",
    background: "#007bff",
    color: "white",
    border: "none",
    cursor: "pointer",
  } as const,
};
