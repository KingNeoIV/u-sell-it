/**
 * @fileoverview User Listings Management View.
 * Displays a filtered list of products owned by the authenticated user.
 * Provides entry points for editing, deleting, or creating new marketplace entries.
 */

// import React from "react";
import { Link } from "react-router-dom";

/**
 * MyListings Page.
 * * * Features:
 * - Empty state handling with a Call to Action (CTA).
 * - Grid/List view of user-owned inventory (planned).
 * - Direct navigation to the creation form.
 * * @returns {JSX.Element} The rendered listings management view.
 */
export default function MyListings() {
  // Logic note: In production, you will fetch listings from the API here.
  const hasListings = false;

  return (
    <main style={styles.container} aria-labelledby="my-listings-title">
      <h1 id="my-listings-title" style={styles.title}>
        My Listings
      </h1>

      {!hasListings ? (
        <section style={styles.emptyState}>
          <p style={styles.text}>You haven't listed any items for sale yet.</p>
          <Link to="/listings/create" style={styles.ctaButton}>
            + Create Your First Listing
          </Link>
        </section>
      ) : (
        <div>{/* Mapping logic for active listings will go here */}</div>
      )}
    </main>
  );
}

/**
 * Component-specific styles.
 * Layout note: Uses margin-top to clear fixed navigation.
 */
const styles = {
  container: {
    maxWidth: "800px", // Slightly wider to accommodate list items better later
    margin: "100px auto 40px",
    padding: "40px",
    background: "#ffffff",
    borderRadius: "16px",
    border: "1px solid #eee",
    boxShadow: "0 4px 20px rgba(0,0,0,0.05)",
  } as const,

  title: {
    textAlign: "center" as const,
    marginBottom: "30px",
    fontSize: "28px",
    fontWeight: "800",
    color: "#333",
  },

  emptyState: {
    display: "flex",
    flexDirection: "column" as const,
    alignItems: "center",
    padding: "60px 20px",
    textAlign: "center" as const,
  },

  text: {
    fontSize: "18px",
    color: "#666",
    marginBottom: "24px",
  },

  ctaButton: {
    display: "inline-block",
    padding: "12px 24px",
    background: "#007bff",
    color: "#fff",
    textDecoration: "none",
    borderRadius: "8px",
    fontWeight: "700",
    fontSize: "15px",
    boxShadow: "0 4px 12px rgba(0, 123, 255, 0.3)",
    transition: "transform 0.2s ease",
  } as const,
};