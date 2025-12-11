from PyQt6.QtWidgets import (
    QApplication,
    QWidget,
    QLabel,
    QLineEdit,
    QPushButton,
    QVBoxLayout,
    QHBoxLayout,
    QMessageBox,
)

from linuxDemo_registerUI import RegisterScreen
from linuxDemo_forgotPassUI import ForgotPasswordUI
from PyQt6.QtGui import QPixmap, QIcon
from PyQt6.QtCore import Qt
from ctypes import cdll, c_char_p, c_int
import os
import sys


class LoginScreen(QWidget):
    def keyPressEvent(self, event):
        if event.key() == Qt.Key.Key_Escape:
            reply = QMessageBox.question
            (
                self,
                "Exit Application",
                "Are you sure you want to exit?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.close()

    def handle_login(self):
        username = self.username.text().encode("utf-8")
        password = self.password.text().encode("utf-8")

        result = self.login_lib.validate_login(username, password)

        if result == 1:
            QMessageBox.information(self, "Login", "Login successful!")

        else:
            QMessageBox.warning(self, "Login", "Invalid username or password.")

    def open_register_screen(self):
        self.register_window = RegisterScreen()
        self.register_window.show()

    def open_forgot_password_screen(self):
        self.forgot_window = ForgotPasswordUI()
        self.forgot_window.show()

    def __init__(self):
        super().__init__()
        self.setWindowIcon(QIcon("assets/u-sell-it_icon_black.ico"))
        self.setWindowTitle("u-sell-it")
        self.setFixedSize(600, 900)
        self.wallpaper = QLabel(self)
        self.wallpaper.setPixmap(
            QPixmap("assets/LoginScreen2v2.png").scaled(
                self.size(), Qt.AspectRatioMode.IgnoreAspectRatio
            )
        )
        self.wallpaper.setGeometry(0, 0, 600, 900)

        main_layout = QVBoxLayout(self)

        welcome_label_1 = QLabel("Welcome")
        welcome_label_1.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label_1.setStyleSheet(
            """                                   
            font-size: 50px;
            font-weight: bold;
            color: white;
            margin-top: -5px;
        """
        )
        main_layout.addWidget(welcome_label_1)

        welcome_label_2 = QLabel("To")
        welcome_label_2.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label_2.setStyleSheet(
            """
            font-size: 50px;
            font-weight: bold;
            color: white;
            margin-top: -20px;
        """
        )
        main_layout.addWidget(welcome_label_2)

        welcome_label_3 = QLabel("Please login!")
        welcome_label_3.setAlignment(Qt.AlignmentFlag.AlignCenter)
        welcome_label_3.setStyleSheet(
            """
            font-size: 50px;
            font-weight: bold;
            color: white;
            margin-top: 375px;
        """
        )
        main_layout.addWidget(welcome_label_3)

        main_layout.addStretch()

        self.overlay = QWidget(self)
        self.overlay.setGeometry(150, 600, 300, 200)
        self.overlay.setStyleSheet(
            "background-color: rgba(255, 255, 255, 40); border-radius: 15px"
        )

        login_layout = QVBoxLayout()

        self.username = QLineEdit(self)
        self.username.setPlaceholderText("Username:")
        self.username.setStyleSheet(
            """ 
            QLineEdit {
                padding: 5px;
                font-size: 17px;
                min-width: 250px;
                height: 30px;
            }
        """
        )
        self.username.returnPressed.connect(self.handle_login)
        login_layout.addWidget(self.username)

        self.password = QLineEdit()
        self.password.setPlaceholderText("Password:")
        self.password.setEchoMode(QLineEdit.EchoMode.Password)
        self.password.setStyleSheet(
            """
            QLineEdit {
                padding: 5px;
                font-size: 17px;
                min-width: 250px;
                height: 30px;
            }
        """
        )
        self.password.returnPressed.connect(self.handle_login)
        login_layout.addWidget(self.password)

        button_row = QHBoxLayout()

        self.login_btn = QPushButton("Login")
        self.login_btn.setStyleSheet(
            """
            QPushButton {
                background-color: 
                color: white;
                padding: 6px;
                border-radius: 5px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: 
            }
            QPushButton:pressed {
                background-color: 
                padding-top: 7px;
                padding-bottom: 5px;
            }
        """
        )
        self.login_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        button_row.addWidget(self.login_btn)
        self.login_btn.clicked.connect(self.handle_login)

        dll_path = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "linuxDemo_auth_login.so")
        )
        self.login_lib = cdll.LoadLibrary(dll_path)

        self.login_lib.validate_login.argtypes = [c_char_p, c_char_p]
        self.login_lib.validate_login.restype = c_int

        self.register_btn = QPushButton("Register")
        self.register_btn.setStyleSheet(
            """
            QPushButton {
                background-color: 
                color: white;
                padding: 6px;
                border-radius: 5px;
                font-size: 18px;
            }
            QPushButton:hover {
                background-color: 
            }
            QPushButton:pressed {
                background-color: 
                padding-top: 7px;
                padding-bottom: 5px;
            }
        """
        )
        self.register_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        button_row.addWidget(self.register_btn)
        self.register_btn.clicked.connect(self.open_register_screen)

        self.forgot_btn = QPushButton("Forgot Password")
        self.forgot_btn.setStyleSheet(
            """
            QPushButton {
                background-color: 
                color: white;
                min-width: 130px;
                padding: 6px;
                border-radius: 5px;
                font-size:  18px;
            }
            QPushButton:hover {
                background-color: 
            }
            QPushButton:pressed {
                background-color: 
                padding-top: 7px;
                padding-bottom: 5px;
            }
        """
        )
        self.forgot_btn.setCursor(Qt.CursorShape.PointingHandCursor)
        button_row.addWidget(self.forgot_btn)
        self.forgot_btn.clicked.connect(self.open_forgot_password_screen)

        login_layout.addLayout(button_row)

        self.overlay.setLayout(login_layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = LoginScreen()
    window.show()
    sys.exit(app.exec())
