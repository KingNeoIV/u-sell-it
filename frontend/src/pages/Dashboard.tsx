/**
 * @fileoverview Main Marketplace Dashboard.
 * Features a dual-pane layout with a sticky filtering sidebar and a scrollable 
 * product discovery grid.
 */

import { useState, useEffect } from "react";
import { useAuth } from "../hooks/useAuth";

/**
 * Dashboard Component.
 * * * Layout Architecture:
 * - Uses Flexbox for a sidebar-main relationship.
 * - Employs 'hidden' overflow on the root to create an "App-like" feel where 
 * individual columns scroll independently.
 * - Integrated with `useAuth` to ensure session validity on mount.
 */
export default function Dashboard() {
  /** * Validates authentication state.
   * Note: If useAuth handles redirection internally, this ensures 
   * the dashboard is protected.
   */
  useAuth();

  /** Mock data for marketplace grid rendering */
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchListings = async () => {
      try {
        const response = await fetch("http://localhost:8000/listings/");
        const data = await response.json();
        setItems(data);
      } catch (error) {
        console.error("Failed to fetch:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchListings();
  }, []);

  return (
    <div style={styles.pageWrapper}>
      
      {/* --- SIDEBAR: Filtering Logic --- */}
      <aside style={styles.sidebar} aria-label="Marketplace Filters">
        <div style={styles.filterContent}>
          <header style={styles.sidebarHeader}>Marketplace Filters</header>
          
          {/* Category Section */}
          <section style={styles.filterGroup}>
            <p style={styles.filterLabel}>Category</p>
            <div style={styles.checkList} role="group" aria-label="Categories">
              <label style={styles.checkItem}>
                <input type="checkbox" defaultChecked /> Electronics
              </label>
              <label style={styles.checkItem}>
                <input type="checkbox" /> Vehicles
              </label>
              <label style={styles.checkItem}>
                <input type="checkbox" /> Home Decor
              </label>
            </div>
          </section>

          {/* Price Section */}
          <section style={styles.filterGroup}>
            <label htmlFor="price-range" style={styles.filterLabel}>Price Range</label>
            <input 
              id="price-range"
              type="range" 
              style={styles.slider} 
              min="0" 
              max="1000" 
            />
            <div style={styles.priceLabels}>
              <span>$0</span>
              <span>$1k+</span>
            </div>
          </section>

          {/* Sort Section */}
          <section style={styles.filterGroup}>
            <label htmlFor="sort-by" style={styles.filterLabel}>Sort By</label>
            <select id="sort-by" style={styles.select}>
              <option>Newest First</option>
              <option>Price: Low to High</option>
            </select>
          </section>
        </div>
      </aside>

      {/* --- MAIN CONTENT AREA: Product Grid --- */}
      <main style={styles.mainArea} aria-label="Marketplace Products">
        <div style={styles.contentScroll}>
          
          {/* --- CONDITIONAL LOGIC STARTS HERE --- */}
          {loading ? (
            <div style={{ textAlign: 'center', marginTop: '50px', color: '#666' }}>
              <h3>Loading your marketplace...</h3>
            </div>
          ) : (
            /* This only renders when loading is false */
            <div style={styles.grid} role="list">
              {items.map((item) => (
                <article key={item.id} style={styles.card} role="listitem">
                  <div style={styles.cardImg}>
                    {item.images && item.images.length > 0 ? (
                      <img 
                        src={item.images[0].file_path} 
                        alt={item.title} 
                        style={{ 
                          width: '100%', 
                          height: '100%', 
                          objectFit: 'contain' }} 
                      />
                    ) : (
                      <span style={styles.imgText}>NO IMAGE</span>
                    )}
                  </div>
                  
                  <div style={styles.cardBody}>
                    <div>
                      <h4 style={styles.itemName}>{item.title}</h4>
                      <p style={styles.itemPrice}>${item.price}</p>
                    </div>
                    <button 
                      style={styles.detailsBtn} 
                      aria-label={`View details for ${item.title}`}
                    >
                      Details
                    </button>
                  </div>
                </article>
              ))}
            </div>
          )}
          {/* --- CONDITIONAL LOGIC ENDS HERE --- */}

        </div>
      </main>
    </div>
  );
}

/**
 * Component Styles
 * Using 'as const' to ensure TypeScript treats these as specific CSS values.
 */
const styles = {
  pageWrapper: {
    position: "fixed" as const,
    height: "100vh",
    width: "100vw", // Changed to 100% to avoid vw scrollbar issues
    display: "flex",
    background: "#f8f9fa",
    fontFamily: "'Inter', sans-serif",
    overflow: "hidden", 
    paddingTop: "40px", // Matched to Navbar height for consistency
    boxSizing: "border-box",
  } as const,

  sidebar: {
    width: "220px",
    background: "#fff",
    borderRight: "1px solid #eee",
    display: "flex",
    flexDirection: "column" as const,
    height: "calc(100vh - 40px)",
    position: "relative",
    top: 0,
    overflowY: "auto" as const,
    overflowX: "hidden" as const,
    zIndex: 100,
  } as const,

  filterContent: { 
    padding: "25px", 
    flex: 1, 
    overflowY: "auto" as const 
  },

  sidebarHeader: { 
    fontSize: "11px", 
    fontWeight: "800", 
    color: "#bbb", 
    textTransform: "uppercase" as const, 
    marginBottom: "20px" 
  },

  filterGroup: { 
    marginBottom: "30px" 
  },

  filterLabel: { 
    display: "block",
    fontSize: "14px", 
    fontWeight: "700", 
    marginBottom: "12px", 
    color: "#333" 
  },
  
  checkList: { 
    display: "flex", 
    flexDirection: "column" as const, 
    gap: "10px" 
  },

  checkItem: { 
    fontSize: "13px", 
    color: "#666", 
    cursor: "pointer", 
    display: "flex", 
    gap: "8px",
    alignItems: "center"
  },
  
  slider: { 
    width: "100%", 
    accentColor: "#007bff" 
  },

  priceLabels: { 
    display: "flex", 
    justifyContent: "space-between", 
    fontSize: "11px", 
    color: "#999", 
    marginTop: "5px" 
  },
  
  select: { 
    width: "100%", 
    padding: "8px", 
    borderRadius: "6px", 
    border: "1px solid #ddd" 
  },

  mainArea: { 
    flex: 1, 
    display: "flex", 
    flexDirection: "column" as const,
    height: "100%",
    overflow: "hidden", 
  },

  contentScroll: { 
    flex: 1, 
    overflowY: "auto" as const, 
    padding: "30px",
    height: "100%", 
    paddingBottom: "50px",
    WebkitOverflowScrolling: "touch" as const,
  },

  grid: { 
    display: "grid", 
    // Responsive grid: will drop to 2 or 1 columns on smaller screens
    gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))", 
    gap: "25px" 
  },

  card: { 
    background: "#fff", 
    borderRadius: "12px", 
    border: "1px solid #eee", 
    overflow: "hidden",
    transition: "transform 0.2s ease-in-out",
  },

  cardImg: { 
    height: "200px", 
    background: "#f8f9fa", 
    display: "flex", 
    alignItems: "center", 
    justifyContent: "center",
    padding: "10px", 
  },

  imgText: { 
    color: "#ddd", 
    fontSize: "12px", 
    fontWeight: "bold" 
  },
  
  cardBody: { 
    padding: "15px", 
    display: "flex", 
    justifyContent: "space-between", 
    alignItems: "center" 
  },
  
  itemName: { 
    margin: 0, 
    fontSize: "15px", 
    fontWeight: "700" 
  },

  itemPrice: { 
    margin: 0, 
    color: "#007bff", 
    fontWeight: "800" 
  },

  detailsBtn: { 
    background: "#1a1a1b", 
    color: "#fff", 
    border: "none", 
    padding: "6px 12px", 
    borderRadius: "6px", 
    fontSize: "12px", 
    fontWeight: "600", 
    cursor: "pointer" 
  }
};