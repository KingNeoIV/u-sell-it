/**
 * @fileoverview User Listings Management View.
 * Handles image fallbacks locally to prevent infinite re-render loops.
 */

import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

interface Listing {
  id: string;
  title: string;
  price: number;
  description: string;
  status: string;
  images: { file_path: string }[];
}

export default function MyListings() {
  const [listings, setListings] = useState<Listing[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMyListings = async () => {
      const token = localStorage.getItem("access_token");
      
      if (!token) {
        setLoading(false);
        return;
      }

      try {
        const response = await fetch("http://localhost:8000/listings/me", {
          headers: { 
            "Authorization": `Bearer ${token}` 
          },
        });

        if (response.ok) {
          const data = await response.json();
          setListings(data);
        } else {
          console.error("Failed to fetch user listings. Status:", response.status);
        }
      } catch (err) {
        console.error("Network error connecting to backend:", err);
      } finally {
        setLoading(false);
      }
    };

    fetchMyListings();
  }, []);

  // Helper to format image URLs correctly
  const getImageUrl = (path: string) => {
    if (path.startsWith('http')) return path;
    // Remove leading slash if it exists to prevent double slashes
    const cleanPath = path.startsWith('/') ? path.substring(1) : path;
    return `http://localhost:8000/${cleanPath}`;
  };

  if (loading) {
    return (
      <main style={styles.container}>
        <div style={styles.loadingState}>Loading your inventory...</div>
      </main>
    );
  }

  return (
    <main style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>My Listings</h1>
        <Link to="/listings/create" style={styles.addButton}>
          + Create New
        </Link>
      </header>

      {listings.length === 0 ? (
        <section style={styles.emptyState}>
          <div style={styles.emptyIcon}>📦</div>
          <p style={styles.text}>You haven't listed any items for sale yet.</p>
          <Link to="/listings/create" style={styles.ctaButton}>
            List Your First Item
          </Link>
        </section>
      ) : (
        <div style={styles.grid}>
          {listings.map((item) => (
            <div key={item.id} style={styles.card}>
              <div style={styles.imageContainer}>
                {item.images && item.images.length > 0 ? (
                  <img 
                    src={getImageUrl(item.images[0].file_path)} 
                    alt={item.title} 
                    crossOrigin="anonymous"
                    style={styles.image} 
                    onError={(e) => {
                      // Stop the loop: remove the handler so it doesn't fire again
                      e.currentTarget.onerror = null;
                      // Replace the source with a simple base64 placeholder or local asset
                      // This avoids fetching another external URL that might fail
                      e.currentTarget.src = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNkYAAAAAYAAjCB0C8AAAAASUVORK5CYII=";
                      // Optional: visually indicate failure
                      e.currentTarget.style.opacity = "0.3";
                    }}
                  />
                ) : (
                  <div style={styles.placeholderImage}>No Image Uploaded</div>
                )}
                <div style={styles.badge}>{item.status}</div>
              </div>
              
              <div style={styles.cardContent}>
                <h3 style={styles.cardTitle}>{item.title}</h3>
                <p style={styles.price}>${item.price.toFixed(2)}</p>
                <div style={styles.actions}>
                  <Link to={`/listings/edit/${item.id}`} style={styles.editBtn}>
                    Edit Details
                  </Link>
                  <Link to={`/listings/edit/${item.id}`} style={styles.uploadLink}>
                    Upload Image
                  </Link>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}
    </main>
  );
}

const styles = {
  container: { maxWidth: "1000px", margin: "100px auto 40px", padding: "20px", fontFamily: "Inter, system-ui, sans-serif" } as const,
  header: { display: "flex", justifyContent: "space-between", alignItems: "center", marginBottom: "40px" },
  title: { fontSize: "32px", fontWeight: "800", color: "#1a1a1a", margin: 0 },
  addButton: { padding: "12px 24px", background: "#28a745", color: "#fff", borderRadius: "10px", textDecoration: "none", fontWeight: "bold", boxShadow: "0 4px 12px rgba(40, 167, 69, 0.2)" },
  grid: { display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: "25px" },
  card: { background: "#fff", borderRadius: "16px", overflow: "hidden", border: "1px solid #eee", boxShadow: "0 4px 15px rgba(0,0,0,0.05)", transition: "transform 0.2s ease" },
  imageContainer: { position: "relative" as const, height: "200px", background: "#f8f9fa", overflow: "hidden" },
  image: { width: "100%", height: "100%", objectFit: "cover" as const },
  placeholderImage: { height: "100%", display: "flex", alignItems: "center", justifyContent: "center", color: "#999", fontSize: "14px", background: "#f0f0f0" },
  badge: { position: "absolute" as const, top: "10px", right: "10px", background: "rgba(0,0,0,0.6)", color: "#fff", padding: "4px 10px", borderRadius: "20px", fontSize: "12px", textTransform: "uppercase" as const },
  cardContent: { padding: "20px" },
  cardTitle: { fontSize: "18px", fontWeight: "700", color: "#333", marginBottom: "8px", whiteSpace: "nowrap" as const, overflow: "hidden", textOverflow: "ellipsis" },
  price: { fontSize: "20px", fontWeight: "800", color: "#007bff", marginBottom: "15px" },
  actions: { display: "flex", justifyContent: "space-between", alignItems: "center", borderTop: "1px solid #f0f0f0", paddingTop: "15px" },
  editBtn: { textDecoration: "none", color: "#555", fontSize: "14px", fontWeight: "600" },
  uploadLink: { textDecoration: "none", color: "#007bff", fontSize: "14px", fontWeight: "600" },
  emptyState: { textAlign: "center" as const, padding: "80px 20px", background: "#fff", borderRadius: "20px", border: "2px dashed #ddd" },
  emptyIcon: { fontSize: "50px", marginBottom: "20px" },
  text: { fontSize: "18px", color: "#666", marginBottom: "30px" },
  ctaButton: { padding: "14px 30px", background: "#007bff", color: "#fff", borderRadius: "8px", textDecoration: "none", fontWeight: "bold", boxShadow: "0 4px 12px rgba(0, 123, 255, 0.3)" },
  loadingState: { textAlign: "center" as const, padding: "100px", fontSize: "18px", color: "#666" }
};