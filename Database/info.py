from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QGridLayout,
                             QLabel, QFrame, QSizePolicy, QDialog, QFormLayout,
                             QRadioButton, QLineEdit, QMessageBox, QDialogButtonBox)
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont

class Info(QWidget):
    back_to_home = pyqtSignal()
    # 新增：跳转到Graph页的信号，携带查询类型参数
    switch_to_graph = pyqtSignal(str, object, object)

    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(45, 35, 45, 35)
        main_layout.setSpacing(20)

        # 顶部标题面板（和home完全一致）
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
        self.title_label = QLabel("Library Information Center")
        self.title_label.setFont(QFont("Microsoft YaHei", 17, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color:#1f4b80;")
        title_layout.addWidget(self.title_label)
        main_layout.addWidget(self.title_panel)

        # 按钮网格
        btn_grid = QGridLayout()
        btn_grid.setSpacing(24)
        btn_grid.setContentsMargins(20, 0, 20, 5)

        self.btn_search_book = QPushButton("Query books")
        self.btn_search_reader = QPushButton("Query readers")
        self.btn_search_available = QPushButton("Books Available")
        self.btn_search_history = QPushButton("Query history record")
        self.btn_search_borrow = QPushButton("Query borrow")
        self.btn_calculate_reader = QPushButton("Rank Bookworms")
        self.btn_calculate_book = QPushButton("Rank Bestsellers")
        self.btn_back = QPushButton("back")

        btn_css = """
            QPushButton{
                min-height: 72px;
                padding: 0 40px;
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
        """
        all_btns = [
            self.btn_search_book, self.btn_search_reader,
            self.btn_search_available, self.btn_search_history,
            self.btn_search_borrow, self.btn_calculate_reader,
            self.btn_calculate_book, self.btn_back
        ]
        for btn in all_btns:
            btn.setStyleSheet(btn_css)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # 网格排布：每行两个
        btn_grid.addWidget(self.btn_search_book, 0, 0)
        btn_grid.addWidget(self.btn_search_reader, 0, 1)
        btn_grid.addWidget(self.btn_search_available, 1, 0)
        btn_grid.addWidget(self.btn_search_history, 1, 1)
        btn_grid.addWidget(self.btn_search_borrow, 2, 0)
        btn_grid.addWidget(self.btn_calculate_reader, 2, 1),
        btn_grid.addWidget(self.btn_calculate_book, 3, 0)
        btn_grid.addWidget(self.btn_back, 3, 1)

        main_layout.addStretch()
        main_layout.addLayout(btn_grid)

        # 绑定点击事件
        self.btn_search_book.clicked.connect(self.on_search_book)
        self.btn_search_reader.clicked.connect(self.on_search_reader)
        self.btn_search_available.clicked.connect(self.on_search_available)
        self.btn_search_history.clicked.connect(self.on_search_history)
        self.btn_search_borrow.clicked.connect(self.on_search_borrow)
        self.btn_calculate_reader.clicked.connect(self.on_calculate_reader)
        self.btn_calculate_book.clicked.connect(self.on_calculate_book)
        self.btn_back.clicked.connect(self.on_back_home)

    # ====================== 按钮槽函数 ======================
    def on_search_book(self):
        self.switch_to_graph.emit("search_book", None, None)

    def on_search_reader(self):
        self.switch_to_graph.emit("search_reader", None, None)

    def on_search_available(self):
        self.switch_to_graph.emit("search_available", None, None)

    def on_search_history(self):
        self.switch_to_graph.emit("search_history", None, None)

    def on_search_borrow(self):
        dlg = QDialog(self)
        dlg.setWindowTitle("Search Borrow Records")
        dlg.resize(500, 280)
        
        flags = dlg.windowFlags()
        flags &= ~Qt.WindowContextHelpButtonHint  # 清除问号
        dlg.setWindowFlags(flags)
        
        layout = QFormLayout(dlg)
        layout.setLabelAlignment(Qt.AlignRight)
        
        # 单选选项（天然互斥，有且仅能选一个）
        self.rb_search_reader = QRadioButton("Search by reader_id")
        self.rb_search_title = QRadioButton("Search by title_id")
        self.rb_search_reader.setChecked(True)  # 默认选中第一项
        
        # 选项容器（垂直排布，与Reset对话框结构一致）
        option_widget = QWidget()
        option_layout = QVBoxLayout(option_widget)
        option_layout.setContentsMargins(0, 0, 0, 0)
        option_layout.setSpacing(10)
        option_layout.addWidget(self.rb_search_reader)
        option_layout.addWidget(self.rb_search_title)
        layout.addRow("Search mode:", option_widget)
        
        # 两个输入框
        ed_reader_id = QLineEdit()
        ed_title_id = QLineEdit()
        ed_reader_id.setPlaceholderText("example: 510000F")
        ed_title_id.setPlaceholderText("example: A1001")
        # 默认选中reader_id，禁用并清空title_id输入框
        ed_title_id.setEnabled(False)
        
        layout.addRow("reader_id:", ed_reader_id)
        layout.addRow("title_id:", ed_title_id)
        
        # 单选切换逻辑：选中一个则清空并禁用另一个输入框
        def on_reader_toggled(checked):
            if checked:
                ed_title_id.clear()
                ed_title_id.setEnabled(False)
                ed_reader_id.setEnabled(True)
        
        def on_title_toggled(checked):
            if checked:
                ed_reader_id.clear()
                ed_reader_id.setEnabled(False)
                ed_title_id.setEnabled(True)
        
        self.rb_search_reader.toggled.connect(on_reader_toggled)
        self.rb_search_title.toggled.connect(on_title_toggled)
        
        # 按钮组
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(dlg.accept)
        btn_box.rejected.connect(dlg.reject)
        layout.addRow(btn_box)
        
        if not dlg.exec_():
            return  # 用户点Cancel直接返回
        
        if self.rb_search_reader.isChecked():
            reader_id_val = ed_reader_id.text().strip()
            title_id_val = None
            if not reader_id_val:
                QMessageBox.warning(self, "Input Error", "reader_id cannot be empty.")
                return
        else:
            title_id_val = ed_title_id.text().strip()
            reader_id_val = None
            if not title_id_val:
                QMessageBox.warning(self, "Input Error", "title_id cannot be empty.")
                return
        
        self.switch_to_graph.emit("search_borrow", reader_id_val, title_id_val)

    def on_calculate_reader(self):
        self.switch_to_graph.emit("calculate_reader", None, None)
        
    def on_calculate_book(self):
        self.switch_to_graph.emit("calculate_book", None, None)

    def on_back_home(self):
        self.back_to_home.emit()
