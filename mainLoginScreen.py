# Import all necessary PyQt6 modules for building the UI
from PyQt6.QtWidgets import (
    QApplication,       # Manages the GUI application's control flow 
    QWidget,            # Base class for all windows and containers
    QLabel,             # Display text or images
    QLineEdit,          # Editable text field (used for username and password)
    QPushButton,        # Clickable button
    QVBoxLayout,        # Vertical layout manager
    QHBoxLayout,         # Horizontal layout manager
    QMessageBox
)

from PyQt6.QtGui import (QPixmap, QIcon)     # QPixmap handles images, QIcon handle the window icon
from PyQt6.QtCore import Qt                  # Provides alignment and other core constants
from ctypes import cdll, c_char_p, c_int
import os
import sys                                   # Used to exit the application cleanly

# Define the main login screen class
class LoginScreen(QWidget):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            reply = QMessageBox.question(
                self,
                "Exit Application",
                "Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.close()

    def handle_login(self):
        # Get text from input fields
        username = self.username.text().encode('utf-8')
        password = self.password.text().encode('utf-8')

        # Call the C++ DLL function
        result = self.login_lib.validate_login(username, password)

        # Handle result
        if result == 1:
            print("Login successful!")
            # TODO: Transition to next screen or show success massage

        else:
            print("Login failed!")
            # TODO: Show error message or shake overlay

    def __init__(self):
        super().__init__()                                                      #Initialize the QWidget base class

        # Window setup
        self.setWindowIcon(QIcon("assets/u-sell-it_icon.ico"))                  # Set the window icon
        self.setWindowTitle("u-sell-it")                                        # Title bar text
        self.setFixedSize(600, 900)                                             # Fixed window size

        #BackGround wallpaper
        self.wallpaper = QLabel(self)                                       # QLabel to hold the background image
        self.wallpaper.setPixmap(QPixmap("assets/LoginScreen2v2.png")       # Load image from assets folder
            .scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio))     # Scale to fit window
        self.wallpaper.setGeometry(0, 0, 600, 900)                          # Position image to cover full window

        # Main layout for welcome text and spacing
        main_layout = QVBoxLayout(self)

        # Welcome label 1: "Welcome"
        welcome_label_1 = QLabel("Welcome")
        welcome_label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label_1.setStyleSheet("""
            font-size: 50px;
            font-weight: bold;
            color: white;
            margin-top: -5px;
        """)
        main_layout.addWidget(welcome_label_1)

        # Welcome label 2: "To"
        welcome_label_2 = QLabel("To")
        welcome_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label_2.setStyleSheet("""
            font-size: 50px;
            font-weight: bold;
            color: white;
            margin-top: -20px;
        """)
        main_layout.addWidget(welcome_label_2)

        # Welcome label 3: "Please login!"
        welcome_label_3 = QLabel("Please login!")
        welcome_label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label_3.setStyleSheet("""
            font-size: 50px;
            font-weight: bold;
            color: white;
            margin-top: 375px;
        """)
        main_layout.addWidget(welcome_label_3)

        # Spacer to push overlay lower
        main_layout.addStretch()

        
        # Overlay Container
        self.overlay = QWidget(self)
        self.overlay.setGeometry(150, 600, 300, 200)    # Manually postitioned
        self.overlay.setStyleSheet("background-color: rgba(255, 255, 255, 40); border-radius: 15px")

        # Layout for login form inside overlay
        login_layout = QVBoxLayout()

        # Username input field
        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Username:")
        self.username.setStyleSheet(""" 
            QLineEdit {
                padding: 5px;
                font-size: 17px;
                min-width: 250px;
                height: 30px;
            }
        """)
        self.username.returnPressed.connect(self.handle_login)
        login_layout.addWidget(self.username)

        # Password input field
        self.password = QLineEdit()
        self.password.setPlaceholderText("Password:")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)  # Hide Character
        self.password.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                font-size: 17px;
                min-width: 250px;
                height: 30px;
            }
        """)
        self.password.returnPressed.connect(self.handle_login)
        login_layout.addWidget(self.password)

        # Horizontal layout for buttons
        button_row = QHBoxLayout()

        # Login button
        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet("""
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
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        button_row.addWidget(self.login_btn)
        self.login_btn.clicked.connect(self.handle_login)

        # Load the C++ DLL
        dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "login_logic.dll"))
        self.login_lib = cdll.LoadLibrary(dll_path)

        # Define argument and return types
        self.login_lib.validate_login.argtypes = [c_char_p, c_char_p]
        self.login_lib.validate_login.restype = c_int

        # Register button
        self.register_btn = QPushButton("Register")
        self.register_btn.setStyleSheet("""
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
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        button_row.addWidget(self.register_btn)
        self.register_btn.clicked.connect(self.handle_login)

        # Forgot Password button
        self.forgot_btn = QPushButton("Forgot Password")
        self.forgot_btn.setStyleSheet("""
            QPushButton {
                background-color: #0078D7;
                color: white;
                min-width: 130px;
                padding: 6px;
                border-radius: 5px;
                font-size:  18px;
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
        self.forgot_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        button_row.addWidget(self.forgot_btn)
        self.forgot_btn.clicked.connect(self.handle_login)

        # Add button row to login layout
        login_layout.addLayout(button_row)

        # Apply login layout to overlay container
        self.overlay.setLayout(login_layout)

# Entry point for launching the application
if __name__ == "__main__":          
    app = QApplication(sys.argv)    # Create the applicatoin object
    window = LoginScreen()          # Instantiate the login screen
    window.show()                   # Display the window
    sys.exit(app.exec())            # Start the even loop and exit cleanly