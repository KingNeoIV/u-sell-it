export default function CreateListing() {
  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Create Listing</h1>
      <p style={styles.text}>Listing creation form will go here.</p>
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

  text: {
    textAlign: "center",
    fontSize: "18px",
  } as const,
};
