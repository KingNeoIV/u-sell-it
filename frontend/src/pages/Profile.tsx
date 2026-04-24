import { useAuth } from "../hooks/useAuth";

export default function Profile() {
  const { user } = useAuth();

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Profile</h1>

      <div style={styles.card}>
        <p style={styles.label}>Email</p>
        <p style={styles.value}>{user?.email}</p>

        <p style={styles.label}>User ID</p>
        <p style={styles.value}>{user?.id}</p>
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
    gap: "8px",
  } as const,

  label: {
    fontWeight: "bold",
    fontSize: "16px",
  } as const,

  value: {
    fontSize: "16px",
    marginBottom: "12px",
  } as const,
};
