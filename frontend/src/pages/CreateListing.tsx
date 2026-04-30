/**
 * @fileoverview View component for the marketplace listing creation process.
 * This component handles the form submission and validation for new user listings.
 */

// import React from "react";

/**
 * CreateListing Page.
 * * * Features:
 * - Form for product details, pricing, and category selection.
 * - Multi-part image upload (planned).
 * - Integration with the Listing API.
 * * @returns {JSX.Element} The rendered listing creation view.
 */
export default function CreateListing() {
  return (
    <main style={styles.container} aria-labelledby="create-listing-title">
      <h1 id="create-listing-title" style={styles.title}>
        Create New Listing
      </h1>
      <section style={styles.formPlaceholder}>
        <p style={styles.text}>
          The listing creation form is currently under construction. 
          Please check back soon to start selling on U-SELL-IT.
        </p>
      </section>
    </main>
  );
}

/**
 * Component-specific styles.
 * Layout note: 'margin-top' accounts for the 70px fixed navbar.
 */
const styles = {
  container: {
    maxWidth: "600px",
    margin: "100px auto 40px", // Increased top margin to clear the fixed Navbar
    padding: "40px",
    background: "#ffffff", // Switched to white for a cleaner "card" feel
    borderRadius: "12px",
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

  formPlaceholder: {
    padding: "40px 20px",
    border: "2px dashed #e0e0e0",
    borderRadius: "8px",
    background: "#fafafa",
  },

  text: {
    textAlign: "center" as const,
    fontSize: "16px",
    color: "#666",
    lineHeight: "1.5",
  },
};