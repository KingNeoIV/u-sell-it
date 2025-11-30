# ============= PyQt6 Imports =========================
from PyQt6.QtWidgets import(
    QApplication, 
    QWidget, 
    QLabel, 
    QLineEdit, 
    QPushButton,
    QVBoxLayout, 
    QHBoxLayout, 
    QFormLayout, 
    QMessageBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

# 
from ctypes import cdll, c_char_p, c_int
import os, sys

class RegisterScreen(QWidget):
    def handle_register(self):
        #check password confirmation
        if self.password.text() != self.confirm.text():
            QMessageBox.warning(self, "Error", "Passwords do not match.")
            return
        
        result = self.register_lib.register_user(
            self.first_name.text().encode('utf-8'),
            self.last_name.text().encode('utf-8'),
            self.street_address.text().encode('utf-8'),
            self.city.text().encode('utf-8'),
            self.state.text().encode('utf-8'),
            self.zip_code.text().encode('utf-8'),
            self.phone.text().encode('utf-8'),
            self.email.text().encode('utf-8'),
            self.username.text().encode('utf-8'),
            self.password.text().encode('utf-8'),
        )

        if result == 1:
            QMessageBox.information(self, "Sucess", "Registration successful!")
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Registration failed. Try again.")
            
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register -- u-sell-it")
        self.setFixedSize(1000, 700)
        self.setWindowIcon(QIcon("assets/u-sell-it_icon_black.ico"))
        
        # Load C++ DLL
        dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "demo_auth_login.dll"))

        if not os.path.exists(dll_path):
            raise FileNotFoundError(f"DLL not found at: {dll_path}")
        

        self.register_lib = cdll.LoadLibrary(dll_path)
        self.register_lib.register_user.argtypes = [c_char_p, c_char_p, c_char_p, c_char_p, c_char_p, 
                                                    c_char_p, c_char_p, c_char_p, c_char_p, c_char_p]
        self.register_lib.register_user.restype = c_int

        # =============== Left Panel ===============
        left_panel = QVBoxLayout()
        left_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Optional: Add a logo or image
        logo_label = QLabel()
        logo_label.setPixmap(QIcon("assets/u-sell-it_icon_black.png").pixmap(188, 188))
        logo_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Add welcome text
        welcome_text = QLabel("Welcome to the u-sell-it app!\nYour trusted local marketplace.\nBuy. Sell. Trade. Simple and secure.\n\n" \
            "\nCreate your free account to start listing items, \nbrowsing local deals, and connecting with trusted\nbuyers and sellers in your " \
            "community. Registration\nonly takes a minute and you'll be ready to\nroll the dice on your next great find.")
        welcome_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_text.setStyleSheet("font-size: 18px; font-weight: bold; color: #444;")

        left_panel.addWidget(logo_label)
        left_panel.addSpacing(20)
        left_panel.addWidget(welcome_text)

        left_panel.addStretch()

        left_widget = QWidget()
        left_widget.setLayout(left_panel)

        # ================= Right Panel =====================
        right_panel = QVBoxLayout()

        # Add "Form" header
        form_header = QLabel("Registration Form")
        form_header.setStyleSheet("font-size: 32px; font-weight: bold; color: #444; margin-bottom: 10px;")
        form_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # =============== Form Layout ========================
        form_layout = QFormLayout()

        # ======== First and Last name form ================
        name_row = QHBoxLayout()

        # First Name Column
        first_name_col = QVBoxLayout()
        first_label = QLabel("First Name:")
        first_label.setStyleSheet("font-size: 13px;")
        self.first_name = QLineEdit()
        self.first_name.setFixedWidth(240)
        self.first_name.setFixedHeight(28)
        self.first_name.setStyleSheet("font-size: 13px")
        first_name_col.addWidget(first_label)
        first_name_col.addWidget(self.first_name)

        # Last Name column
        last_name_col = QVBoxLayout()
        last_label = QLabel("Last Name:")
        last_label.setStyleSheet("font-size: 13px;")
        self.last_name = QLineEdit()
        self.last_name.setFixedWidth(220)
        self.last_name.setFixedHeight(28)
        self.last_name.setStyleSheet("font-size: 13px")
        last_name_col.addWidget(last_label)
        last_name_col.addWidget(self.last_name)
        
        # Add both columns side by side
        name_row.addLayout(first_name_col)
        name_row.addSpacing(20)                 # Space between first and last name
        name_row.addLayout(last_name_col)

        name_widget = QWidget()
        name_widget.setLayout(name_row)

        form_layout.addRow(name_widget)

        # ================ Email address: ===================
        email_row = QVBoxLayout()

        email_label = QLabel("Email address:")
        email_label.setStyleSheet("font-size: 13px;")
        self.email = QLineEdit()
        self.email.setFixedWidth(487)
        self.email.setFixedHeight(28)
        self.email.setStyleSheet("font-size: 13px")

        email_row.addWidget(email_label)
        email_row.addWidget(self.email)

        email_widget = QWidget()
        email_widget.setLayout(email_row)

        form_layout.addRow(email_widget)

        # ============= Street address: ===================
        street_address_row = QVBoxLayout()

        street_address_label = QLabel("Street address:")
        street_address_label.setStyleSheet("font-size: 13px;")
        self.street_address = QLineEdit()
        self.street_address.setFixedWidth(487)
        self.street_address.setFixedHeight(28)
        self.street_address.setStyleSheet("font-size: 13px;")

        street_address_row.addWidget(street_address_label)
        street_address_row.addWidget(self.street_address)

        street_address_widget = QWidget()
        street_address_widget.setLayout(street_address_row)

        form_layout.addRow(street_address_widget)

        # ============== City and State =====================
        city_state_row = QHBoxLayout()

        # City Column
        city_col = QVBoxLayout()
        city_label = QLabel("City:")
        city_label.setStyleSheet("font-size: 13px;")
        self.city = QLineEdit()
        self.city.setFixedWidth(240)
        self.city.setFixedHeight(28)
        self.city.setStyleSheet("font-size: 13px")
        city_col.addWidget(city_label)
        city_col.addWidget(self.city)

        # State Column
        state_col = QVBoxLayout()
        state_label = QLabel("State:")
        state_label.setStyleSheet("font-size: 13px;")
        self.state = QLineEdit()
        self.state.setFixedWidth(220)
        self.state.setFixedHeight(28)
        self.state.setStyleSheet("font-size: 13px")
        state_col.addWidget(state_label)
        state_col.addWidget(self.state)
        
        # Add both columns side by side
        city_state_row.addLayout(city_col)
        city_state_row.addSpacing(20)                 # Space between first and last name
        city_state_row.addLayout(state_col)

        city_state_widget = QWidget()
        city_state_widget.setLayout(city_state_row)

        form_layout.addRow(city_state_widget)

        # =============== Zip and Phone =================
        zip_phone_row = QHBoxLayout()

        # Zip Column
        zip_col = QVBoxLayout()
        zip_label = QLabel("Zip:")
        zip_label.setStyleSheet("font-size: 13px;")
        self.zip_code = QLineEdit()
        self.zip_code.setFixedWidth(240)
        self.zip_code.setFixedHeight(28)
        self.zip_code.setStyleSheet("font-size: 13px")
        zip_col.addWidget(zip_label)
        zip_col.addWidget(self.zip_code)

        # Phone Column
        phone_col = QVBoxLayout()
        phone_label = QLabel("Phone:")
        phone_label.setStyleSheet("font-size: 13px;")
        self.phone = QLineEdit()
        self.phone.setFixedWidth(220)
        self.phone.setFixedHeight(28)
        self.phone.setStyleSheet("font-size: 13px")
        phone_col.addWidget(phone_label)
        phone_col.addWidget(self.phone)
        
        # Add both columns side by side
        zip_phone_row.addLayout(zip_col)
        zip_phone_row.addSpacing(20)                 # Space between first and last name
        zip_phone_row.addLayout(phone_col)

        zip_dob_widget = QWidget()
        zip_dob_widget.setLayout(zip_phone_row)

        form_layout.addRow(zip_dob_widget)

        # ========== Username: =================
        username_row = QVBoxLayout()

        username_label = QLabel("Username:")
        username_label.setStyleSheet("font-size: 13px;")
        self.username = QLineEdit()
        self.username.setFixedWidth(487)
        self.username.setFixedHeight(28)
        self.username.setStyleSheet("font-size: 13px;")

        username_row.addWidget(username_label)
        username_row.addWidget(self.username)

        username_widget = QWidget()
        username_widget.setLayout(username_row)

        form_layout.addRow(username_widget)

        # ========== Password and Confirm ============
        password_confirm_row = QHBoxLayout()

        # Password Column
        password_col = QVBoxLayout()
        password_label = QLabel("Password:")
        password_label.setStyleSheet("font-size: 13px;")
        self.password = QLineEdit()
        self.password.setFixedWidth(240)
        self.password.setFixedHeight(28)
        self.password.setStyleSheet("font-size: 13px")
        password_col.addWidget(password_label)
        password_col.addWidget(self.password)

        # Confirm Column
        confirm_col = QVBoxLayout()
        confirm_label = QLabel("Confirm Password:")
        confirm_label.setStyleSheet("font-size: 13px;")
        self.confirm = QLineEdit()
        self.confirm.setFixedWidth(220)
        self.confirm.setFixedHeight(28)
        self.confirm.setStyleSheet("font-size: 13px")
        confirm_col.addWidget(confirm_label)
        confirm_col.addWidget(self.confirm)
        
        # Add both columns side by side
        password_confirm_row.addLayout(password_col)
        password_confirm_row.addSpacing(20)                 # Space between first and last name
        password_confirm_row.addLayout(confirm_col)

        password_confirm_widget = QWidget()
        password_confirm_widget.setLayout(password_confirm_row)

        form_layout.addRow(password_confirm_widget)

        # ============ Confirm Button =================
        self.confirm_btn = QPushButton("Confirm")
        self.confirm_btn.setFixedWidth(120)
        self.confirm_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                padding: 6px;
                border-radius: 5px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: #2893f5;
            }
            QPushButton:pressed {
                background-color: #005a9e;
                padding-top: 7px;
                padding-bottom: 5px;
            }
        """)
        self.confirm_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        btn_layout.addWidget(self.confirm_btn)
        btn_layout.addStretch()

        form_layout.addRow(btn_layout)

        self.confirm_btn.clicked.connect(self.handle_register)


        # Add spacing between header and form
        right_panel.addWidget(form_header)

        

        right_panel.addLayout(form_layout)

        right_panel.addStretch()

        right_widget = QWidget()
        right_widget.setLayout(right_panel)

        # ================ Main Layout ==================
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget, stretch=1)
        main_layout.addWidget(right_widget, stretch=5)

        self.setLayout(main_layout)


# Entry point for launching the application
if __name__ == "__main__":          
    app = QApplication(sys.argv)    # Create the applicatoin object
    window = RegisterScreen()          # Instantiate the login screen
    window.show()                   # Display the window
    sys.exit(app.exec())            # Start the even loop and exit cleanly