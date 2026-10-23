from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
                             QLabel, QFrame, QSizePolicy, QScrollArea)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont


class Announce(QWidget):
    """Display the book management system usage notes."""

    back_to_home = pyqtSignal()

    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(45, 35, 45, 35)
        main_layout.setSpacing(20)

        self.title_panel = QFrame()
        self.title_panel.setFrameShape(QFrame.StyledPanel)
        self.title_panel.setStyleSheet("""
            QFrame {
                background: #f4faff;
                border-radius: 12px;
                border: 1px solid #a4caf0;
            }
        """)
        title_layout = QVBoxLayout(self.title_panel)
        title_layout.setContentsMargins(24, 18, 24, 18)
        self.title_label = QLabel("Library Announcement")
        self.title_label.setFont(QFont("Microsoft YaHei", 17, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color:#1f4b80;")
        title_layout.addWidget(self.title_label)
        main_layout.addWidget(self.title_panel)

        self.content_panel = QFrame()
        self.content_panel.setFrameShape(QFrame.StyledPanel)
        self.content_panel.setStyleSheet("""
            QFrame {
                background: #ffffff;
                border-radius: 12px;
                border: 1px solid #d0dce8;
            }
        """)
        content_layout = QVBoxLayout(self.content_panel)
        content_layout.setContentsMargins(30, 24, 30, 24)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setFrameShape(QFrame.NoFrame)
        scroll_area.setStyleSheet("QScrollArea { background: transparent; }")

        content_widget = QWidget()
        announcement_layout = QVBoxLayout(content_widget)
        announcement_layout.setContentsMargins(8, 4, 8, 4)
        announcement_layout.setSpacing(18)

        intro = QLabel(
            "Welcome to the Book Management System. Please read the following "
            "notes before using the system."
        )
        intro.setWordWrap(True)
        intro.setStyleSheet("color:#435466; font-size:22px;")
        announcement_layout.addWidget(intro)

        sections = [
            ("1. User permission", [
                "Admin can manage books and readers, record purchases, abandonments, borrowing and returns.",
                "Guest can browse library information and use the available query and statistics tools.",
            ]),
            ("2. Daily operations", [
                "Use the operation buttons on the home page to register books or readers and update circulation records.",
                "The undo button reverses the latest supported operation. Reset is reserved for system data maintenance.",
            ]),
            ("3. Information and statistics", [
                "Search Info provides book, reader, availability, history and borrowing queries.",
                "Ranking views summarize bookworms and bestsellers from the current library records.",
            ]),
            ("4. Rules for Readers(Attention!)", [
                "Each reader can borrow up to 10 books and can keep them for 30 days.",
                "Anyone who return books over 30 days later will face fine. The formula for calculating fine is as follows: ",
                "fine = number_of_books * price * ceil(keep_days - 30) * 0.1 ",
                "Anyone who is tagged 'overdue' cannot borrow books anymore unless he/she pays fine completely.",
            ]),
            ("5. Data notes", [
                "Please enter valid IDs and values when prompted. Operations are checked before being written to the database.",
                "Log out when changing users. Use Exit only when you want to close the application completely.",
            ]),
        ]

        for heading, lines in sections:
            section_title = QLabel(heading)
            section_title.setStyleSheet("color:#1f4b80; font-size:20px; font-weight:bold; font-family:'Microsoft YaHei';")
            announcement_layout.addWidget(section_title)

            for line in lines:
                detail = QLabel("-  " + line)
                detail.setWordWrap(True)
                detail.setStyleSheet("color:#526273; font-size:22px; padding-left:8px;")
                announcement_layout.addWidget(detail)

        announcement_layout.addStretch()
        scroll_area.setWidget(content_widget)
        content_layout.addWidget(scroll_area)
        main_layout.addWidget(self.content_panel, stretch=1)

        button_layout = QHBoxLayout()
        button_layout.addStretch()
        self.btn_back = QPushButton("back")
        self.btn_back.setStyleSheet("""
            QPushButton{
                min-height: 72px;
                padding: 0 60px;
                font-size: 25px;
                background-color:#3b86e0;
                color:#ffffff;
                border: none;
                border-radius: 10px;
            }
            QPushButton:hover{
                background-color:#2873cd;
            }
            QPushButton:pressed{
                background-color:#1c5fb0;
            }
        """)
        self.btn_back.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        button_layout.addWidget(self.btn_back)
        button_layout.addStretch()
        main_layout.addLayout(button_layout)

        self.btn_back.clicked.connect(self.on_back_to_home)

    def on_back_to_home(self):
        self.back_to_home.emit()
