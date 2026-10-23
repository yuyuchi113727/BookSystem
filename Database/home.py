from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QPushButton,
                             QLabel, QFrame, QInputDialog, QMessageBox,
                             QGridLayout, QSizePolicy, QApplication,
                             QDialog, QDialogButtonBox, QFormLayout, QLineEdit, QRadioButton)
from PyQt5.QtCore import Qt, pyqtSignal, QDateTime
from PyQt5.QtGui import QFont
from operation import (reset_soft, reset_heavy,
                       check_format, check_book_exists, check_reader_exists, check_limit, check_remains, check_ownbook,
                       purchase_book, delete_book, borrow_book, return_book, register_book, register_reader,
                       inv_operation)

from decimal import Decimal
from collections import deque

stack = deque()

class Home(QWidget):
    
    switch_to_info = pyqtSignal()
    switch_to_announce = pyqtSignal()
    log_out_request = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(45, 35, 45, 35)
        main_layout.setSpacing(20)

        # ========== 标题区域（顶部） ==========
        self.title_panel = QFrame()
        self.title_panel.setFrameShape(QFrame.StyledPanel)
        self.title_panel.setStyleSheet("""
            QFrame {
                background: #f4faff;
                border-radius: 12px;
                border: 1px solid #a4caf0;
            }
        """)

        # 改为水平布局，保证标题居中+按钮靠右
        title_layout = QHBoxLayout(self.title_panel)
        title_layout.setContentsMargins(24, 18, 24, 18)
        title_layout.setSpacing(0)

        # 左侧占位控件：与Reset按钮同宽，保证标题严格居中对称
        left_placeholder = QWidget()
        left_placeholder.setFixedWidth(42)
        title_layout.addWidget(left_placeholder)

        # 标题（双弹簧夹在中间，实现居中）
        title_layout.addStretch()
        self.title_label = QLabel("Book Management System")
        self.title_label.setFont(QFont("Microsoft YaHei", 17, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color:#1f4b80;")
        title_layout.addWidget(self.title_label)
        title_layout.addStretch()

        # 右上角 Reset 圆形按钮
        self.reset_btn = QPushButton("Reset")
        self.reset_btn.setFixedSize(42, 42)  # 正圆形：宽高相等
        self.reset_btn.setCursor(Qt.PointingHandCursor)  # 鼠标悬停显示手型
        self.reset_btn.setStyleSheet("""
            QPushButton {
                background-color: #e74c3c;
                color: white;
                border: none;
                border-radius: 18px;  /* 圆角=半径，实现正圆 */
                font-size: 12px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #c0392b;  /* 悬停加深 */
            }
            QPushButton:pressed {
                background-color: #a93226;  /* 按压更深 */
            }
        """)
        title_layout.addWidget(self.reset_btn)

        main_layout.addWidget(self.title_panel)

        # ========== 按钮网格布局（3行2列，底部） ==========
        btn_grid = QGridLayout()
        btn_grid.setSpacing(24)
        btn_grid.setContentsMargins(20, 0, 20, 5)

        self.button_a = QPushButton("new purchase") #admin
        self.button_b = QPushButton("new abandon") #admin
        self.button_c = QPushButton("new borrow") #admin
        self.button_d = QPushButton("new return") #admin
        self.button_e = QPushButton("register book") #admin
        self.button_f = QPushButton("register reader") #admin
        self.button_g = QPushButton("undo latest op") #admin
        self.button_h = QPushButton("search info")
        self.button_i = QPushButton("announcement")
        self.button_j = QPushButton("quit system")

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

        all_buttons = [
            self.button_a, self.button_b,
            self.button_c, self.button_d,
            self.button_e, self.button_f,
            self.button_g, self.button_h,
            self.button_i, self.button_j
        ]
        for btn in all_buttons:
            btn.setStyleSheet(btn_css)
            btn.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        btn_grid.addWidget(self.button_a, 0, 0)
        btn_grid.addWidget(self.button_b, 0, 1)
        btn_grid.addWidget(self.button_c, 1, 0)
        btn_grid.addWidget(self.button_d, 1, 1)
        btn_grid.addWidget(self.button_e, 2, 0)
        btn_grid.addWidget(self.button_f, 2, 1)
        btn_grid.addWidget(self.button_g, 3, 0)
        btn_grid.addWidget(self.button_h, 3, 1)
        btn_grid.addWidget(self.button_i, 4, 0)
        btn_grid.addWidget(self.button_j, 4, 1)

        main_layout.addStretch()
        main_layout.addLayout(btn_grid)

        # ========== 绑定点击事件 ==========
        self.reset_btn.clicked.connect(self.on_click_reset)
        self.button_a.clicked.connect(self.on_click_a)
        self.button_b.clicked.connect(self.on_click_b)
        self.button_c.clicked.connect(self.on_click_c)
        self.button_d.clicked.connect(self.on_click_d)
        self.button_e.clicked.connect(self.on_click_e)
        self.button_f.clicked.connect(self.on_click_f)
        self.button_g.clicked.connect(self.on_click_g)
        self.button_h.clicked.connect(self.on_click_h)
        self.button_i.clicked.connect(self.on_click_i)
        self.button_j.clicked.connect(self.on_click_j)

        # 存储当前用户身份
        self.current_role = ""

    def set_user_role(self, role: str):
        """接收登录身份，可用于权限控制"""
        self.current_role = role
        self.title_label.setText(f"Book Management System - {role}")
    
    def check_privilege(self) -> bool:
        """Guest 身份返回 False 并弹出提示，Admin 返回 True"""
        if self.current_role == "Guest":
            QMessageBox.warning(self, "Permission Denied", 
                              "You have no priority to operate that.")
            return False
        return True

    # ========== 按钮功能 ==========
    def on_click_reset(self):
        if not self.check_privilege():
            return
        
        dlg = QDialog(self)
        dlg.setWindowTitle("Reset Confirm")
        dlg.resize(460, 220)
        
        flags = dlg.windowFlags()
        flags &= ~Qt.WindowContextHelpButtonHint  # 清除问号
        dlg.setWindowFlags(flags)
        
        layout = QFormLayout(dlg)
        layout.setLabelAlignment(Qt.AlignRight)
        
        # 提示文字
        tip_label = QLabel(f"Please select the reset operation to perform:\n Attention! The data cannot be recovered.")
        tip_label.setStyleSheet("color: #333;")
        layout.addRow(tip_label)
        
        # 单选选项
        self.rb_reset_record = QRadioButton("Reset borrow/return records only")
        self.rb_reset_all = QRadioButton("Reset all system data")
        self.rb_reset_record.setChecked(True)  # 默认选中第一项
        
        # 选项容器（垂直排布）
        option_widget = QWidget()
        option_layout = QVBoxLayout(option_widget)
        option_layout.setContentsMargins(0, 0, 0, 0)
        option_layout.setSpacing(10)
        option_layout.addWidget(self.rb_reset_record)
        option_layout.addWidget(self.rb_reset_all)
        layout.addRow("Operation:", option_widget)
        
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(dlg.accept)
        btn_box.rejected.connect(dlg.reject)
        layout.addRow(btn_box)
        
        if not dlg.exec_():
            return  # 用户点Cancel直接返回
        
        # 获取选中项
        if self.rb_reset_record.isChecked():
            reset_flag, reset_msg = reset_soft()
        else:
            reset_flag, reset_msg = reset_heavy()
            
        if not reset_flag:
            QMessageBox.warning(self, "Reset Error", reset_msg)
        else:
            stack.clear()
            QMessageBox.information(self, "Success", reset_msg)
            
    def on_click_a(self):
        if not self.check_privilege():
            return
        
        global stack
        dlg = QDialog(self)
        dlg.setWindowTitle("New Purchase")
        dlg.resize(500, 280)
        
        flags = dlg.windowFlags()
        flags &= ~Qt.WindowContextHelpButtonHint  # 清除问号
        dlg.setWindowFlags(flags)
        
        layout = QFormLayout(dlg)
        
        ed_title_id = QLineEdit()
        ed_number = QLineEdit()
        ed_time = QLineEdit()
        ed_title_id.setPlaceholderText("example: A1001")
        ed_number.setPlaceholderText("example: 3")
        ed_time.setPlaceholderText("example: 2020-01-01 12:00:00")
        
        layout.addRow("title_id:", ed_title_id)
        layout.addRow("number:", ed_number)
        layout.addRow("time:", ed_time)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(dlg.accept)
        btn_box.rejected.connect(dlg.reject)
        layout.addRow(btn_box)

        if not dlg.exec_():
            return  # 用户点Cancel直接返回

        # 获取输入
        title_id_str = ed_title_id.text().strip()
        num_str = ed_number.text().strip()
        time_str = ed_time.text().strip() if ed_time.text().strip() else QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        #校验数字与时间
        format_flag, format_msg = check_format(num_str, time_str)
        if not format_flag:
            QMessageBox.warning(self, "Input Error", format_msg)
            return
        
        #校验书号是否被注册
        exist_flag, exist_msg = check_book_exists(title_id_str)
        if not exist_flag:
            QMessageBox.warning(self, "Id Error", exist_msg)
            return 
        
        #插入采购
        purchase_flag, purchase_msg, stack = purchase_book(title_id_str, int(num_str), time_str, stack)
        if not purchase_flag:
            QMessageBox.warning(self, "Purchase Error", purchase_msg)
        else:
            QMessageBox.information(self, "Success", purchase_msg)
            
        
    def on_click_b(self):
        if not self.check_privilege():
            return
        
        global stack
        dlg = QDialog(self)
        dlg.setWindowTitle("New Abandon")
        dlg.resize(500, 280)
        
        flags = dlg.windowFlags()
        flags &= ~Qt.WindowContextHelpButtonHint  # 清除问号
        dlg.setWindowFlags(flags)
        
        layout = QFormLayout(dlg)
        
        ed_title_id = QLineEdit()
        ed_number = QLineEdit()
        ed_time = QLineEdit()
        ed_title_id.setPlaceholderText("example: A1001")
        ed_number.setPlaceholderText("example: 3")
        ed_time.setPlaceholderText("example: 2020-01-01 12:00:00")
        
        layout.addRow("title_id:", ed_title_id)
        layout.addRow("number:", ed_number)
        layout.addRow("time:", ed_time)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(dlg.accept)
        btn_box.rejected.connect(dlg.reject)
        layout.addRow(btn_box)

        if not dlg.exec_():
            return  # 用户点Cancel直接返回

        # 获取输入
        title_id_str = ed_title_id.text().strip()
        num_str = ed_number.text().strip()
        time_str = ed_time.text().strip() if ed_time.text().strip() else QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        #校验数字与时间
        format_flag, format_msg = check_format(num_str, time_str)
        if not format_flag:
            QMessageBox.warning(self, "Input Error", format_msg)
            return
        
        #查此书是否库存足够
        remains_flag, remains_msg = check_remains(title_id_str, int(num_str))
        if not remains_flag:
            QMessageBox.warning(self, "Id Error", remains_msg)
            return
        
        #淘汰操作
        delete_flag, delete_msg, stack = delete_book(title_id_str, int(num_str), time_str, stack)
        if not delete_flag:
            QMessageBox.warning(self, "Abandon Error", delete_msg)
        else:
            QMessageBox.information(self, "Success", delete_msg)
            
    def on_click_c(self):
        if not self.check_privilege():
            return
        
        global stack
        dlg = QDialog(self)
        dlg.setWindowTitle("New Borrow")
        dlg.resize(500, 280)
        
        flags = dlg.windowFlags()
        flags &= ~Qt.WindowContextHelpButtonHint  # 清除问号
        dlg.setWindowFlags(flags)
        
        layout = QFormLayout(dlg)
        
        ed_reader_id = QLineEdit()
        ed_title_id = QLineEdit()
        ed_number = QLineEdit()
        ed_time = QLineEdit()
        ed_reader_id.setPlaceholderText("example: 510000M")
        ed_title_id.setPlaceholderText("example: A1001")
        ed_number.setPlaceholderText("example: 3")
        ed_time.setPlaceholderText("example: 2020-01-01 00:00:00")
        
        layout.addRow("reader_id:", ed_reader_id)
        layout.addRow("title_id:", ed_title_id)
        layout.addRow("number:", ed_number)
        layout.addRow("time:", ed_time)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(dlg.accept)
        btn_box.rejected.connect(dlg.reject)
        layout.addRow(btn_box)

        if not dlg.exec_():
            return  # 用户点Cancel直接返回

        # 获取输入
        reader_id_str = ed_reader_id.text().strip()
        title_id_str = ed_title_id.text().strip()
        num_str = ed_number.text().strip()
        time_str = ed_time.text().strip() if ed_time.text().strip() else QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        #校验数字与时间
        format_flag, format_msg = check_format(num_str, time_str)
        if not format_flag:
            QMessageBox.warning(self, "Input Error", format_msg)
            return
        
        #检查读者是否注册
        exist_flag, exist_msg = check_reader_exists(reader_id_str)
        if not exist_flag:
            QMessageBox.warning(self, "Id Error", exist_msg)
            return 
        
        #查此书库存是否足够
        remains_flag, remains_msg = check_remains(title_id_str, int(num_str))
        if not remains_flag:
            QMessageBox.warning(self, "Id Error", remains_msg)
            return 
            
        #查读者是否超出未还上限10本，同时是否有未缴罚款
        limit_flag, limit_msg = check_limit(reader_id_str)
        if not limit_flag:
            QMessageBox.warning(self, "Id Error", limit_msg)
            return
        
        #借书操作
        borrow_flag, borrow_msg, stack = borrow_book(reader_id_str, title_id_str, int(num_str), time_str, stack)
        if not borrow_flag:
            QMessageBox.warning(self, "Borrow Error", borrow_msg)
        else:
            QMessageBox.information(self, "Success", borrow_msg)
        
    def on_click_d(self):
        if not self.check_privilege():
            return
        
        global stack
        dlg = QDialog(self)
        dlg.setWindowTitle("New Return")
        dlg.resize(500, 280)
        
        flags = dlg.windowFlags()
        flags &= ~Qt.WindowContextHelpButtonHint  # 清除问号
        dlg.setWindowFlags(flags)
        
        layout = QFormLayout(dlg)
        
        ed_reader_id = QLineEdit()
        ed_title_id = QLineEdit()
        ed_number = QLineEdit()
        ed_time = QLineEdit()
        ed_reader_id.setPlaceholderText("example: 510000M")
        ed_title_id.setPlaceholderText("example: A1001")
        ed_number.setPlaceholderText("example: 3")
        ed_time.setPlaceholderText("example: 2020-01-01 12:00:00")
        
        layout.addRow("reader_id", ed_reader_id)
        layout.addRow("title_id:", ed_title_id)
        layout.addRow("number:", ed_number)
        layout.addRow("time:", ed_time)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(dlg.accept)
        btn_box.rejected.connect(dlg.reject)
        layout.addRow(btn_box)

        if not dlg.exec_():
            return  # 用户点Cancel直接返回
        
        reader_id_str = ed_reader_id.text().strip()
        title_id_str = ed_title_id.text().strip()
        num_str = ed_number.text().strip()
        time_str = ed_time.text().strip() if ed_time.text().strip() else QDateTime.currentDateTime().toString("yyyy-MM-dd HH:mm:ss")
        
        #校验数字与时间
        format_flag, format_msg = check_format(num_str, time_str)
        if not format_flag:
            QMessageBox.warning(self, "Input Error", format_msg)
            return
        
        #检查归还书本数量要求
        own_flag, own_msg = check_ownbook(reader_id_str, title_id_str, int(num_str))
        if not own_flag:
            QMessageBox.warning(self, "Id Error", own_msg)
            return
        
        return_flag, return_msg, stack = return_book(reader_id_str, title_id_str, int(num_str), time_str, stack)
        if not return_flag:
            QMessageBox.warning(self, "Return Error", return_msg)
        else:
            QMessageBox.information(self, "Success", return_msg)
        

    def on_click_e(self):
        if not self.check_privilege():
            return
        
        global stack
        dlg = QDialog(self)
        dlg.setWindowTitle("Register Book")
        dlg.resize(600, 400)
        
        flags = dlg.windowFlags()
        flags &= ~Qt.WindowContextHelpButtonHint  # 清除问号
        dlg.setWindowFlags(flags)
        
        layout = QFormLayout(dlg)
        
        ed_title_id = QLineEdit()
        ed_title = QLineEdit()
        ed_edition = QLineEdit()
        ed_year = QLineEdit()
        ed_author = QLineEdit()
        ed_price = QLineEdit()
        ed_title_id.setPlaceholderText("example: A1001")
        ed_title.setPlaceholderText("example: The Theroy of Relativity")
        ed_edition.setPlaceholderText("example: 1")
        ed_year.setPlaceholderText("example: 2001")
        ed_author.setPlaceholderText("example: Einstein")
        ed_price.setPlaceholderText("example: 39.80")
        
        layout.addRow("title_id:", ed_title_id)
        layout.addRow("title:", ed_title)
        layout.addRow("edition:", ed_edition)
        layout.addRow("year:", ed_year)
        layout.addRow("author", ed_author)
        layout.addRow("price", ed_price)
        
        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(dlg.accept)
        btn_box.rejected.connect(dlg.reject)
        layout.addRow(btn_box)

        if not dlg.exec_():
            return  # 用户点Cancel直接返回
        
        #获取输入
        title_id_str = ed_title_id.text().strip()
        title_str = ed_title.text().strip()
        edtion_str = ed_edition.text().strip()
        year_str = ed_year.text().strip()
        author_str = ed_author.text().strip()
        price_str = ed_price.text().strip()
        
        register_flag, register_msg, stack = register_book(title_id_str, title_str, int(edtion_str), int(year_str), author_str, Decimal(price_str), stack)
        if not register_flag:
            QMessageBox.warning(self, "Register Error", register_msg)
        else:
            QMessageBox.information(self, "Success", register_msg)

    def on_click_f(self):
        if not self.check_privilege():
            return
        
        global stack
        dlg = QDialog(self)
        dlg.setWindowTitle("Register Reader")
        dlg.resize(500, 200)
        
        flags = dlg.windowFlags()
        flags &= ~Qt.WindowContextHelpButtonHint  # 清除问号
        dlg.setWindowFlags(flags)
        
        layout = QFormLayout(dlg)
        
        ed_reader_id = QLineEdit()
        ed_reader_name = QLineEdit()
        ed_reader_id.setPlaceholderText("example: 510000M")
        ed_reader_name.setPlaceholderText("example: Zhang San")
        
        layout.addRow("reader_id:", ed_reader_id)
        layout.addRow("reader_name:", ed_reader_name)

        btn_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        btn_box.accepted.connect(dlg.accept)
        btn_box.rejected.connect(dlg.reject)
        layout.addRow(btn_box)

        if not dlg.exec_():
            return  # 用户点Cancel直接返回
        
        reader_id_str = ed_reader_id.text().strip()
        reader_name_str = ed_reader_name.text().strip()
        
        register_flag, register_msg, stack = register_reader(reader_id_str, reader_name_str, stack)
        if not register_flag:
            QMessageBox.warning(self, "Register Error", register_msg)
        else:
            QMessageBox.information(self, "Success", register_msg)
        
    def on_click_g(self):
        if not self.check_privilege():
            return
        
        global stack
        undo_flag, undo_msg, stack = inv_operation(stack)
        if not undo_flag:
            QMessageBox.warning(self, "Undo Error", undo_msg)
        else:
            QMessageBox.information(self, "Success", undo_msg)
        
    def on_click_h(self):
        self.switch_to_info.emit()
        
    def on_click_i(self):
        self.switch_to_announce.emit()

    def on_click_j(self):
        global stack
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle("Quit Confirmation")
        msg_box.setText("You can just log out or you can exit directly")
        msg_box.setIcon(QMessageBox.Question)

        # 添加三个自定义按钮，顺序即显示顺序
        btn_logout = msg_box.addButton("Log out", QMessageBox.ActionRole)
        btn_exit = msg_box.addButton("Exit", QMessageBox.ActionRole)
        btn_cancel = msg_box.addButton("Cancel", QMessageBox.RejectRole)

        # 阻塞显示弹窗
        msg_box.exec_()

        # 判断点击的按钮
        clicked = msg_box.clickedButton()
        if clicked == btn_logout:
            # 发射注销信号，由主窗口处理页面切换
            stack.clear()
            self.log_out_request.emit()
        elif clicked == btn_exit:
            # 直接退出整个应用
            QApplication.instance().quit()
