# ============= PyQt6 Imports =========================
from PyQt6.QtWidgets import(
    QApplication, QWidget, QLabel, QLineEdit, QPushButton,
    QVBoxLayout, QHBoxLayout, QFormLayout, QMessageBox
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt

# 
from ctypes import cdll, c_char_p, c_int
import os, sys

class RegisterScreen(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Register -- u-sell-it")
        self.setFixedSize(1000, 600)
        self.setWindowIcon(QIcon("assets/u-sell-it_icon.ico"))
        
        # Load C++ DLL
        dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "auth_login.dll"))

        if not os.path.exists(dll_path):
            raise FileNotFoundError(f"DLL not found at: {dll_path}")
        

        self.register_lib = cdll.LoadLibrary(dll_path)
        self.register_lib.register_user.argtypes = [c_char_p, c_char_p, c_char_p]
        self.register_lib.register_user.restype = c_int

        # Form Layout

        form_layout = QFormLayout()

        self.first_name = QLineEdit()
        self.last_name = QLineEdit()
        
        name_row = QHBoxLayout()
        name_row.addWidget(QLabel("First Name:"))
        name_row.addWidget(self.first_name)
        name_row.addWidget(QLabel("Last Name:"))
        name_row.addWidget(self.last_name)

        name_widget = QWidget()
        name_widget.setLayout(name_row)
        form_layout.addRow(name_widget)

        #

        self.email = QLineEdit()
        form_layout.addRow("Email:", self.email)

        self.phone = QLineEdit()
        form_layout.addRow("Phone:", self.phone)

        self.street_address = QLineEdit()
        form_layout.addRow("Street Address:", self.street_address)


        # 
        self.city = QLineEdit()
        self.zip_code = QLineEdit()
        
        city_row = QHBoxLayout()
        city_row.addWidget(QLabel("City:"))
        city_row.addWidget(self.city)
        city_row.addWidget(QLabel("Zip:"))
        city_row.addWidget(self.zip_code)

        city_widget = QWidget()
        city_widget.setLayout(city_row)
        form_layout.addRow(city_widget)


        self.username = QLineEdit()
        form_layout.addRow("Username:", self.username)

        self.password = QLineEdit()
        self.confirm_password = QLineEdit()
        
        password_row = QHBoxLayout()
        password_row.addWidget(QLabel("Password:"))
        password_row.addWidget(self.password)
        password_row.addWidget(QLabel("Confirm Password:"))
        password_row.addWidget(self.confirm_password)

        password_widget = QWidget()
        password_widget.setLayout(password_row)
        form_layout.addRow(password_widget)

        #self.setLayout(form_layout)

        # =============== Left Panel ===============
        left_panel = QVBoxLayout()
        left_panel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Optional: Add a logo or image
        logo_label = QLabel()
        logo_label.setPixmap(QIcon("assets/u-sell-it_icon.ico").pixmap(128, 128))
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
        form_header.setStyleSheet("font-size: 22px; font-weight: bold; margin-bottom: 10px;")
        form_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        right_panel.addWidget(form_header)
        right_panel.addLayout(form_layout)

        right_panel.addStretch()

        right_widget = QWidget()
        right_widget.setLayout(right_panel)

        # ================ Main Layout ==================
        main_layout = QHBoxLayout()
        main_layout.addWidget(left_widget, stretch=1)
        main_layout.addWidget(right_widget, stretch=1)

        self.setLayout(main_layout)


# Entry point for launching the application
if __name__ == "__main__":          
    app = QApplication(sys.argv)    # Create the applicatoin object
    window = RegisterScreen()          # Instantiate the login screen
    window.show()                   # Display the window
    sys.exit(app.exec())            # Start the even loop and exit cleanly