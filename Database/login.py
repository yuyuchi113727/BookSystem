from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QFrame)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont


class Login(QWidget):
    # 切换页面信号，参数：用户身份（Admin / Guest）
    switch_to_home = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(45, 80, 45, 80)
        main_layout.setSpacing(40)

        # ========== 标题面板 ==========
        title_panel = QFrame()
        title_panel.setFrameShape(QFrame.StyledPanel)
        title_panel.setStyleSheet("""
            QFrame {
                background: #f4faff;
                border-radius: 12px;
                border: 1px solid #a4caf0;
            }
        """)
        title_layout = QVBoxLayout(title_panel)
        title_layout.setContentsMargins(24, 22, 24, 22)

        title_label = QLabel("Please select your identity")
        title_label.setFont(QFont("Microsoft YaHei", 18, QFont.Bold))
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("color:#1f4b80;")
        title_layout.addWidget(title_label)
        main_layout.addWidget(title_panel)

        # 弹性占位，让按钮区域居中
        main_layout.addStretch()

        # ========== 身份选择按钮 ==========
        btn_layout = QHBoxLayout()
        btn_layout.setSpacing(30)

        self.btn_admin = QPushButton("Admin")
        self.btn_guest = QPushButton("Guest")

        btn_css = """
        QPushButton{
            min-height: 52px;
            min-width: 160px;
            padding: 0 24px;
            font-size: 20px;
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
        """
        self.btn_admin.setStyleSheet(btn_css)
        self.btn_guest.setStyleSheet(btn_css)

        btn_layout.addWidget(self.btn_admin)
        btn_layout.addWidget(self.btn_guest)
        main_layout.addLayout(btn_layout)

        main_layout.addStretch()

        # ========== 绑定点击事件 ==========
        self.btn_admin.clicked.connect(lambda: self.switch_to_home.emit("Admin"))
        self.btn_guest.clicked.connect(lambda: self.switch_to_home.emit("Guest"))
