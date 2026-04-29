import { useAuth } from "../hooks/useAuth";

export default function Dashboard() {
  // Hook to handle authentication status
  useAuth();

  // Mock data to simulate items in your marketplace grid
  const items = Array(9).fill({
    name: "Product Item",
    price: "$129.00",
  });

  return (
    /* pageWrapper: The outer container that holds the sidebar and main content side-by-side */
    <div style={styles.pageWrapper}>
      
      {/* --- LEFT SIDEBAR: Browsing & Filtering Logic --- */}
      <aside style={styles.sidebar}>
        <div style={styles.filterContent}>
          <p style={styles.sidebarHeader}>Marketplace Filters</p>
          
          {/* Category Section: Uses checkboxes for multi-selection */}
          <div style={styles.filterGroup}>
            <p style={styles.filterLabel}>Category</p>
            <div style={styles.checkList}>
              <label style={styles.checkItem}><input type="checkbox" defaultChecked /> Electronics</label>
              <label style={styles.checkItem}><input type="checkbox" /> Vehicles</label>
              <label style={styles.checkItem}><input type="checkbox" /> Home Decor</label>
            </div>
          </div>

          {/* Price Section: A range slider for quick budget filtering */}
          <div style={styles.filterGroup}>
            <p style={styles.filterLabel}>Price Range</p>
            <input type="range" style={styles.slider} min="0" max="1000" />
            <div style={styles.priceLabels}><span>$0</span><span>$1k+</span></div>
          </div>

          {/* Sort Section: Dropdown for organization */}
          <div style={styles.filterGroup}>
            <p style={styles.filterLabel}>Sort By</p>
            <select style={styles.select}>
              <option>Newest First</option>
              <option>Price: Low to High</option>
            </select>
          </div>
        </div>
      </aside>

      {/* --- MAIN CONTENT AREA: Displays the actual marketplace products --- */}
      <main style={styles.mainArea}>
        {/* Note: We don't put a Header here anymore because the Navbar.tsx 
            is 'fixed' to the top of the entire browser window.
        */}
        
        {/* contentScroll: Makes only the product grid scrollable, keeping sidebar/topbar pinned */}
        <div style={styles.contentScroll}>
          <div style={styles.grid}>
            {/* Loop through our mock items and render a 'Card' for each one */}
            {items.map((item, index) => (
              <div key={index} style={styles.card}>
                {/* Visual placeholder for the product image */}
                <div style={styles.cardImg}>
                   <span style={styles.imgText}>ITEM_PREVIEW</span>
                </div>
                
                {/* Card footer containing details and price */}
                <div style={styles.cardBody}>
                  <div>
                    <h4 style={styles.itemName}>{item.name}</h4>
                    <p style={styles.itemPrice}>{item.price}</p>
                  </div>
                  <button style={styles.detailsBtn}>Details</button>
                </div>
              </div>
            ))}
          </div>
        </div>
      </main>
    </div>
  );
}

const styles = {
  pageWrapper: {
    height: "100vh", // Lock height to viewport
    width: "100vw",
    display: "flex", // Puts Sidebar and Main Area next to each other
    background: "#f8f9fa",
    fontFamily: "'Inter', sans-serif",
    overflow: "hidden", // Prevents the whole page from scrolling (only the grid should scroll)
    paddingTop: "30px", // CRITICAL: Makes room for the fixed top Navbar
  } as const,

  sidebar: {
    width: "260px",
    background: "#fff",
    borderRight: "1px solid #eee",
    display: "flex",
    flexDirection: "column" as const,
  } as const,

  filterContent: { 
    padding: "25px", 
    flex: 1, 
    overflowY: "auto" as const // Allows the filter list to scroll if it gets too long
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
    gap: "8px" 
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
    flex: 1, // Tells this section to take up all remaining width
    display: "flex", 
    flexDirection: "column" as const 
  },

  contentScroll: { 
    flex: 1, 
    overflowY: "auto" as const, // This makes the product grid scrollable
    padding: "30px" 
  },

  grid: { 
    display: "grid", 
    gridTemplateColumns: "repeat(3, 1fr)", // Creates the 3-column marketplace look
    gap: "25px" 
  },

  card: { 
    background: "#fff", 
    borderRadius: "12px", 
    border: "1px solid #eee", 
    overflow: "hidden" 
  },

  cardImg: { 
    height: "160px", 
    background: "#f8f9fa", 
    display: "flex", 
    alignItems: "center", 
    justifyContent: "center" 
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