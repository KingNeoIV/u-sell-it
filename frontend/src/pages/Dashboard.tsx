import { useAuth } from "../hooks/useAuth";

export default function Dashboard() {
  const { user, logout } = useAuth();

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Dashboard</h1>

      <div style={styles.card}>
        <p style={styles.text}>Welcome, {user?.email}</p>

        <button style={styles.button} onClick={logout}>
          Logout
        </button>
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "600px",
    margin: "80px auto",
    padding: "20px",
    background: "#f5f5f5",
    borderRadius: "8px",
    boxShadow: "0 0 10px rgba(0,0,0,0.1)",
  } as const,

  title: {
    textAlign: "center",
    marginBottom: "20px",
  } as const,

  card: {
    padding: "20px",
    background: "white",
    borderRadius: "8px",
    boxShadow: "0 0 5px rgba(0,0,0,0.1)",
    display: "flex",
    flexDirection: "column" as const,
    gap: "16px",
  } as const,

  text: {
    fontSize: "18px",
  } as const,

  button: {
    padding: "10px",
    fontSize: "16px",
    background: "#dc3545",
    color: "white",
    border: "none",
    cursor: "pointer",
  } as const,
};
