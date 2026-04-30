import React, { useState, useEffect } from "react";
import { useParams, useNavigate } from "react-router-dom";

interface Listing {
  title: string;
  price: number;
  description: string;
  status: string;
  category_id: string; // FIX: Added this to satisfy backend requirements
}

export default function EditListing() {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  
  const [formData, setFormData] = useState<Listing>({
    title: "",
    price: 0,
    description: "",
    status: "active",
    category_id: "" // FIX: Added initial state
  });

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [loading, setLoading] = useState(true);
  const [message, setMessage] = useState("");

  const token = localStorage.getItem("access_token");

  // 1. Fetch current data on load
  useEffect(() => {
    const fetchListing = async () => {
      try {
        const response = await fetch(`http://localhost:8000/listings/${id}`, {
          headers: { "Authorization": `Bearer ${token}` }
        });
        if (response.ok) {
          const data = await response.json();
          // FIX: Capture category_id from the existing record
          setFormData({
            title: data.title || "",
            price: data.price || 0,
            description: data.description || "",
            status: data.status || "active",
            category_id: data.category_id || "" 
          });
        }
      } catch (err) {
        console.error("Failed to fetch listing:", err);
      } finally {
        setLoading(false);
      }
    };
    fetchListing();
  }, [id, token]);

  // 2. Handle Text Update
  const handleUpdateDetails = async (e: React.FormEvent) => {
    e.preventDefault();
    setMessage("Updating...");

    const payload = {
      title: formData.title,
      description: formData.description,
      price: Number(formData.price),
      status: formData.status,
      category_id: formData.category_id // FIX: Sent to satisfy "Field required"
    };

    try {
      const response = await fetch(`http://localhost:8000/listings/${id}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
          "Authorization": `Bearer ${token}`
        },
        body: JSON.stringify(payload)
      });

      if (response.ok) {
        setMessage("✅ Details updated successfully!");
      } else {
        const errorData = await response.json();
        console.error("BACKEND VALIDATION ERROR:", errorData.detail);
        
        // Formats the error "body -> category_id: Field required" for the UI
        const errorMsg = Array.isArray(errorData.detail) 
          ? `${errorData.detail[0].loc[1]}: ${errorData.detail[0].msg}`
          : "Failed to update details.";
          
        setMessage(`❌ ${errorMsg}`);
      }
    } catch (err) {
      setMessage("❌ Network error.");
    }
  };

  // 3. Handle Image Upload
  const handleImageUpload = async () => {
    if (!selectedFile) return;
    setMessage("Uploading image...");

    const uploadData = new FormData();
    uploadData.append("file", selectedFile);

    try {
      const response = await fetch(`http://localhost:8000/images/${id}`, {
        method: "POST",
        headers: { "Authorization": `Bearer ${token}` },
        body: uploadData
      });

      if (response.ok) {
        setMessage("✅ Image uploaded successfully!");
        setSelectedFile(null);
      } else {
        setMessage("❌ Upload failed.");
      }
    } catch (err) {
      setMessage("❌ Network error during upload.");
    }
  };

  if (loading) return <div style={styles.container}>Loading item data...</div>;

  return (
    <main style={styles.container}>
      <button onClick={() => navigate("/listings")} style={styles.backBtn}>← Back to My Listings</button>
      
      <h1 style={styles.title}>Edit Listing</h1>
      {message && <div style={styles.alert}>{message}</div>}

      <div style={styles.flexContainer}>
        {/* SECTION: Details Form */}
        <section style={styles.card}>
          <h3 style={styles.sectionTitle}>Item Details</h3>
          <form onSubmit={handleUpdateDetails} style={styles.form}>
            <div style={styles.inputGroup}>
              <label style={styles.label}>Title</label>
              <input 
                type="text" 
                value={formData.title} 
                onChange={(e) => setFormData({...formData, title: e.target.value})} 
                style={styles.input}
              />
            </div>
            
            <div style={styles.inputGroup}>
              <label style={styles.label}>Price ($)</label>
              <input 
                type="number" 
                step="0.01"
                value={formData.price} 
                onChange={(e) => setFormData({...formData, price: parseFloat(e.target.value)})} 
                style={styles.input}
              />
            </div>

            <div style={styles.inputGroup}>
              <label style={styles.label}>Description</label>
              <textarea 
                value={formData.description} 
                onChange={(e) => setFormData({...formData, description: e.target.value})} 
                style={styles.textarea}
              />
            </div>
            
            <button type="submit" style={styles.saveBtn}>Save Changes</button>
          </form>
        </section>

        {/* SECTION: Image Upload */}
        <section style={styles.card}>
          <h3 style={styles.sectionTitle}>Add / Update Image</h3>
          <div style={styles.uploadBox}>
            <p style={styles.helpText}>Select a new photo to replace or add to this listing.</p>
            <input 
              type="file" 
              accept="image/*" 
              onChange={(e) => setSelectedFile(e.target.files ? e.target.files[0] : null)} 
              style={styles.fileInput}
            />
            <button 
              onClick={handleImageUpload} 
              disabled={!selectedFile}
              style={{...styles.uploadBtn, opacity: selectedFile ? 1 : 0.5}}
            >
              Upload Selected Image
            </button>
          </div>
        </section>
      </div>
    </main>
  );
}

const styles = {
  container: { maxWidth: "1000px", margin: "80px auto", padding: "20px", fontFamily: "sans-serif" },
  title: { fontSize: "32px", fontWeight: "bold", marginBottom: "30px" },
  sectionTitle: { fontSize: "18px", fontWeight: "bold", marginBottom: "20px" },
  flexContainer: { display: "grid", gridTemplateColumns: "1.2fr 0.8fr", gap: "30px" },
  card: { padding: "30px", background: "#fff", borderRadius: "16px", boxShadow: "0 4px 20px rgba(0,0,0,0.08)", border: "1px solid #f0f0f0" },
  form: { display: "flex", flexDirection: "column" as const, gap: "20px" },
  inputGroup: { display: "flex", flexDirection: "column" as const, gap: "8px" },
  label: { fontSize: "12px", fontWeight: "bold", color: "#666", textTransform: "uppercase" as const },
  input: { padding: "12px", borderRadius: "8px", border: "1px solid #ddd", fontSize: "16px" },
  textarea: { padding: "12px", borderRadius: "8px", border: "1px solid #ddd", minHeight: "120px", fontSize: "16px" },
  saveBtn: { padding: "15px", background: "#007bff", color: "#fff", border: "none", borderRadius: "8px", fontWeight: "bold", cursor: "pointer" },
  uploadBox: { display: "flex", flexDirection: "column" as const, gap: "20px" },
  helpText: { fontSize: "14px", color: "#777" },
  fileInput: { fontSize: "14px" },
  uploadBtn: { padding: "12px", background: "#28a745", color: "#fff", border: "none", borderRadius: "8px", fontWeight: "bold", cursor: "pointer" },
  backBtn: { background: "none", border: "none", color: "#007bff", cursor: "pointer", marginBottom: "15px", fontSize: "16px" },
  alert: { padding: "15px", background: "#f0f7ff", color: "#0056b3", borderRadius: "10px", marginBottom: "30px", borderLeft: "5px solid #007bff" }
};