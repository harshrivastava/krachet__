from PyQt5.QtWidgets import QApplication, QWidget, QTextEdit, QMainWindow, QStackedWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel
from PyQt5.QtGui import QMovie, QColor, QTextCharFormat
from PyQt5.QtCore import Qt, QSize, QTimer
import sys
import os

# Paths for resources
current_dir = os.getcwd()
GraphicsDirPath = rf"{current_dir}\Frontend\Graphics"
TempDirPath = rf"{current_dir}\Frontend\Files"

def GraphicsDirectoryPath(Filename):
    return rf"{GraphicsDirPath}\{Filename}"

def TempDirectoryPath(Filename):
    return rf"{TempDirPath}\{Filename}"

class ChatSection(QWidget):
    def __init__(self):
        super(ChatSection, self).__init__()
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(10)

        # Chat Text Edit
        self.chat_text_edit = QTextEdit()
        self.chat_text_edit.setReadOnly(True)
        self.chat_text_edit.setStyleSheet("""
            QTextEdit {
                background-color: #2c2f33;
                color: white;
                font-size: 14px;
                border: 1px solid #23272a;
                border-radius: 5px;
                padding: 5px;
            }
        """)
        layout.addWidget(self.chat_text_edit)

        # AI Orb
        self.orb_label = QLabel()
        self.orb_movie = QMovie(GraphicsDirectoryPath("AI_Orb.gif"))  # Add your AI orb GIF here
        self.orb_movie.setScaledSize(QSize(100, 100))  # Adjust size as needed
        self.orb_label.setMovie(self.orb_movie)
        self.orb_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.orb_label)

        # Status Label
        self.label = QLabel("Status: Idle")
        self.label.setStyleSheet("color: white; font-size: 16px;")
        layout.addWidget(self.label)

        # Timer for Updates
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.updateStatus)
        self.timer.start(500)

    def updateStatus(self):
        # Simulate reading status from a file
        try:
            with open(TempDirectoryPath('Status.data'), "r", encoding='utf-8') as file:
                status = file.read().strip()
                self.label.setText(f"Status: {status}")

                # Control AI Orb Animation
                if "Listening" in status or "Speaking" in status:
                    self.orb_movie.start()
                else:
                    self.orb_movie.stop()
        except FileNotFoundError:
            self.label.setText("Status: File not found")

    def addMessage(self, message, color="white"):
        cursor = self.chat_text_edit.textCursor()
        format = QTextCharFormat()
        format.setForeground(QColor(color))
        cursor.setCharFormat(format)
        cursor.insertText(message + "\n")
        self.chat_text_edit.setTextCursor(cursor)

class CustomTopBar(QWidget):
    def __init__(self, parent):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.setFixedHeight(50)
        layout = QHBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)

        # Title Label
        title_label = QLabel("AI Assistant")
        title_label.setStyleSheet("color: white; font-size: 18px; font-weight: bold; padding-left: 10px;")
        layout.addWidget(title_label)

        layout.addStretch(1)

        # Minimize Button
        minimize_button = QPushButton("-")
        minimize_button.setStyleSheet("""
            QPushButton {
                background-color: #99aab5;
                color: black;
                border: none;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #7289da;
                color: white;
            }
        """)
        minimize_button.clicked.connect(self.parent().showMinimized)
        layout.addWidget(minimize_button)

        # Close Button
        close_button = QPushButton("X")
        close_button.setStyleSheet("""
            QPushButton {
                background-color: #f04747;
                color: white;
                border: none;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #d83c3e;
            }
        """)
        close_button.clicked.connect(self.parent().close)
        layout.addWidget(close_button)

        self.setLayout(layout)

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setStyleSheet("background-color: #2c2f33;")
        self.initUI()

    def initUI(self):
        # Main Layout
        stacked_widget = QStackedWidget(self)
        stacked_widget.addWidget(ChatSection())

        # Top Bar
        top_bar = CustomTopBar(self)
        top_bar.setStyleSheet("background-color: #23272a;")

        # Main Layout
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(top_bar)
        main_layout.addWidget(stacked_widget)

        # Central Widget
        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

def GraphicalUserInterface():
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QMainWindow {
            background-color: #2c2f33;
        }
        QLabel {
            color: white;
            font-size: 14px;
        }
    """)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    GraphicalUserInterface()



