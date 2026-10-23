import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QStackedWidget
from login import Login
from home import Home
from info import Info
from graph import Graph  # 导入Graph页面

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PB24331912 Database Homework")
        self.resize(1200, 800)

        self.stack = QStackedWidget()
        self.setCentralWidget(self.stack)

        # 初始化所有页面
        self.login = Login()
        self.home = Home()
        self.info = Info()
        self.graph = Graph()

        # 添加到堆栈（索引依次为 0、1、2、3）
        self.stack.addWidget(self.login)
        self.stack.addWidget(self.home)
        self.stack.addWidget(self.info)
        self.stack.addWidget(self.graph)

        # 默认显示登录页
        self.stack.setCurrentIndex(0)

        # 登录 → 首页
        self.login.switch_to_home.connect(self.handle_go_to_home)
        # 首页 → 登录
        self.home.log_out_request.connect(self.handle_go_to_login)
        # 首页 → Info
        self.home.switch_to_info.connect(self.handle_go_to_info)
        # Info → 首页
        self.info.back_to_home.connect(self.handle_back_to_home)
        # Info → Graph
        self.info.switch_to_graph.connect(self.handle_go_to_graph)
        # Graph → Info
        self.graph.back_to_info.connect(self.handle_back_to_info)

    # -------------------------- 页面切换槽函数 --------------------------
    def handle_go_to_home(self, role: str):
        self.home.set_user_role(role)
        self.stack.setCurrentWidget(self.home)

    def handle_go_to_login(self):
        self.stack.setCurrentWidget(self.login)

    def handle_go_to_info(self):
        self.stack.setCurrentWidget(self.info)

    def handle_back_to_home(self):
        self.stack.setCurrentWidget(self.home)

    def handle_go_to_graph(self, query_type: str, reader_id, title_id):
        self.graph.set_query_type(query_type, reader_id, title_id)
        self.stack.setCurrentWidget(self.graph)

    def handle_back_to_info(self):
        self.stack.setCurrentWidget(self.info)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
