/**
 * @fileoverview Finalized View component for the u-sell-it marketplace.
 * Handles the two-stage submission process:
 * 1. Creates the listing record to generate a UUID.
 * 2. Uploads the image to /images/{listing_id} as a path parameter.
 */

import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";

interface Category {
  id: string;
  name: string;
}

export default function CreateListing() {
  const navigate = useNavigate();
  
  // Component State
  const [categories, setCategories] = useState<Category[]>([]);
  const [loading, setLoading] = useState(false);
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [imagePreview, setImagePreview] = useState<string | null>(null);
  
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    price: "",
    category_id: "",
  });

  // Fetch categories on component mount
  useEffect(() => {
    fetch("http://localhost:8000/categories")
      .then((res) => res.json())
      .then((data) => setCategories(data))
      .catch((err) => console.error("Error fetching categories:", err));
  }, []);

  const handleTextChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0] || null;
    setSelectedFile(file);

    // Update the UI preview
    if (file) {
      const reader = new FileReader();
      reader.onloadend = () => setImagePreview(reader.result as string);
      reader.readAsDataURL(file);
    } else {
      setImagePreview(null);
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);

    // Retrieve token stored by Login.tsx
    const token = localStorage.getItem("access_token");

    if (!token) {
      alert("You must be logged in to create a listing.");
      setLoading(false);
      return;
    }

    try {
      // PHASE 1: Create the Listing record
      const listingResponse = await fetch("http://localhost:8000/listings", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`,
        },
        body: JSON.stringify({
          ...formData,
          price: parseFloat(formData.price),
          status: "active",
        }),
      });

      if (!listingResponse.ok) {
        const error = await listingResponse.json();
        throw new Error(error.detail || "Failed to create listing");
      }

      const newListing = await listingResponse.json();
      const newListingId = newListing.id;

      // PHASE 2: Upload Image to /{listing_id} Path
      if (selectedFile) {
        const imageFormData = new FormData();
        imageFormData.append("file", selectedFile); 

        // Correct URL format: http://localhost:8000/images/[UUID]
        const imageResponse = await fetch(`http://localhost:8000/images/${newListingId}`, {
          method: "POST",
          headers: {
            "Authorization": `Bearer ${token}`,
            // Do NOT set Content-Type header here; browser does it for FormData
          },
          body: imageFormData,
        });

        if (!imageResponse.ok) {
          const imgError = await imageResponse.json();
          console.error("Image failed to link to listing:", imgError);
          alert("Listing created, but image upload failed.");
        }
      }

      alert("Success! Your item is live.");
      navigate("/dashboard");

    } catch (err: any) {
      alert(`Error: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <main style={styles.container}>
      <header style={styles.header}>
        <h1 style={styles.title}>Create Listing</h1>
        <p style={styles.subtitle}>List your item on the u-sell-it marketplace</p>
      </header>
      
      <form onSubmit={handleSubmit} style={styles.form}>
        <div style={styles.inputGroup}>
          <label style={styles.label}>Title</label>
          <input
            name="title"
            required
            style={styles.input}
            placeholder="What are you selling?"
            onChange={handleTextChange}
          />
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Category</label>
          <select 
            name="category_id" 
            required 
            style={styles.input} 
            onChange={handleTextChange}
          >
            <option value="">Select a Category</option>
            {categories.map((cat) => (
              <option key={cat.id} value={cat.id}>{cat.name}</option>
            ))}
          </select>
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Price ($)</label>
          <input
            name="price"
            type="number"
            step="0.01"
            required
            style={styles.input}
            placeholder="0.00"
            onChange={handleTextChange}
          />
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Image Upload</label>
          <input 
            type="file" 
            accept="image/*" 
            onChange={handleFileChange} 
            style={styles.fileInput}
          />
          {imagePreview && (
            <img src={imagePreview} alt="Preview" style={styles.preview} />
          )}
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Description</label>
          <textarea
            name="description"
            required
            style={{ ...styles.input, minHeight: "120px", resize: "vertical" }}
            placeholder="Provide details about condition, age, etc."
            onChange={handleTextChange}
          />
        </div>

        <button type="submit" disabled={loading} style={styles.button}>
          {loading ? "Publishing..." : "Publish Listing"}
        </button>
      </form>
    </main>
  );
}

const styles = {
  container: {
    maxWidth: "550px",
    margin: "60px auto",
    padding: "40px",
    background: "#ffffff",
    borderRadius: "16px",
    boxShadow: "0 10px 30px rgba(0,0,0,0.1)",
    fontFamily: "Inter, sans-serif",
  } as const,
  header: {
    textAlign: "center" as const,
    marginBottom: "30px",
  },
  title: {
    fontSize: "28px",
    fontWeight: "800",
    color: "#1a1a1a",
    margin: "0 0 8px 0",
  },
  subtitle: {
    color: "#666",
    fontSize: "14px",
  },
  form: {
    display: "flex",
    flexDirection: "column" as const,
    gap: "20px",
  },
  inputGroup: {
    display: "flex",
    flexDirection: "column" as const,
    gap: "8px",
  },
  label: {
    fontSize: "13px",
    fontWeight: "600",
    color: "#444",
    textTransform: "uppercase" as const,
    letterSpacing: "0.5px",
  },
  input: {
    padding: "12px 16px",
    borderRadius: "8px",
    border: "1px solid #e0e0e0",
    fontSize: "16px",
    outline: "none",
    transition: "border-color 0.2s",
  },
  fileInput: {
    fontSize: "14px",
  },
  preview: {
    marginTop: "12px",
    width: "100%",
    maxHeight: "280px",
    objectFit: "cover" as const,
    borderRadius: "10px",
    border: "1px solid #eee",
  },
  button: {
    marginTop: "10px",
    padding: "16px",
    borderRadius: "8px",
    border: "none",
    background: "#007bff",
    color: "#fff",
    fontSize: "16px",
    fontWeight: "bold",
    cursor: "pointer",
    boxShadow: "0 4px 12px rgba(0, 123, 255, 0.3)",
  },
};