/**
 * @fileoverview Main layout wrapper component.
 * Provides a persistent navigation structure and consistent spacing for all page content.
 */

import React from "react";
import Navbar from "./Navbar";

/**
 * Props for the Layout component.
 * @property children - The page-specific content to be rendered within the layout.
 */
interface LayoutProps {
  children: React.ReactNode;
}

/**
 * A higher-order component that wraps the application's page content.
 * Ensures the Navbar is always present and children are contained within a consistent container.
 * * @example
 * <Layout>
 * <HomePage />
 * </Layout>
 */
export default function Layout({ children }: LayoutProps) {
  return (
    <div style={styles.container}>
      <Navbar />
      <main style={styles.content}>
        {children}
      </main>
    </div>
  );
}

/**
 * Component-specific styles.
 * Note: In a production environment, these might be replaced by CSS Modules or Tailwind.
 */
const styles = {
  container: {
    display: "flex",
    flexDirection: "column" as const,
    minHeight: "100vh", // Ensures the layout covers the full screen height
  },
  content: {
    padding: "20px",
    flex: 1, // Allows the content to grow and push footers down if added later
  } as const,
};