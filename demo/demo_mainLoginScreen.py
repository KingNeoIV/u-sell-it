from PyQt6.QtWidgets import (   # Import selected PyQt6 widget classes for building the login screen UI
    QApplication,               # Controls the event loop and overall GUI application lifecycle 
    QWidget,                    # Base class for all windows and UI containers
    QLabel,                     # Display text or images
    QLineEdit,                  # Editable text field (used for username and password)
    QPushButton,                # Clickable button widget
    QVBoxLayout,                # Layout manager that stacks widgets vertically
    QHBoxLayout,                # Layout manager that arranges widgets horizontally
    QMessageBox                 # Popup dailog for messages (info, warnings, confirmations)
)

from demo_registerUI import RegisterScreen        # Imports your custom registration screen class
from demo_forgotPassUI import ForgotPasswordUI
from PyQt6.QtGui import (QPixmap, QIcon)     # QPixmap handles images, QIcon handle the window icon
from PyQt6.QtCore import Qt                  # Provides constants (alignment, key codes, cursor shapes)
from ctypes import cdll, c_char_p, c_int     # Lets Python call into C++ DLL functions
import os                                    # For filesystems paths
import sys                                   # Used to exit the application cleanly

class LoginScreen(QWidget):                                                             # Define a custom LoginScreen class that inherits QWidget to function as the main login window
    def keyPressEvent(self, event):                                                     # Override QWidget's keyPressEvent to handle keyboard input (e.g., Escape key for exit prompt)
        if event.key() == Qt.Key.Key_Escape:                                            # Check if the pressed key is Escape by comparing the event's key code to Qt's Escape constant
            reply = QMessageBox.question                                                # Create a confirmation dialog using QMessageBox.question and store the user's response in 'reply'
            (                                                                           # Opening parenthesis starts the grouped list of items to import, allowing multi-line formatting
                self,                                                                   # 'self' refers to the current LoginScreen instance, giving access to its attributs and methods
                "Exit Application",                                                     # The dialog window title text shoen at the top of the confirmation box
                "Are you sure you want to exit?",                                       # The message text displayed inside the confirmation dialog asking if the user wants to quit
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No          # Specify the dialog options by combining Yes and No buttons with a bitwise OR so both appear in the confrimation box
            )                                                                           # Closing parenthesis ends the grouped multi-line import list, completing the statement
            if reply == QMessageBox.StandardButton.Yes:                                 # If the user clicked 'Yes' in the confirmation dialog, proceed with the exit action
                self.close()                                                            # Close the current LoginScreen window, effectively exiting the application

    def handle_login(self):                                                             # Define the handle_login method to process user input and control the login flow
        username = self.username.text().encode('utf-8')                                 # Retrive the text from the username input field and encode it as UTF-8 bytes for processing/storage
        password = self.password.text().encode('utf-8')                                 # Retrive the text form the password input field and encode it as UTF-8 bytes for processing/storage

        result = self.login_lib.validate_login(username, password)                      # Call the validate_login function form the login_lib to check if the provided username and password are correct

        if result == 1:                                                                 # If the validate_login returned 1, it means the credentials are valid and the login is successful
            QMessageBox.information(self, "Login", "Login successful!")                 # Display an information dialog titled "Login" to notify the user that the login was successful
            # TODO: Open dashboard screen                                               # Placeholder: after successful login, transition to the main dashbord screen
        else:                                                                           # If the login validation failed (result not equal to 1), handle the unsuccessful login case
            QMessageBox.warning(self, "Login", "Invalid username or password.")         # Show a warning dialog titled "Login" to inform the user that their credentials are invalid
    
    def open_register_screen(self):                                                     # Define the open_register_screen method to launch the registration window when the user chooses to sign up
        self.register_window = RegisterScreen()                                         # Create a new instance of the RegistrationScreen window and assing it to self.register_window
        self.register_window.show()                                                     # Display the registration window on the screen so the user can begin creating an account

    def open_forgot_password_screen(self):
        self.forgot_window = ForgotPasswordUI()
        self.forgot_window.show()

    def __init__(self):                                                         # Constructor method that initializes the LoginScreen object and sets up its starting state
        super().__init__()                                                      # Call the parent class constructor to ensure proper initialization of inherited functionality
        self.setWindowIcon(QIcon("assets/u-sell-it_icon_black.ico"))            # Set the window's icon to custom "u-sell-it" image from the assests folder
        self.setWindowTitle("u-sell-it")                                        # Set the windows's title text to "u-sell-it", shown in the title bar of the application window
        self.setFixedSize(600, 900)                                             # Fix the window size to 600x900 pixels, preventing the user from resizing the application window
        self.wallpaper = QLabel(self)                                       # Create a QLabel widget as a child of the window to serve as the wallpaper background
        self.wallpaper.setPixmap(QPixmap("assets/LoginScreen2v2.png")       # Load and set the "LoginScreen2v2.png" image from the assets folder as the wallpaper background
            .scaled(self.size(), Qt.AspectRatioMode.IgnoreAspectRatio))     # Scale the wallpaper image to match the window size, ignoring the orginal aspect ratio
        self.wallpaper.setGeometry(0, 0, 600, 900)                          # Postition and size the wallpaper QLabel to cover the entire 600x900 window area

        main_layout = QVBoxLayout(self)                                     # Create a vertical box layout for the window, stacking child widgets top to bottom

        welcome_label_1 = QLabel("Welcome")                                 # Create a QLabel widget displaying the text "Welcome" to greet the user on the login screen
        welcome_label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)          # Align the "Welcome" label text to the center of the window for a balanced, polished look
        welcome_label_1.setStyleSheet("""                                   
            font-size: 50px;
            font-weight: bold;
            color: white;
            margin-top: -5px;
        """)                                                            # Apply custom CSS styling to the "Welcome" label to control its font, color, and appearance
        main_layout.addWidget(welcome_label_1)                          # Add the centered "Welcome" label to the main vertical layout so it appears at the top of the IO

        welcome_label_2 = QLabel("To")                                  # Create a QLabel displaying the word "To" as the second part of the welcome message
        welcome_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)      # Center-align the "To" label text to maintain consistent visual flow in the stacked welcome message
        welcome_label_2.setStyleSheet("""
            font-size: 50px;
            font-weight: bold;
            color: white;
            margin-top: -20px;
        """)                                                            # Apply custom CSS styling to the "Welcome" label to control its font, color, and appearance
        main_layout.addWidget(welcome_label_2)                          # Add the "To" label to the main layout, stacking it below the "Welcome" label for a smooth greeting flow

        welcome_label_3 = QLabel("Please login!")                       # Create a QLabel displaying "Please login!" to prompt the user to begin the authentication process
        welcome_label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)      # Center-align the "Please login!" label to keep the welcome message visually balanced and user-focused
        welcome_label_3.setStyleSheet("""
            font-size: 50px;
            font-weight: bold;
            color: white;
            margin-top: 375px;
        """)                                                            # Apply custom CSS styling to the "Welcome" label to control its font, color, and appearance
        main_layout.addWidget(welcome_label_3)                          # Add the "Please login!" label to the layout, completing the stacked welcome message above the login form

        main_layout.addStretch()                                        # Add flexible vertival space below the welcome labels to push login fields toward the bottom of the window

        self.overlay = QWidget(self)                                                                        # Create a transparent overlay widget on top of the main window for layering additional UI elements
        self.overlay.setGeometry(150, 600, 300, 200)                                                        # Position the overlay widget at (150, 600) with the size 300x200 for diaplaying content above the background
        self.overlay.setStyleSheet("background-color: rgba(255, 255, 255, 40); border-radius: 15px")        # Style the overlay with semi-transparent white and rounded corners for a soft, modern panel effect

        login_layout = QVBoxLayout()                                    # Create a vertical layout to stack login form elements (username, password, buttons) top to bottom

        self.username = QLineEdit(self)                                 # Create a text input field for the username entry in the login form
        self.username.setPlaceholderText("Username:")                   # Set a placeholder text in the username field to guide users jon what to enter
        self.username.setStyleSheet(""" 
            QLineEdit {
                padding: 5px;
                font-size: 17px;
                min-width: 250px;
                height: 30px;
            }
        """)                                                            # Style the username field for consistent sizing, readable font, and comfortable padding in the login form
        self.username.returnPressed.connect(self.handle_login)          # Trigger login handler when Enter is pressed in the username field for smoother user experience
        login_layout.addWidget(self.username)                           # Add the username input field to the login layout for vertical stacking with elements   

        self.password = QLineEdit()                                     # Create a text input field for password entry in the login form
        self.password.setPlaceholderText("Password:")                   # Set placeholder text in the password field to prompt users for their login credentials
        self.password.setEchoMode(QLineEdit.EchoMode.Password)          # Mask password input with asterisks to protect user privacy during login
        self.password.setStyleSheet("""
            QLineEdit {
                padding: 5px;
                font-size: 17px;
                min-width: 250px;
                height: 30px;
            }
        """)                                                            # Style the password field for consistent sizing, readable font, and comfortable padding in the login form
        self.password.returnPressed.connect(self.handle_login)          # Trigger login handler when Enter is pressed in the password field for faster form submission
        login_layout.addWidget(self.password)                           # Add the password input field to the login layout for vertical stacking beneath the username field

        button_row = QHBoxLayout()                                      # Create a horizontal layout to arrange login buttons side by side (e.g. Login and Register)

        self.login_btn = QPushButton("Login")                           # Create a Login button to initiate credential varification when clicked
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
        """)                                                            # Style the Login button with a modern blue theme, hover glow, and pressed depth effect for tectile feedback            
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)     # Change cursor to a pointing hand when hovering over the Login button to signal it's clickable
        button_row.addWidget(self.login_btn)                                                        # Add the Login button to the horizontal button row for side-by-side alignment with other actions
        self.login_btn.clicked.connect(self.handle_login)                                           # Connect the Login button click to the login handler to verify credentials when pressed

        dll_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "demo_auth_login.dll")) # Resolve the absolute path to the auth_login.dll for dynamic loading in the login workflow
        self.login_lib = cdll.LoadLibrary(dll_path)                                                 # Load the compiled C++ DLL to access native authentication functions for secure login processing

        self.login_lib.validate_login.argtypes = [c_char_p, c_char_p]           # Define argument types for validate_login to accept username and password as C-style strings
        self.login_lib.validate_login.restype = c_int                           # Specify return type of validate_login as integere to interpret success/failure codesd from the DLL

        self.register_btn = QPushButton("Register")                             # Create a Register button to allow new users to initiate account creation
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
        """)                                                                    # Style the Register button to match the Login button with consistant color, hover, and press effects
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)          # Set cursor to pointing hand on Register button to indicate it's interactive and clickable
        button_row.addWidget(self.register_btn)                                 # Add the Register button to the horizontal layout for side-by-side placement with the login button
        self.register_btn.clicked.connect(self.open_register_screen)            # Connect the Register button click to the screen transition handler for launching the account creation form

        self.forgot_btn = QPushButton("Forgot Password")                        # Create a Forgot Password button to guide users through credential recovery if they've lost access
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
        """)                                                                # Style the Forgot button to match the Login button with consistant color, hover, and press effects
        self.forgot_btn.setCursor(Qt.CursorShape.PointingHandCursor)        # Set cursor to pointing hand on Forgot Password button to signal it's clickable and interactive
        button_row.addWidget(self.forgot_btn)                               # Add the Forgot Password button to the horizontal layout to complete the action row with recovery support
        self.forgot_btn.clicked.connect(self.open_forgot_password_screen)

        login_layout.addLayout(button_row)                                  # Insert the button row into the main login layout to organize all action buttons within the form structure

        self.overlay.setLayout(login_layout)                                # Apply the login layout to the overlay widget to structure all form elements within the visible interface

if __name__ == "__main__":          # Entry point for launching the login interface when the script is run directly
    app = QApplication(sys.argv)    # Initialize the Qt application to manage GUI event handling and widget lifecycle
    window = LoginScreen()          # Instantiate the LoginScreen widget to initialize and display the login interface
    window.show()                   # Display the LoginScreen window to render the interface and begin user interaction
    sys.exit(app.exec())            # Start the Qt event loop and exit the application cleanly when the login window is closed