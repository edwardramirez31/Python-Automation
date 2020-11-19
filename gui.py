import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QMessageBox, QFormLayout, QGroupBox
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot
from main import GoToClass, MeetingDatabase


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'AutoMeet'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.table_widget = MyTableWidget(self)
        self.setCentralWidget(self.table_widget)

        self.show()


class MyTableWidget(QWidget):

    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.layout = QVBoxLayout(self)

        # Initialize tab screen
        self.tabs = QTabWidget()
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Main Page")
        self.tabs.addTab(self.tab2, "Add a Meet")

        # Create first tab
        self.tab1_layout = QVBoxLayout()
        self.pushButton1 = QPushButton("Go to class")
        self.pushButton1.clicked.connect(self.go_to_class)

        self.tab1_layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1_layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.initial_settings()
        self.go_to_class()

    def initial_settings(self):
        self.entry = GoToClass()
        self.zoom = MeetingDatabase()

    def go_to_class(self):

        day, hour, minute = self.entry.get_time()
        meetid_password = self.zoom.retrieveZoomMeeting(
            day, hour, minute)
        if meetid_password is None:
            QMessageBox.critical(self, "ERROR", "This class doesn't exist.")
        else:
            id, password = meetid_password
            self.entry.robotic_arm(id, password)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    sys.exit(app.exec_())
