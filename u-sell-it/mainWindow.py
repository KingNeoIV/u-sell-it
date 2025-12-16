# mainWindow.py
from PyQt6.QtWidgets import (
    QWidget,
    QLabel,
    QVBoxLayout,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
    QToolBar,
    QToolButton,
    QMenu,
    QCheckBox,
    QGroupBox,
    QScrollArea,
    QRadioButton,
    QSlider,
    QComboBox,
    QListWidget,
    QGridLayout,
)
from PyQt6.QtGui import QIcon, QAction, QPixmap
from PyQt6.QtCore import Qt
import psycopg2


class MainWindow(QWidget):
    def keyPressEvent(self, event):
        # Allow pressing ESC to close the window
        if event.key() == Qt.Key.Key_Escape:
            self.close()

    def __init__(self):
        super().__init__()

        # ---------------- Window Setup ----------------
        self.setWindowTitle("u-sell-it Marketplace")
        self.setWindowIcon(QIcon("assets/u-sell-it_icon_black.ico"))
        self.setFixedSize(1200, 800)

        # ---------------- Main Layout ----------------
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)  # remove margins around the layout
        layout.setSpacing(0)

        # ---------------- Top Toolbar Area ----------------

        toolbar_container = QWidget()
        toolbar_container.setObjectName("toolbarContainer")
        toolbar_container.setFixedHeight(60)
        toolbar_container.setStyleSheet(
            """
            #toolbarContainer {
                background-color: #0064a3;   /* Blue background */
                border: 2px solid black;     /* Black outline only for the container */
            }
            """
        )

        # Layout for the toolbar inside the container
        toolbar_layout = QHBoxLayout(toolbar_container)
        toolbar_layout.setContentsMargins(10, 0, 10, 0)  # spacing inside the box
        toolbar_layout.setSpacing(15)  # spacing between buttons/fields

        # ---------- Leftside Top Toolbar ----------

        # Shared style for all toolbar buttons
        button_style = """
        QToolButton {
            background-color: #d3d3d3;   /* Light grey background */
            color: black;                /* Black text */
            font-size: 18px;             /* Larger font */
            border-radius: 5px;          /* Rounded corners */
            padding: 6px;                /* Inner padding */
        }
        QToolButton:hover {
            background-color: #c0c0c0;   /* Slightly darker grey on hover */
        }
        QToolButton:pressed {
            background-color: #a9a9a9;   /* Even darker grey when pressed */
        }
        """

        # Account dropdown
        account_btn = QToolButton()
        account_btn.setText("Account")
        account_btn.setFixedSize(100, 40)  # width=100px, height=40px
        account_btn.setStyleSheet(button_style)

        # Create the drop-down menu
        account_menu = QMenu(account_btn)
        account_menu.addAction("Profile")  # Example action
        account_menu.addAction("Settings")  # Example action
        account_menu.addAction("Logout")  # Example action

        # Style the dropdown menu background
        account_menu.setStyleSheet(
            """
            QMenu {
                background-color: #d3d3d3;   /* Light grey background */
                color: black;                /* Black text */
                font-size: 16px;             /* Slightly smaller font for menu items */
                border: 1px solid black;     /* Optional: thin border around menu */
            }
            QMenu::item:selected {
                background-color: #c0c0c0;   /* Slightly darker grey when hovered */
            }
            """
        )

        # Attach menu to the button
        account_btn.setMenu(account_menu)
        account_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        toolbar_layout.addWidget(account_btn)

        # Categories dropdown
        categories_btn = QToolButton()
        categories_btn.setText("Categories")
        categories_btn.setFixedSize(120, 40)  # width=120px, height=40px
        categories_btn.setStyleSheet(button_style)

        # Create the drop-down menu
        categories_menu = QMenu(categories_btn)
        categories_menu.addAction("Electronics")  # Example action
        categories_menu.addAction("Clothing")  # Example action
        categories_menu.addAction("Home\\Garden")  # Example action

        # Style the dropdown menu background
        categories_menu.setStyleSheet(
            """
            QMenu {
                background-color: #d3d3d3;   /* Light grey background */
                color: black;                /* Black text */
                font-size: 16px;             /* Slightly smaller font for menu items */
                border: 1px solid black;     /* Optional: thin border around menu */
            }
            QMenu::item:selected {
                background-color: #c0c0c0;   /* Slightly darker grey when hovered */
            }
            """
        )

        # Attach menu to the button
        categories_btn.setMenu(categories_menu)
        categories_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        toolbar_layout.addWidget(categories_btn)

        # Help dropdown
        help_btn = QToolButton()
        help_btn.setText("Help")
        help_btn.setFixedSize(100, 40)  # width=100px, height=40px
        help_btn.setStyleSheet(button_style)

        # Create the drop-down menu
        help_menu = QMenu(help_btn)
        help_menu.addAction("Documentation")  # Example action
        help_menu.addAction("FAQ")  # Example action
        help_menu.addAction("Contact Support")  # Example action

        # Style the dropdown menu background
        help_menu.setStyleSheet(
            """
            QMenu {
                background-color: #d3d3d3;   /* Light grey background */
                color: black;                /* Black text */
                font-size: 16px;             /* Slightly smaller font for menu items */
                border: 1px solid black;     /* Optional: thin border around menu */
            }
            QMenu::item:selected {
                background-color: #c0c0c0;   /* Slightly darker grey when hovered */
            }
            """
        )

        # Attach menu to the button
        help_btn.setMenu(help_menu)
        help_btn.setPopupMode(QToolButton.ToolButtonPopupMode.InstantPopup)

        toolbar_layout.addWidget(help_btn)

        toolbar_layout.addStretch()

        # ---------- Rightside Top Toolbar ----------

        # Search button
        search_btn = QPushButton("Search")
        search_btn.setFixedSize(100, 40)
        search_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        search_btn.clicked.connect(self.handle_search)

        # Darker blue style for Search button
        search_btn.setStyleSheet(
            """
            QPushButton {
                background-color: #2893f5;   /* Lighter, brighter blue */
                color: white;                /* White text for contrast */
                font-size: 18px;             /* Match other buttons */
                border-radius: 5px;
                padding: 6px;
            }
            QPushButton:hover {
                background-color: #2893f5;   /* Lighter blue on hover */
            }
            QPushButton:pressed {
                background-color: #003f73;   /* Even darker blue when pressed */
            }
            """
        )

        toolbar_layout.addWidget(search_btn)

        # Search field
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search listings...")
        self.search_input.setStyleSheet(
            "background-color: white; color: black; font-size: 16px; padding: 5px;"
        )
        self.search_input.setFixedSize(300, 40)  # width and height for a shorter box
        toolbar_layout.addWidget(self.search_input)

        # Add the styled container to the main layout
        layout.addWidget(toolbar_container)

        # ---------- Left Sidebar Area ----------
        # Create a horizontal layout for sidebar + main content
        content_layout = QHBoxLayout()
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(0)

        # Sidebar container
        sidebar_container = QWidget()
        sidebar_container.setObjectName("sidebarContainer")  # Scoped name
        sidebar_container.setFixedWidth(250)  # Sidebar width
        sidebar_container.setStyleSheet(
            """
            #sidebarContainer {
                background-color: #0064a3;   /* Match toolbar style */
                border: 2px solid black;     /* Black outline only for sidebar */
            }
            """
        )

        sidebar_layout = QVBoxLayout(sidebar_container)
        sidebar_layout.setContentsMargins(10, 10, 10, 10)
        sidebar_layout.setSpacing(15)

        # ---------------- Sidebar Filters ----------------

        # ---------------- Scrollable Category Box ----------------
        category_scroll = QScrollArea()
        category_scroll.setObjectName("categoryScroll")
        category_scroll.setFixedHeight(200)  # Adjust height as needed
        category_scroll.setStyleSheet(
            """
            #categoryScroll {
                background-color: #d3d3d3;   /* Blue background */
                border: 2px solid black;     /* Black trim only on outer frame */
                border-radius: 6px
            }
            """
        )

        # Inner container widget
        category_container = QWidget()
        category_container.setObjectName("categoryContainer")

        category_container.setStyleSheet(
            """
            #categoryContainer {
                background-color: #d3d3d3;   /* Blue background inside the box */
            }
            """
        )

        category_layout = QVBoxLayout(category_container)
        category_layout.setContentsMargins(10, 10, 10, 10)
        category_layout.setSpacing(8)

        # ---------- Radio Buttons ----------

        # Electronics
        self.electronics_rb = QRadioButton("Electronics")
        self.electronics_rb.setStyleSheet("color: black; font-size: 18px;")
        category_layout.addWidget(self.electronics_rb)

        # Books
        self.books_rb = QRadioButton("Books")
        self.books_rb.setStyleSheet("color: black; font-size: 18px;")
        category_layout.addWidget(self.books_rb)

        # Clothing
        self.clothing_rb = QRadioButton("Clothing")
        self.clothing_rb.setStyleSheet("color: black; font-size: 18px;")
        category_layout.addWidget(self.clothing_rb)

        # Outdoor
        self.outdoor_rb = QRadioButton("Outdoor")
        self.outdoor_rb.setStyleSheet("color: black; font-size: 18px;")
        category_layout.addWidget(self.outdoor_rb)

        # Home & Garden
        self.home_garden_rb = QRadioButton("Home & Garden")
        self.home_garden_rb.setStyleSheet("color: black; font-size: 18px;")
        category_layout.addWidget(self.home_garden_rb)

        # Toys & Games
        self.toys_rb = QRadioButton("Toys & Games")
        self.toys_rb.setStyleSheet("color: black; font-size: 18px;")
        category_layout.addWidget(self.toys_rb)

        # Beauty & Personal Care
        self.beauty_rb = QRadioButton("Personal Care")
        self.beauty_rb.setStyleSheet("color: black; font-size: 18px;")
        category_layout.addWidget(self.beauty_rb)

        # Automotive
        self.automotive_rb = QRadioButton("Automotive")
        self.automotive_rb.setStyleSheet("color: black; font-size: 18px;")
        category_layout.addWidget(self.automotive_rb)

        # Sports & Fitness
        self.sports_rb = QRadioButton("Sports & Fitness")
        self.sports_rb.setStyleSheet("color: black; font-size: 18px;")
        category_layout.addWidget(self.sports_rb)

        # Pet Supplies
        self.pet_supplies_rb = QRadioButton("Pet Supplies")
        self.pet_supplies_rb.setStyleSheet("color: black; font-size: 18px;")
        category_layout.addWidget(self.pet_supplies_rb)

        # Finalize scroll area
        category_scroll.setWidget(category_container)
        category_scroll.setWidgetResizable(True)

        # Add to sidebar
        sidebar_layout.addWidget(category_scroll)

        # Connect signals to a handler
        # self.electronics_cb.stateChanged.connect(self.handle_category_filter)
        # self.clothing_cb.stateChanged.connect(self.handle_category_filter)
        # self.home_cb.stateChanged.connect(self.handle_category_filter)

        # ---------------- Price Filter ----------------

        # Text box for manual price entry
        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Enter max price...")
        self.price_input.setStyleSheet(
            """
            QLineEdit {
                background-color: #ffffff;
                color: black;
                font-size: 16px;
                border: 1px solid black;
                border-radius: 4px;
                padding: 4px;
            }
            """
        )
        sidebar_layout.addWidget(self.price_input)

        # Slider for selecting price range
        self.price_slider = QSlider(Qt.Orientation.Horizontal)
        self.price_slider.setRange(0, 1000)  # Range: 0–1000
        self.price_slider.setTickInterval(50)  # Tick marks every 50
        self.price_slider.setTickPosition(QSlider.TickPosition.TicksBelow)  # <-- fixed
        self.price_slider.setStyleSheet(
            """
            QSlider::groove:horizontal {
                border: 1px solid #999999;
                height: 8px;
                background: #d3d3d3;
                margin: 2px 0;
            }
            QSlider::handle:horizontal {
                background: black;
                border: 1px solid white;
                width: 18px;
                margin: -4px 0;
                border-radius: 4px;
            }
            """
        )
        sidebar_layout.addWidget(self.price_slider)

        # Optional: connect slider to update text box
        self.price_slider.valueChanged.connect(
            lambda val: self.price_input.setText(str(val))
        )

        # ---------------- Favorite Sellers ----------------
        self.favorite_sellers_combo = QComboBox()
        self.favorite_sellers_combo.setObjectName("favoriteSellers")
        self.favorite_sellers_combo.setStyleSheet(
            """
            QComboBox {
                background-color: #ffffff;
                color: black;
                font-size: 16px;
                border: 1px solid black;
                border-radius: 4px;
                padding: 4px;
            }
            QComboBox QAbstractItemView {
                background-color: #d3d3d3;
                selection-background-color: #a0a0a0;
                color: black;
            }
            """
        )

        # Add a placeholder option first
        self.favorite_sellers_combo.addItem("Favorite Seller")

        # Add seller names
        self.favorite_sellers_combo.addItem("Michael Rios")
        self.favorite_sellers_combo.addItem("John Smith")
        self.favorite_sellers_combo.addItem("Emily Gallegos")
        self.favorite_sellers_combo.addItem("Trent Rodriguez")

        sidebar_layout.addWidget(self.favorite_sellers_combo)

        # Optional: connect selection change to a handler
        self.favorite_sellers_combo.currentTextChanged.connect(
            lambda val: print(
                "Selected favorite seller:", val if val else "No seller selected"
            )
        )

        # ---------------- Favorite Buyers ----------------
        self.favorite_buyer_combo = QComboBox()
        self.favorite_buyer_combo.setObjectName("favoriteBuyers")
        self.favorite_buyer_combo.setStyleSheet(
            """
            QComboBox {
                background-color: #ffffff;
                color: black;
                font-size: 16px;
                border: 1px solid black;
                border-radius: 4px;
                padding: 4px;
            }
            QComboBox QAbstractItemView {
                background-color: #d3d3d3;
                selection-background-color: #a0a0a0;
                color: black;
            }
            """
        )

        # Add a placeholder option first
        self.favorite_buyer_combo.addItem("Favorite Buyer")

        # Add seller names
        self.favorite_buyer_combo.addItem("Sophia Martinez")
        self.favorite_buyer_combo.addItem("James Carter")
        self.favorite_buyer_combo.addItem("Olivia Nguyen")
        self.favorite_buyer_combo.addItem("Ethan Brooks")
        self.favorite_buyer_combo.addItem("Ava Thompson")
        self.favorite_buyer_combo.addItem("Liam Hernandez")
        self.favorite_buyer_combo.addItem("Isabella Flores")
        self.favorite_buyer_combo.addItem("Noah Patel")
        self.favorite_buyer_combo.addItem("Mia Johnson")
        self.favorite_buyer_combo.addItem("Lucas Ramirez")

        sidebar_layout.addWidget(self.favorite_buyer_combo)

        # Optional: connect selection change to a handler
        self.favorite_buyer_combo.currentTextChanged.connect(
            lambda val: print(
                "Selected favorite buyer:", val if val else "No buyer selected"
            )
        )

        # ---------- Watchlist ----------
        watchlist_label = QLabel("Watchlist")
        watchlist_label.setStyleSheet(
            "color: white; font-size: 18px; font-weight: bold;"
        )
        sidebar_layout.addWidget(watchlist_label)

        # Input row: item name + target price
        watchlist_input_row = QWidget()
        watchlist_input_layout = QHBoxLayout(watchlist_input_row)
        watchlist_input_layout.setContentsMargins(0, 0, 0, 0)
        watchlist_input_layout.setSpacing(6)

        self.item_input = QLineEdit()
        self.item_input.setPlaceholderText("Item name...")
        self.item_input.setStyleSheet(
            "background-color: white; color: black; font-size: 14px; padding: 4px;"
        )
        watchlist_input_layout.addWidget(self.item_input)

        self.price_input = QLineEdit()
        self.price_input.setPlaceholderText("Target price")
        self.price_input.setStyleSheet(
            "background-color: white; color: black; font-size: 14px; padding: 4px;"
        )
        watchlist_input_layout.addWidget(self.price_input)

        self.add_watch_btn = QPushButton("Add")
        self.add_watch_btn.setStyleSheet(
            "background-color: #0064a3; color: white; font-weight: bold; padding: 4px;"
        )
        watchlist_input_layout.addWidget(self.add_watch_btn)

        sidebar_layout.addWidget(watchlist_input_row)

        # Watchlist display
        self.watchlist_display = QListWidget()
        self.watchlist_display.setStyleSheet(
            "background-color: #d3d3d3; color: black; font-size: 14px;"
        )
        sidebar_layout.addWidget(self.watchlist_display)

        # Add item to watchlist on button click
        def add_to_watchlist():
            item = self.item_input.text().strip()
            price = self.price_input.text().strip()
            if item and price:
                self.watchlist_display.addItem(f"{item} — Target: ${price}")
                self.item_input.clear()
                self.price_input.clear()

        self.add_watch_btn.clicked.connect(add_to_watchlist)

        # Add sidebar to content layout
        content_layout.addWidget(sidebar_container)

        # ---------- Main Content Area ----------

        # Temporary test data (replace with get_items() later)
        items = [
            (
                "9000 Watt Dual Champion Generator",
                "items/9000_Watt_Dual_Champion.png",
                899.99,
            ),
            ("Hello Kitty Plush", "items/Hello_kitty.png", 29.99),
            ("HP Laptop", "items/HP_Laptop.png", 699.99),
            ("iPhone 17", "items/IPhone_17.png", 999.99),
            ("Murder at Holly House", "items/Murder_at_Holly_House.png", 14.99),
            ("Party Pooper Game", "items/Partypooper.png", 19.99),
            ("V-Neck Sweater Dress", "items/V_Neck_Sweater_Dress.png", 49.99),
            ("Welding Cutting Torch", "items/Welding_Cutting_Torch.png", 129.99),
        ]

        # Create a grid layout for product cards
        grid_widget = QWidget()
        grid_layout = QGridLayout(grid_widget)

        row, col = 0, 0
        for title, image_path, price in items:
            # Image
            pixmap = QPixmap(image_path).scaled(
                200,
                200,
                Qt.AspectRatioMode.KeepAspectRatio,
                Qt.TransformationMode.SmoothTransformation,
            )
            image_label = QLabel()
            image_label.setPixmap(pixmap)
            image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Title
            title_label = QLabel(title)
            title_label.setStyleSheet("font-size: 14px; font-weight: bold;")
            title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Price
            price_label = QLabel(f"${price:.2f}")
            price_label.setStyleSheet("font-size: 12px; color: green;")
            price_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

            # Place Bid button
            bid_button = QPushButton("Place Bid")
            bid_button.setStyleSheet(
                "background-color: #0078D7; color: white; padding: 5px;"
            )

            # Vertical box for card
            vbox = QVBoxLayout()
            vbox.addWidget(image_label)
            vbox.addWidget(title_label)
            vbox.addWidget(price_label)
            vbox.addWidget(bid_button)

            product_widget = QWidget()
            product_widget.setLayout(vbox)
            product_widget.setStyleSheet(
                "border: 1px solid #ccc; border-radius: 5px; padding: 10px;"
            )

            # Add card to grid
            grid_layout.addWidget(product_widget, row, col)

            col += 1
            if col > 1:  # 2 items per row
                col = 0
                row += 1

        # Scroll area to hold the grid
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setWidget(grid_widget)

        # Add scroll area to main content
        content_layout.addWidget(scroll_area)

        # Add content layout to the main vertical layout (below toolbar)
        layout.addLayout(content_layout)

        # ---------------- Reference Points ----------------
        # TODO: Add product grid (scrollable listings with bid buttons)

    # ---------------- Toolbar Handlers ----------------
    def handle_search(self):
        query = self.search_input.text()
        # TODO: Hook into product grid filtering
        print(f"Searching for: {query}")

    def open_account_menu(self):
        # TODO: Replace with Account menu logic
        print("Account menu clicked")

    def open_categories_menu(self):
        # TODO: Replace with Categories menu logic
        print("Categories menu clicked")

    def open_help_menu(self):
        # TODO: Replace with Help menu logic
        print("Help menu clicked")


# Entry point for standalone testing
if __name__ == "__main__":
    from PyQt6.QtWidgets import QApplication
    import sys

    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
