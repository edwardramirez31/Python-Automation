import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QMessageBox, QFormLayout, QGroupBox, QLineEdit, QSpinBox, QComboBox, QTimeEdit
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QTime
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

        self.add_meeting_form()
        self.initial_settings()

    def add_meeting_form(self):
        self.days = {
            "Lunes": "Mon",
            "Martes": "Tue",
            "Miércoles": "Wed",
            "Jueves": "Thu",
            "Viernes": "Fri",
            "Sábado": "Sat"}
        # Meeting group data
        self.group_box = QGroupBox("Datos de la reunión")
        form_layout = QFormLayout()
        form_layout.addRow("Name:", QLineEdit())
        form_layout.addRow("ID de la reunión:", QLineEdit())
        form_layout.addRow("Password", QLineEdit())
        self.group_box.setLayout(form_layout)

        # Date grou data
        self.group_box2 = QGroupBox("Fecha y Hora")
        form_layout2 = QFormLayout()

        # ComboBox for the days
        self.combo_days = QComboBox()
        self.combo_days.addItems(self.days.keys())
        form_layout2.addRow("Seleccione el día:", self.combo_days)
        # Widget used to get the hour
        self.time_edit = QTimeEdit()
        self.time_edit.setTime(QTime.currentTime())
        self.time_edit.setDisplayFormat("HH:mm")
        # https://codetorial.net/en/pyqt5/widget/qtimeedit.html
        form_layout2.addRow("Seleccione la hora:", self.time_edit)
        # Widget used to get the class length
        self.hours = QSpinBox()
        self.hours.setMaximum(20)
        form_layout2.addRow("Duración (horas)", self.hours)
        self.group_box2.setLayout(form_layout2)

        # Tab2 Main Layout
        self.tab2_layout = QVBoxLayout()
        self.tab2_layout.addWidget(self.group_box)
        self.tab2_layout.addWidget(self.group_box2)
        self.tab2.setLayout(self.tab2_layout)

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
