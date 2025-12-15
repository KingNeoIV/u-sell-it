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
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt, QPropertyAnimation, QSize


class ForgotPasswordUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/u-sell-it_icon_black.ico"))
        self.setWindowTitle("Forgot Password")
        self.setFixedSize(450, 500)

        self.stack = QStackedWidget(self)
        layout = QVBoxLayout(self)
        layout.addWidget(self.stack)

        # Page 0: Forgot password form
        page0 = QWidget()
        top_layout = QVBoxLayout(page0)
        top_layout.setSpacing(25)

        # Image
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

        # Title
        forgot_pass_widget = QLabel("Forgot\nPassword", self)
        forgot_pass_widget.setStyleSheet("font-weight: bold; font-size: 30px;")
        forgot_pass_widget.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Instructions
        instructions_label = QLabel(
            "Please enter your account's\nemail address and we will send you a verification code.",
            self,
        )
        instructions_label.setStyleSheet("font-size: 16px; color: gray;")
        instructions_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Email input
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Email")
        self.email_input.setStyleSheet("font-size: 16px;")
        self.email_input.setFixedWidth(300)
        self.email_input.setFixedHeight(30)

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
        next_button.clicked.connect(lambda: self.animateTransition(1))

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(next_button)
        button_layout.addStretch()

        # Assemble page0
        top_layout.addWidget(
            forgot_password_image, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        top_layout.addWidget(forgot_pass_widget)
        top_layout.addWidget(instructions_label)
        top_layout.addLayout(tbox_location)
        top_layout.addLayout(button_layout)

        # Add page0 to stack
        self.stack.addWidget(page0)
        # Page 1: Confirmation options
        self.stack.addWidget(self.createConfirmationPage())

    def createConfirmationPage(self):
        page = QWidget()
        layout = QVBoxLayout(page)

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

        title_layout = QVBoxLayout()
        title_layout.setContentsMargins(20, 20, 0, 0)
        title_layout.addWidget(title_label, alignment=Qt.AlignmentFlag.AlignLeft)

        layout.addLayout(title_layout)

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

        # Email button
        email_button = QPushButton("Send via Email")
        email_button.setFixedSize(220, 60)  # big enough for icon + text
        email_button.setIcon(QIcon("assets/hand.png"))  # your small picture
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

        # SMS button
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

        layout.addWidget(email_button, alignment=Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(sms_button, alignment=Qt.AlignmentFlag.AlignCenter)

        return page

    def animateTransition(self, index):
        current = self.stack.currentWidget()
        effect = QGraphicsOpacityEffect(current)
        current.setGraphicsEffect(effect)

        self.fade_out = QPropertyAnimation(effect, b"opacity")  # keep reference
        self.fade_out.setDuration(400)
        self.fade_out.setStartValue(1.0)
        self.fade_out.setEndValue(0.0)

        def switchPage():
            self.stack.setCurrentIndex(index)
            new_page = self.stack.currentWidget()

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


# Keep standalone mode for testing
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ForgotPasswordUI()
    window.show()
    sys.exit(app.exec())
