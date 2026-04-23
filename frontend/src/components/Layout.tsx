import Navbar from "./Navbar";

export default function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div>
      <Navbar />
      <div style={styles.content}>{children}</div>
    </div>
  );
}

const styles = {
  content: {
    padding: "20px",
  } as const,
};
