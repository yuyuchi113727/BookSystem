from PyQt5.QtWidgets import (QWidget, QPushButton, QVBoxLayout, QHBoxLayout,
                             QLabel, QFrame, QSizePolicy, QTableWidget,
                             QTableWidgetItem, QHeaderView, QStackedWidget, QCheckBox)
from PyQt5.QtChart import QChart, QPieSeries, QPieSlice, QChartView
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QFont, QPainter, QColor
from operation import get_library, get_bookstore, get_readers, get_history, get_borrow, get_reader_rank, get_book_rank


class Graph(QWidget):
    # 返回Info页面的信号
    back_to_info = pyqtSignal()

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
        self.title_label = QLabel("Data Visualization")
        self.title_label.setFont(QFont("Microsoft YaHei", 17, QFont.Bold))
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color:#1f4b80;")
        title_layout.addWidget(self.title_label)
        main_layout.addWidget(self.title_panel)

        # ========== 中间内容展示区域（堆叠布局：占位 + 表格） ==========
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
        content_layout.setContentsMargins(30, 30, 30, 30)
        content_layout.setSpacing(20)
        
        self.query_tip_label = QLabel("当前查询：暂无")
        self.query_tip_label.setFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        self.query_tip_label.setStyleSheet("color: #1f4b80;")
        
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background: transparent;")

        self.chart_placeholder = QLabel("📊 图表展示区域\n\n可在此嵌入统计图表与数据表格")
        self.chart_placeholder.setFont(QFont("Microsoft YaHei", 12))
        self.chart_placeholder.setAlignment(Qt.AlignCenter)
        self.chart_placeholder.setStyleSheet("color: #667788;")

        #Table for books registered
        self.book_table = QTableWidget()
        self.book_table.setEditTriggers(QTableWidget.NoEditTriggers)    # 禁止编辑
        self.book_table.setSelectionBehavior(QTableWidget.SelectRows)  # 选中整行
        self.book_table.setSelectionMode(QTableWidget.SingleSelection) # 单选模式
        self.book_table.setAlternatingRowColors(True)                  # 隔行变色
        self.book_table.verticalHeader().setVisible(False)             # 隐藏左侧行号
        self.book_table.setColumnCount(6)
        book_headers = ["title_id", "title", "edition", "year", "author", "price"]
        self.book_table.setHorizontalHeaderLabels(book_headers)
        self.book_table.horizontalHeader().setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        self.book_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # 列宽自适应
        self.book_table.horizontalHeader().setFixedHeight(38)
        self.book_table.setStyleSheet("""
            QTableWidget {
                background: #ffffff;
                border: 1px solid #d0dce8;
                border-radius: 8px;
                gridline-color: #e6edf5;
                font-size: 14px;
                color: #2c3e50;
            }
            QTableWidget::item {
                padding: 8px 12px;
            }
            QTableWidget::item:selected {
                background-color: #e8f2ff;
                color: #1f4b80;
            }
            QHeaderView::section {
                background-color: #3b86e0;
                color: white;
                border: none;
                padding: 0 10px;
                font-weight: bold;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #3b86e0;
                border: none;
            }
        """)
        
        #Table for readers registered
        self.reader_table = QTableWidget()
        self.reader_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.reader_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.reader_table.setSelectionMode(QTableWidget.SingleSelection)
        self.reader_table.setAlternatingRowColors(True)
        self.reader_table.verticalHeader().setVisible(False)
        self.reader_table.setColumnCount(3)
        reader_headers = ["reader_id", "reader_name", "status"]
        self.reader_table.setHorizontalHeaderLabels(reader_headers)
        self.reader_table.horizontalHeader().setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        self.reader_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.reader_table.horizontalHeader().setFixedHeight(38)
        self.reader_table.setStyleSheet("""
            QTableWidget {
                background: #ffffff;
                border: 1px solid #d0dce8;
                border-radius: 8px;
                gridline-color: #e6edf5;
                font-size: 14px;
                color: #2c3e50;
            }
            QTableWidget::item {
                padding: 8px 12px;
            }
            QTableWidget::item:selected {
                background-color: #e8f2ff;
                color: #1f4b80;
            }
            QHeaderView::section {
                background-color: #3b86e0;
                color: white;
                border: none;
                padding: 0 10px;
                font-weight: bold;
                font-size:14px;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #3b86e0;
                border: none;
            }
        """)
        # ====== 新增：读者页容器（复选框 + 表格）======
        self.reader_page = QWidget()
        reader_page_layout = QVBoxLayout(self.reader_page)
        reader_page_layout.setContentsMargins(0, 0, 0, 0)
        reader_page_layout.setSpacing(12)

        # 复选框
        self.cb_only_overdue = QCheckBox("Show only overdue")
        self.cb_only_overdue.setStyleSheet("font-size: 15px; color: #2c3e50;")
        self.cb_only_overdue.stateChanged.connect(self.filter_reader_overdue)  # 绑定过滤函数

        reader_page_layout.addWidget(self.cb_only_overdue)
        reader_page_layout.addWidget(self.reader_table)
        
        #Table for books available now
        self.available_table = QTableWidget()
        self.available_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.available_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.available_table.setSelectionMode(QTableWidget.SingleSelection)
        self.available_table.setAlternatingRowColors(True)
        self.available_table.verticalHeader().setVisible(False)
        self.available_table.setColumnCount(5)
        available_headers = ["title_id", "title", "author", "remains", "borrowed"]
        self.available_table.setHorizontalHeaderLabels(available_headers)
        self.available_table.horizontalHeader().setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        self.available_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.available_table.horizontalHeader().setFixedHeight(38)
        self.available_table.setStyleSheet("""
            QTableWidget {
                background: #ffffff;
                border: 1px solid #d0dce8;
                border-radius: 8px;
                gridline-color: #e6edf5;
                font-size: 14px;
                color: #2c3e50;
            }
            QTableWidget::item {
                padding: 8px 12px;
            }
            QTableWidget::item:selected {
                background-color: #e8f2ff;
                color: #1f4b80;
            }
            QHeaderView::section {
                background-color: #3b86e0;
                color: white;
                border: none;
                padding: 0 10px;
                font-weight: bold;
                font-size:14px;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #3b86e0;
                border: none;
            }
        """)
        
        #Table for books history record
        self.history_table = QTableWidget()
        self.history_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.history_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.history_table.setSelectionMode(QTableWidget.SingleSelection)
        self.history_table.setAlternatingRowColors(True)
        self.history_table.verticalHeader().setVisible(False)
        self.history_table.setColumnCount(6)
        history_headers = ["title_id", "title", "author", "number", "time", "operation_type"]
        self.history_table.setHorizontalHeaderLabels(history_headers)
        self.history_table.horizontalHeader().setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.horizontalHeader().setFixedHeight(38)
        self.history_table.setStyleSheet("""
            QTableWidget {
                background: #ffffff;
                border: 1px solid #d0dce8;
                border-radius: 8px;
                gridline-color: #e6edf5;
                font-size: 14px;
                color: #2c3e50;
            }
            QTableWidget::item {
                padding: 8px 12px;
            }
            QTableWidget::item:selected {
                background-color: #e8f2ff;
                color: #1f4b80;
            }
            QHeaderView::section {
                background-color: #3b86e0;
                color: white;
                border: none;
                padding: 0 10px;
                font-weight: bold;
                font-size:14px;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #3b86e0;
                border: none;
            }
        """)
        
        self.history_page = QWidget()
        history_page_layout = QVBoxLayout(self.history_page)
        history_page_layout.setContentsMargins(0, 0, 0, 0)
        history_page_layout.setSpacing(12)

        cb_history_layout = QHBoxLayout()
        cb_history_layout.setSpacing(20)

        self.cb_only_purchase = QCheckBox("Show purchase Only")
        self.cb_only_purchase.setStyleSheet("font-size: 15px; color: #2c3e50;")
        self.cb_only_purchase.stateChanged.connect(self.on_history_purchase_check)

        self.cb_only_abandon = QCheckBox("Show abandon Only")
        self.cb_only_abandon.setStyleSheet("font-size: 15px; color: #2c3e50;")
        self.cb_only_abandon.stateChanged.connect(self.on_history_abandon_check)

        cb_history_layout.addWidget(self.cb_only_purchase)
        cb_history_layout.addWidget(self.cb_only_abandon)
        cb_history_layout.addStretch()

        history_page_layout.addLayout(cb_history_layout)
        history_page_layout.addWidget(self.history_table)
        
        #Table for books borrowed records
        self.borrow_table = QTableWidget()
        self.borrow_table.setEditTriggers(QTableWidget.NoEditTriggers)    # 禁止编辑
        self.borrow_table.setSelectionBehavior(QTableWidget.SelectRows)  # 选中整行
        self.borrow_table.setSelectionMode(QTableWidget.SingleSelection) # 单选模式
        self.borrow_table.setAlternatingRowColors(True)                  # 隔行变色
        self.borrow_table.verticalHeader().setVisible(False)             # 隐藏左侧行号
        self.borrow_table.horizontalHeader().setFont(QFont("Microsoft YaHei", 11, QFont.Bold))
        self.borrow_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch) # 列宽自适应
        self.borrow_table.horizontalHeader().setFixedHeight(38)
        self.borrow_table.setStyleSheet("""
            QTableWidget {
                background: #ffffff;
                border: 1px solid #d0dce8;
                border-radius: 8px;
                gridline-color: #e6edf5;
                font-size: 14px;
                color: #2c3e50;
            }
            QTableWidget::item {
                padding: 8px 12px;
            }
            QTableWidget::item:selected {
                background-color: #e8f2ff;
                color: #1f4b80;
            }
            QHeaderView::section {
                background-color: #3b86e0;
                color: white;
                border: none;
                padding: 0 10px;
                font-weight: bold;
            }
            QTableWidget QTableCornerButton::section {
                background-color: #3b86e0;
                border: none;
            }
        """)
        
        #Pie chart for bookworms 
        self.reader_rank_chart = QChart()
        self.reader_rank_chart.setTitle("Top Bookworms Ranking")
        self.reader_rank_chart.setTitleFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        self.reader_rank_chart.setTitleBrush(QColor("#1f4b80"))
        self.reader_rank_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.reader_rank_chart.legend().setFont(QFont("Microsoft YaHei", 11))
        self.reader_rank_chart.legend().setAlignment(Qt.AlignRight)
        self.reader_rank_chart.setBackgroundRoundness(8)
        self.reader_rank_chart.layout().setContentsMargins(10, 10, 10, 10)

        self.reader_rank_view = QChartView(self.reader_rank_chart)
        self.reader_rank_view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.reader_rank_view.setStyleSheet("""
            QChartView {
                background: #ffffff;
                border: 1px solid #d0dce8;
                border-radius: 8px;
            }
        """)
        
        #Pie chart for bestsellers 
        self.book_rank_chart = QChart()
        self.book_rank_chart.setTitle("Top Bestsellers Ranking")
        self.book_rank_chart.setTitleFont(QFont("Microsoft YaHei", 14, QFont.Bold))
        self.book_rank_chart.setTitleBrush(QColor("#1f4b80"))
        self.book_rank_chart.setAnimationOptions(QChart.SeriesAnimations)
        self.book_rank_chart.legend().setFont(QFont("Microsoft YaHei", 11))
        self.book_rank_chart.legend().setAlignment(Qt.AlignRight)
        self.book_rank_chart.setBackgroundRoundness(8)
        self.book_rank_chart.layout().setContentsMargins(10, 10, 10, 10)

        self.book_rank_view = QChartView(self.book_rank_chart)
        self.book_rank_view.setRenderHint(QPainter.Antialiasing)  # 抗锯齿
        self.book_rank_view.setStyleSheet("""
            QChartView {
                background: #ffffff;
                border: 1px solid #d0dce8;
                border-radius: 8px;
            }
        """)

        # 加入堆叠容器
        self.content_stack.addWidget(self.chart_placeholder) # 索引0：占位页
        self.content_stack.addWidget(self.book_table)        # 索引1：图书表格页
        self.content_stack.addWidget(self.reader_page)       # 索引2：读者表格页
        self.content_stack.addWidget(self.available_table)   # 索引3：图书库存页
        self.content_stack.addWidget(self.history_page)      # 索引4：历史周转页
        self.content_stack.addWidget(self.borrow_table)      # 索引5：借阅查询页
        self.content_stack.addWidget(self.reader_rank_view)  # 索引6：读者借阅排行
        self.content_stack.addWidget(self.book_rank_view)    # 索引7：畅销书排行
        
        content_layout.addWidget(self.query_tip_label)
        content_layout.addWidget(self.content_stack, stretch=1)
        
        main_layout.addWidget(self.content_panel, stretch=1)

        # ========== 底部返回按钮 ==========
        btn_layout = QHBoxLayout()
        btn_layout.addStretch()
        self.btn_back = QPushButton("back")
        
        # 按钮样式与其他页面完全统一
        btn_css = """
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
        """
        self.btn_back.setStyleSheet(btn_css)
        self.btn_back.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        btn_layout.addWidget(self.btn_back)
        btn_layout.addStretch()
        main_layout.addLayout(btn_layout)

        # 绑定点击事件
        self.btn_back.clicked.connect(self.on_back_to_info)

    # ====================== 外部调用接口 ======================
    def set_query_type(self, query_type: str, reader_id = None, title_id = None):
        type_name_map = {
            "search_book": "Table for Books Registered",
            "search_reader": "Table for Readers Registered",
            "search_available": "Table for Books Available Now",
            "search_history": "Table for Books History Record",
            "search_borrow": f"Reader {reader_id}: Table for Books Borrowed" if reader_id is not None else f"Book {title_id}: Table for Books Borrowed",
            "calculate_reader": "Pie Chart for Rank Bookworms",
            "calculate_book": "Pie Chart for Rank Bestsells"
        }
        display_name = type_name_map.get(query_type, "Unknown query type")
        self.query_tip_label.setText(f"{display_name}")
        
        if query_type == "search_book":
            self.content_stack.setCurrentWidget(self.book_table)
            self.load_book_data()
        elif query_type == "search_reader":
            self.content_stack.setCurrentWidget(self.reader_page)
            self.cb_only_overdue.setChecked(False)
            self.load_reader_data()
            self.filter_reader_overdue()
        elif query_type == "search_available":
            self.content_stack.setCurrentWidget(self.available_table)
            self.load_available_data()
        elif query_type == "search_history":
            self.content_stack.setCurrentWidget(self.history_page)
            self.cb_only_purchase.setChecked(False)
            self.cb_only_abandon.setChecked(False)
            self.load_history_data()
            self.filter_history_type()
        elif query_type == "search_borrow":
            self.content_stack.setCurrentWidget(self.borrow_table)
            self.load_borrow_data(reader_id, title_id)
        elif query_type == "calculate_reader":
            self.content_stack.setCurrentWidget(self.reader_rank_view)
            self.load_reader_rank()
        elif query_type == "calculate_book":
            self.content_stack.setCurrentWidget(self.book_rank_view)
            self.load_book_rank()
        else:
            self.content_stack.setCurrentWidget(self.chart_placeholder)
            self.chart_placeholder.setText(f"📊 {display_name}\n\n功能开发中，敬请期待")

    # ====================== 业务方法 ======================
    #button 1
    def load_book_data(self):
        self.book_table.setRowCount(0)
        
        rows = get_library()
        if not rows:
            self.book_table.setRowCount(1)
            empty_item = QTableWidgetItem("No books registered")
            empty_item.setTextAlignment(Qt.AlignCenter)
            empty_item.setForeground(Qt.gray)
            self.book_table.setItem(0, 0, empty_item)
            self.book_table.setSpan(0, 0, 1, 6) 
            return
        
        self.book_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.book_table.setItem(row_idx, col_idx, item)
    
    #button 2            
    def load_reader_data(self):
        self.reader_table.setRowCount(0)
        rows = get_readers()
        if not rows:
            self.reader_table.setRowCount(1)
            empty_item = QTableWidgetItem("No readers registered")
            empty_item.setTextAlignment(Qt.AlignCenter)
            empty_item.setForeground(Qt.gray)
            self.reader_table.setItem(0, 0, empty_item)
            self.reader_table.setSpan(0, 0, 1, 3)
            return

        self.reader_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.reader_table.setItem(row_idx, col_idx, item)
                
    def filter_reader_overdue(self):
        show_only_overdue = self.cb_only_overdue.isChecked()
        for row in range(self.reader_table.rowCount()):
            status_item = self.reader_table.item(row, 2)  # status是第3列，索引为2
            if not status_item:
                continue
            if show_only_overdue:
                self.reader_table.setRowHidden(row, status_item.text() != "overdue")
            else:
                self.reader_table.setRowHidden(row, False)
    
    #button 3
    def load_available_data(self):
        self.available_table.setRowCount(0)
        
        rows = get_bookstore()
        if not rows:
            self.available_table.setRowCount(1)
            empty_item = QTableWidgetItem("No books available now")
            empty_item.setTextAlignment(Qt.AlignCenter)
            empty_item.setForeground(Qt.gray)
            self.available_table.setItem(0, 0, empty_item)
            self.available_table.setSpan(0, 0, 1, 5) 
            return
        
        self.available_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.available_table.setItem(row_idx, col_idx, item)
    
    #button 4            
    def on_history_purchase_check(self):
        if self.cb_only_purchase.isChecked():
            self.cb_only_abandon.setChecked(False)
        self.filter_history_type()

    def on_history_abandon_check(self):
        if self.cb_only_abandon.isChecked():
            self.cb_only_purchase.setChecked(False)
        self.filter_history_type()

    def filter_history_type(self):
        show_purchase = self.cb_only_purchase.isChecked()
        show_abandon = self.cb_only_abandon.isChecked()

        for row in range(self.history_table.rowCount()):
            type_item = self.history_table.item(row, 5)  # operation_type在第6列，索引为5
            if not type_item:
                continue
            op_type = type_item.text()

            if show_purchase:
                self.history_table.setRowHidden(row, op_type != "purchase")
            elif show_abandon:
                self.history_table.setRowHidden(row, op_type != "abandon")
            else:
                self.history_table.setRowHidden(row, False)

    def load_history_data(self):
        self.history_table.setRowCount(0)

        rows = get_history()
        if not rows:
            self.history_table.setRowCount(1)
            empty_item = QTableWidgetItem("No history records")
            empty_item.setTextAlignment(Qt.AlignCenter)
            empty_item.setForeground(Qt.gray)
            self.history_table.setItem(0, 0, empty_item)
            self.history_table.setSpan(0, 0, 1, 6)
            return

        self.history_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.history_table.setItem(row_idx, col_idx, item)
    
    #button 5
    def load_borrow_data(self, reader_id = None, title_id = None):
        self.borrow_table.setRowCount(0)
        
        rows = get_borrow(reader_id, title_id)
        if reader_id is not None:
            self.borrow_table.setColumnCount(6)
            headers = ["title_id", "title", "author", "borrow_time", "not_returned", "due_time"]
        else:
            self.borrow_table.setColumnCount(4)
            headers = ["reader_id", "reader_name", "borrow_time", "due_time"]
            
        self.borrow_table.setHorizontalHeaderLabels(headers)
        
        if not rows:
            self.borrow_table.setRowCount(1)
            empty_item = QTableWidgetItem("No history records")
            empty_item.setTextAlignment(Qt.AlignCenter)
            empty_item.setForeground(Qt.gray)
            self.borrow_table.setItem(0, 0, empty_item)
            self.borrow_table.setSpan(0, 0, 1, 6) if reader_id is not None else self.borrow_table.setSpan(0, 0, 1, 4)
            return
        
        self.borrow_table.setRowCount(len(rows))
        for row_idx, row_data in enumerate(rows):
            for col_idx, value in enumerate(row_data):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                self.borrow_table.setItem(row_idx, col_idx, item)
    
    #button 6
    def load_reader_rank(self):
        rank_data = get_reader_rank()
        self.reader_rank_chart.removeAllSeries()
        if not rank_data:
            self.reader_rank_chart.setTitle("No readers yet.")
            self.reader_rank_chart.legend().setVisible(False)
            return
    
        self.reader_rank_chart.setTitle("")
        self.reader_rank_chart.legend().setVisible(True)
        series = QPieSeries()
        colors = [QColor("#3b86e0"), QColor("#5a9ce8"), QColor("#7bb3ef"),
              QColor("#9cc9f5"), QColor("#bddffb")]
    
        # 计算总数
        total = sum(count for _, count in rank_data)
    
        for idx, (name, count) in enumerate(rank_data):
            percent = count / total * 100
            label_text = f"{name}: {percent:.1f}%"
            slice_item = QPieSlice(label_text, count)
            slice_item.setBrush(colors[idx % len(colors)])
            slice_item.setLabelFont(QFont("Microsoft YaHei", 8))
            series.append(slice_item)
    
        if series.slices():
            series.slices()[0].setExploded(True)
            series.slices()[0].setExplodeDistanceFactor(0.12)
    
        series.setLabelsVisible(True)
        self.reader_rank_chart.addSeries(series)
    
    #button 7    
    def load_book_rank(self):
        rank_data = get_book_rank()
        self.book_rank_chart.removeAllSeries()
        if not rank_data:
            self.book_rank_chart.setTitle("No Books yet.")
            self.book_rank_chart.legend().setVisible(False)
            return
    
        self.book_rank_chart.setTitle("")
        self.book_rank_chart.legend().setVisible(True)
        series = QPieSeries()
        colors = [QColor("#3b86e0"), QColor("#5a9ce8"), QColor("#7bb3ef"),
              QColor("#9cc9f5"), QColor("#bddffb")]
        
        # 计算总数
        total = sum(count for _, count in rank_data)

        for idx, (name, count) in enumerate(rank_data):
            percent = count / total * 100
            label_text = f"{name}: {percent:.1f}%"
            slice_item = QPieSlice(label_text, count)
            slice_item.setBrush(colors[idx % len(colors)])
            slice_item.setLabelFont(QFont("Microsoft YaHei", 8))
            series.append(slice_item)
    
        if series.slices():
            series.slices()[0].setExploded(True)
            series.slices()[0].setExplodeDistanceFactor(0.12)
    
        series.setLabelsVisible(True)
        self.book_rank_chart.addSeries(series)

    def on_back_to_info(self):
        self.back_to_info.emit()
