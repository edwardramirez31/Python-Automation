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

        self.widgets_group_1 = {
            "Materia": QLineEdit(),
            "ID de la reunión": QLineEdit(),
            "Password": QLineEdit()
        }
        # Meeting group data
        self.group_box = QGroupBox("Datos de la reunión")
        form_layout = QFormLayout()
        for name, widget in self.widgets_group_1.items():
            form_layout.addRow(name, widget)

        self.group_box.setLayout(form_layout)

        # Date grou data
        self.widgets_group_2 = {
            "Seleccione un día": QComboBox(),
            "Seleccione la hora": QTimeEdit(),
            "Duración (horas)": QSpinBox()
        }
        self.group_box2 = QGroupBox("Fecha y Hora")
        form_layout2 = QFormLayout()
        self.group_box2.setLayout(form_layout2)

        for name, widget in self.widgets_group_2.items():
            form_layout2.addRow(name, widget)

        # ComboBox for the days
        self.widgets_group_2["Seleccione un día"].addItems(self.days.keys())
        self.widgets_group_2["Seleccione la hora"].setTime(QTime.currentTime())
        self.widgets_group_2["Seleccione la hora"].setDisplayFormat("HH:mm")

        # https://codetorial.net/en/pyqt5/widget/qtimeedit.html

        # Tab2 Main Layout
        self.tab2_layout = QVBoxLayout()
        self.tab2_layout.addWidget(self.group_box)
        self.tab2_layout.addWidget(self.group_box2)
        self.tab2.setLayout(self.tab2_layout)

        self.get_values_button = QPushButton("Submit")
        self.get_values_button.clicked.connect(self.get_values)
        self.tab2_layout.addWidget(self.get_values_button)

    def get_values(self):
        self.values = list()
        for widget in self.widgets_group_1.values():
            self.values.append(widget.text())
        self.day = self.widgets_group_2["Seleccione un día"].currentText()
        self.hour = self.widgets_group_2["Seleccione la hora"].time(
        ).toString()
        self.length = self.widgets_group_2["Duración (horas)"].value()
        print(self.day, self.hour, self.length, self.values)

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
