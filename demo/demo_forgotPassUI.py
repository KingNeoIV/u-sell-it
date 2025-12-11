from PyQt6.QtWidgets import (
    QWidget,
    QVBoxLayout,
    QLabel,
    QLineEdit,
    QHBoxLayout,
    QPushButton,
)
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt


class ForgotPasswordUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/u-sell-it_icon_black.ico"))
        self.setWindowTitle("Forgot Password")
        self.setFixedSize(450, 500)

        layout = QVBoxLayout(self)

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
        next_button.setStyleSheet("font-size: 16px;")
        next_button.setFixedWidth(100)
        next_button.setFixedHeight(30)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        button_layout.addWidget(next_button)
        button_layout.addStretch()

        # Sub-layout
        top_layout = QVBoxLayout()
        top_layout.setSpacing(25)
        top_layout.addWidget(
            forgot_password_image, alignment=Qt.AlignmentFlag.AlignHCenter
        )
        top_layout.addWidget(forgot_pass_widget)
        top_layout.addWidget(instructions_label)
        top_layout.addLayout(tbox_location)
        top_layout.addLayout(button_layout)

        layout.addLayout(top_layout)
        layout.addStretch()


# Keep standalone mode for testing
if __name__ == "__main__":
    import sys
    from PyQt6.QtWidgets import QApplication

    app = QApplication(sys.argv)
    window = ForgotPasswordUI()
    window.show()
    sys.exit(app.exec())
