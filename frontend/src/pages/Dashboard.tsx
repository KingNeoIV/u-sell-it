export default function Dashboard() {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Welcome to your dashboard!</h1>
      <p style={styles.text}>You are now logged in.</p>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "600px",
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

  text: {
    textAlign: "center",
    fontSize: "18px",
  } as const,
};
