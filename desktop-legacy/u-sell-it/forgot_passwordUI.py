from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QPushButton,
    QStackedWidget,
    QMessageBox,
    QGraphicsOpacityEffect,
)
from PyQt6.QtGui import QPixmap, QIcon, QShortcut
from PyQt6.QtCore import Qt, QPropertyAnimation, QSize, QTimer
import os, ctypes

# ==================== DLL Setup ====================

# Load the external C++ DLL (auth_login.dll) so Python can call its functions
dll_full_path = os.path.join(os.path.dirname(__file__), "auth_login.dll")
dll_path = ctypes.CDLL(dll_full_path)

# Define the function signature for validate_contact inside the DLL
dll_path.validate_contact.argtypes = [
    ctypes.c_char_p
]  # takes a string (email or phone)
dll_path.validate_contact.restype = (
    ctypes.c_int
)  # returns an int (1 = found, 0 = not found)

# Define the function signature for generate_demo_code inside the DLL
dll_path.generate_demo_code.argtypes = []  # takes no arguments
dll_path.generate_demo_code.restype = ctypes.c_char_p  # returns a const char* (string)

# Define the function signature for validate_demo_code inside the DLL
dll_path.validate_demo_code.argtypes = [ctypes.c_char_p]  # takes the entered code
dll_path.validate_demo_code.restype = (
    ctypes.c_int
)  # returns 1 if valid, 0 if invalid/expired

# Define the function signature for get_demo_code_remaining_time inside the DLL
dll_path.get_demo_code_remaining_time.argtypes = []  # takes no arguments
dll_path.get_demo_code_remaining_time.restype = (
    ctypes.c_int
)  # returns remaining seconds (0 if expired)

dll_path.update_password_by_contact.argtypes = [
    ctypes.c_char_p,
    ctypes.c_char_p,
    ctypes.c_char_p,
]
dll_path.update_password_by_contact.restype = ctypes.c_int


class ForgotPasswordUI(QWidget):
    # ==================== Keyboard Handling ====================

    def keyPressEvent(self, event):
        # If the user presses ESC, close the Forgot Password window

        if event.key() == Qt.Key.Key_Escape:
            self.close()

    # ==================== Email Validation ====================

    def check_email_and_proceed(self):
        # Get the email entered by the user

        email = self.email_input.text().strip()
        if not email:
            # Show warning if empty

            QMessageBox.warning(self, "Error", "Please enter an email address.")
            return

        # Call DLL function to check if email exists in database

        found = dll_path.validate_contact(email.encode("utf-8"))
        if found == 1:
            # If email exists, animate transition to next page (index 1)

            self.animateTransition(1)
        else:
            # Otherwise, show error message

            QMessageBox.warning(self, "Error", "Email or Phone not found in database.")

    # ==================== Code Entry Helpers ====================

    def move_focus(self, idx, text):
        """Move cursor to next box when current box is filled"""
        if text:  # if user typed something
            next_idx = idx + 1
            if next_idx < len(self.code_inputs):
                self.code_inputs[next_idx].setFocus()

    # ==================== Demo Code Validation & Timer ==========

    def check_code_complete(self):
        """
        Enable the Submit button only when all 6 input boxes are filled with digits.
        This prevents the user from submitting an incomplete or non-numeric code.
        """
        code = "".join([box.text() for box in self.code_inputs])
        if len(code) == 6 and code.isdigit():
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)

    def check_code_complete(self):
        # Alternate implementation: checks each box individually
        # If all boxes contain digits, enable the Submit button
        if all(box.text().isdigit() for box in self.code_inputs):
            self.submit_button.setEnabled(True)
        else:
            self.submit_button.setEnabled(False)

    def on_submit(self):
        """
        Called when the user clicks Submit.
        - Collects the 6-digit code entered by the user.
        - Passes it to the C++ DLL (validate_demo_code).
        - Shows a success message if the code matches and is still valid.
        - Shows an error message if the code is incorrect or expired.
        """
        entered_code = "".join(box.text() for box in self.code_inputs)
        result = dll_path.validate_demo_code(entered_code.encode("utf-8"))

        if result == 1:
            QMessageBox.information(self, "Success", "Code validated successfully!")
            # Move to Page 3 (New Password form)

            self.animateTransition(3)
        else:
            QMessageBox.warning(self, "Invalid", "Code is incorrect or expired.")

    def start_timer_ui(self):
        """
        Starts a countdown timer that updates the label every second.
        Uses QTimer to call update_timer_label() once per second.
        """
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_timer_label)
        self.timer.start(1000)

    def update_timer_label(self):
        """
        Updates the timer label with the number of seconds remaining.
        - Calls into the C++ DLL (get_demo_code_remaining_time).
        - If time remains, shows "Code expires in X seconds".
        - If expired, stops the timer, disables Submit, and updates the label.
        """
        remaining = dll_path.get_demo_code_remaining_time()
        if remaining > 0:
            self.timer_label.setText(f"Code expires in {remaining} seconds")
        else:
            self.timer.stop()
            self.timer_label.setText("Code expired. Please request a new code.")
            self.submit_button.setEnabled(False)

    def on_password_submit(self):
        new_pass = self.new_password_input.text()
        confirm_pass = self.confirm_password_input.text()

        result = dll_path.update_password_by_contact(
            self.current_contact.encode("utf-8"),
            new_pass.encode("utf-8"),
            confirm_pass.encode("utf-8"),
        )

        if result == -1:
            self.feedback_label.setText("Both fields are required.")
        elif result == -2:
            self.feedback_label.setText("Passwords do not match.")
        elif result == -3:
            self.feedback_label.setText("Password must be at least 8 characters.")
        elif result == -4:
            self.feedback_label.setText("Password is not strong enough.")
        elif result == -5:
            self.feedback_label.setText("Invalid contact format.")
        elif result == 1:
            self.feedback_label.setStyleSheet("font-size: 14px; color: green;")
            self.feedback_label.setText("Password updated successfully!")

            # Show a quick confirmation

            QMessageBox.information(self, "Success", "Password updated successfully!")

            # Close only this ForgotPasswordUI window

            self.close()
        else:
            self.feedback_label.setText("An error occurred while updating password.")

    # ==================== Constructor ====================

    def __init__(self):
        super().__init__()

        # Window setup

        self.setWindowIcon(QIcon("assets/u-sell-it_icon_black.ico"))
        self.setWindowTitle("Forgot Password")
        self.setFixedSize(450, 500)

        # Stack widget holds multiple pages (page0, page1, etc.)

        self.stack = QStackedWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        # ---------- Page 0: Forgot password form ----------

        page0 = QWidget()
        top_layout = QVBoxLayout(page0)
        top_layout.setSpacing(25)

        # Image at the top

        forgot_password_image = QLabel(self)
        pixmap = QPixmap("assets/reset-password.png")
        pixmap = pixmap.scaled(
            175,
            175,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        forgot_password_image.setPixmap(pixmap)
        forgot_password_image.setAlignment(Qt.AlignmentFlag.AlignHCenter)

        # Title text

        forgot_pass_widget = QLabel("Forgot\nPassword", self)
        forgot_pass_widget.setStyleSheet("font-weight: bold; font-size: 30px;")
        forgot_pass_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Instructions text

        instructions_label = QLabel(
            "Please enter your account's phone number or\nemail address and we will send you a verification code.",
            self,
        )
        instructions_label.setStyleSheet("font-size: 16px; color: gray;")
        instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Email input field

        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email/Phone number")
        self.email_input.setStyleSheet("font-size: 16px;")
        self.email_input.setFixedWidth(300)
        self.email_input.setFixedHeight(30)

        # Center the email input horizontally

        tbox_location = QHBoxLayout()
        tbox_location.addStretch()
        tbox_location.addWidget(self.email_input)
        tbox_location.addStretch()

        # Next button

        next_button = QPushButton("Next", self)
        next_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0078D7;
                color: white;
                min-width: 130px;
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
                padding-bottom: 5px
            }
        """
        )
        next_button.setFixedWidth(100)
        next_button.setFixedHeight(30)

        # Allow pressing Enter (main or numpad) to trigger the Next button

        QShortcut(Qt.Key.Key_Return, next_button, activated=next_button.click)
        QShortcut(Qt.Key.Key_Enter, next_button, activated=next_button.click)

        # Connect button click to email validation

        next_button.clicked.connect(self.check_email_and_proceed)

        # Layout for the Next button (centered horizontally)

        button_layout = QHBoxLayout()
        button_layout.addStretch()  # push button to center

        button_layout.addWidget(next_button)  # add the Next button

        button_layout.addStretch()

        # ---------- Assemble Page 0 (Forgot Password form) ----------
        top_layout.addWidget(
            forgot_password_image, alignment=Qt.AlignmentFlag.AlignHCenter
        )  # top image

        top_layout.addWidget(forgot_pass_widget)  # "Forgot Password" title

        top_layout.addWidget(instructions_label)  # instructions text

        top_layout.addLayout(tbox_location)  # email input field

        top_layout.addLayout(button_layout)  # Next button

        # Add Page 0 to stacked widget

        self.stack.addWidget(page0)

        # Add Page 1 (confirmation options) to stack

        self.stack.addWidget(self.createConfirmationPage())

        # Add Page 2 (code entry) to stack

        self.stack.addWidget(self.createCodeEntryPage())

        # Add Page 3 (new password) to stack

        self.stack.addWidget(self.createNewPasswordPage())

    # ---------- Page 1: Confirmation Options ----------

    def createConfirmationPage(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title label ("Make Selection")

        title_label = QLabel("Make\nSelection")
        title_label.setStyleSheet(
            """
            font-family: 'Segoe Script';
            font-weight: bold; 
            font-size: 38px;
            padding-left: 20px;
            
        """
        )
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft | Qt.AlignmentFlag.AlignTop)

        # Title layout with margins

        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(20, 20, 0, 0)
        title_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignLeft)
        layout.addLayout(title_layout)

        # Instruction label ("How would you like to receive your code?")

        instruction_label = QLabel(
            "How would you like to receive your\nconfirmation code?"
        )
        instruction_label.setStyleSheet(
            """
            font-size: 16px; 
            font-weight: bold;
            padding-left: 20px;
        """
        )
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        instruction_label.setContentsMargins(40, 0, 0, 0)
        layout.addWidget(instruction_label)

        # Email button (with icon)

        email_button = QPushButton("Send via Email")
        email_button.setFixedSize(220, 60)  # size for icon + text

        email_button.setIcon(QIcon("assets/hand.png"))  # icon image

        email_button.setIconSize(QSize(32, 32))  # control icon size

        email_button.setStyleSheet(
            """
            QPushButton {
                background-color: lightgray;
                color: black;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: gray; }
            QPushButton:pressed { background-color: darkgray; }
        """
        )

        # SMS button (wieh icon)
        sms_button = QPushButton("Send via SMS")
        sms_button.setFixedSize(220, 60)
        sms_button.setIcon(QIcon("assets/smartphone.png"))
        sms_button.setIconSize(QSize(32, 32))
        sms_button.setStyleSheet(
            """
            QPushButton {
                background-color: lightgray;
                color: black;
                border-radius: 8px;
                font-size: 16px;
                font-weight: bold;
            }
            QPushButton:hover { background-color: gray; }
            QPushButton:pressed { background-color: darkgray; }
        """
        )

        # Add buttons to layout (centered)

        layout.addWidget(email_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sms_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # ---------- DEMO CODE HANDLER ----------
        def show_demo_code():
            # Call into C++ DLL to get demo code
            demo_code = dll_path.generate_demo_code().decode("utf-8")
            self.current_contact = self.email_input.text()  # save email/phone

            # Create a custom QMessageBox so we can style the text
            msg = QMessageBox(self)
            msg.setWindowTitle("Demo Verification Code")

            # Use HTML to enlarge and center the demo code line
            msg.setText(
                f"<p style='font-size:14px;'>This is a demo app.</p>"
                f"<p style='font-size:22px; font-weight:bold; text-align:center;'>"
                f"Your generated code is:<br>{demo_code}</p>"
                f"<p style='font-size:14px;'>In a real application, this would be sent to your email or phone.</p>"
            )

            msg.exec()

            # Transition to Page 2 (code entry)
            self.animateTransition(2)

            # Start countdown timer when this pag is created

            self.start_timer_ui()

        # Connect both buttons to the same demo handler
        email_button.clicked.connect(show_demo_code)
        sms_button.clicked.connect(show_demo_code)

        return page

    # ---------- Page 2: Code Entry ----------

    def createCodeEntryPage(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # Verification image
        varification_image = QLabel(self)
        pixmap = QPixmap("assets/logistics-management.png")
        pixmap = pixmap.scaled(
            175,
            175,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        varification_image.setPixmap(pixmap)
        varification_image.setAlignment(Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(varification_image, alignment=Qt.AlignmentFlag.AlignHCenter)

        # Title ("Enter Verification Code")

        title_label = QLabel("Enter Verification Code")
        title_label.setStyleSheet("font-weight: bold; font-size: 24px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Instructions

        instruction_label = QLabel(
            "Please enter the 6-digit code sent to your email or phone."
        )
        instruction_label.setStyleSheet("font-size: 16px; color: gray;")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instruction_label)

        # Code input boxes (6 seperate QLineEdit fields)

        code_layout = QHBoxLayout()
        self.code_inputs = []  # store references to each box

        for i in range(6):
            box = QLineEdit()
            box.setMaxLength(1)  # only one digit per box
            box.setAlignment(Qt.AlignmentFlag.AlignCenter)
            box.setFixedSize(40, 50)
            box.setStyleSheet(
                """
                QLineEdit {
                    font-size: 24px;
                    border: 2px solid #0078D7;
                    border-radius: 5px;
                }
            """
            )
            self.code_inputs.append(box)
            code_layout.addWidget(box)

            # Auto-move focus to next box when filled
            # (only connect for first 5 boxes, last box doesn't need to move focus)
            if i < 5:
                box.textChanged.connect(lambda text, idx=i: self.move_focus(idx, text))

        # Add the row of 6 code input boxes to the layout

        layout.addLayout(code_layout)

        # ---------- Timer Label ----------

        # Display countdown until code expires (will be updated by C++ backend)
        self.timer_label = QLabel("Code expires in 60 seconds")
        self.timer_label.setStyleSheet("font-size: 14px; color: red;")
        self.timer_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.timer_label)

        # ---------- Submit Button ----------

        # Disabled until all 6 digits are entered

        self.submit_button = QPushButton("Submit")
        self.submit_button.setFixedSize(120, 40)
        self.submit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover:!disabled { background-color: #2893f5; }
            QPushButton:pressed:!disabled { background-color: #005a9e; }
            QPushButton:disabled {
                background-color: lightgray;
                color: darkgray;
                border: 1px solid gray;
            }
        """
        )
        self.submit_button.setEnabled(False)  # start disabled
        layout.addWidget(self.submit_button, alignment=Qt.AlignmentFlag.AlignCenter)

        # Connect each code box to validation check

        # (Submit button only enables when all 6 boxes are filled with digits)

        for box in self.code_inputs:
            box.textChanged.connect(self.check_code_complete)

        # Connect submit button to validation

        self.submit_button.clicked.connect(self.on_submit)

        return page

    # ---------- Page 3: New Password ----------

    def createNewPasswordPage(self):
        page = QWidget()
        layout = QVBoxLayout(page)

        # Title
        title_label = QLabel("Set New Password")
        title_label.setStyleSheet("font-weight: bold; font-size: 24px;")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(title_label)

        # Instructions
        instruction_label = QLabel("Enter and confirm your new password below.")
        instruction_label.setStyleSheet("font-size: 16px; color: gray;")
        instruction_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(instruction_label)

        # New password input
        self.new_password_input = QLineEdit()
        self.new_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.new_password_input.setPlaceholderText("New Password")
        self.new_password_input.setFixedHeight(40)
        self.new_password_input.setStyleSheet(
            "font-size: 16px; border: 2px solid #0078D7; border-radius: 5px;"
        )
        layout.addWidget(self.new_password_input)

        # Confirm password input
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.confirm_password_input.setPlaceholderText("Confirm New Password")
        self.confirm_password_input.setFixedHeight(40)
        self.confirm_password_input.setStyleSheet(
            "font-size: 16px; border: 2px solid #0078D7; border-radius: 5px;"
        )
        layout.addWidget(self.confirm_password_input)

        # Feedback label
        self.feedback_label = QLabel("")
        self.feedback_label.setStyleSheet("font-size: 14px; color: red;")
        self.feedback_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.feedback_label)

        # Submit button
        self.password_submit_button = QPushButton("Update Password")
        self.password_submit_button.setFixedSize(160, 40)
        self.password_submit_button.setStyleSheet(
            """
            QPushButton {
                background-color: #0078D7;
                color: white;
                border-radius: 5px;
                font-size: 16px;
            }
            QPushButton:hover:!disabled { background-color: #2893f5; }
            QPushButton:pressed:!disabled { background-color: #005a9e; }
            QPushButton:disabled {
                background-color: lightgray;
                color: darkgray;
                border: 1px solid gray;
            }
            """
        )
        layout.addWidget(
            self.password_submit_button, alignment=Qt.AlignmentFlag.AlignCenter
        )

        # Connect submit button
        self.password_submit_button.clicked.connect(self.on_password_submit)

        return page

    # ---------- Page Transition Animation ----------

    def animateTransition(self, index):
        # Fade out current page

        current = self.stack.currentWidget()
        effect = QGraphicsOpacityEffect(current)
        current.setGraphicsEffect(effect)

        self.fade_out = QPropertyAnimation(effect, b"opacity")  # keep reference

        self.fade_out.setDuration(400)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)

        # Switch page one fade-out finishes

        def switchPage():
            self.stack.setCurrentIndex(index)
            new_page = self.stack.currentWidget()

            # Fade in new page

            new_effect = QGraphicsOpacityEffect(new_page)
            new_page.setGraphicsEffect(new_effect)
            new_effect.setOpacity(0.0)

            self.fade_in = QPropertyAnimation(new_effect, b"opacity")  # keep reference

            self.fade_in.setDuration(400)
            self.fade_in.setStartValue(0.0)
            self.fade_in.setEndValue(1.0)
            self.fade_in.start()

        self.fade_out.finished.connect(switchPage)
        self.fade_out.start()


# ==================== Standalone Mode for Testing ====================
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ForgotPasswordUI()
    window.show()
    sys.exit(app.exec())
