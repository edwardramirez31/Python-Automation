import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QPushButton, QWidget, QAction, QTabWidget, QVBoxLayout, QMessageBox, QFormLayout, QGroupBox, QLineEdit, QSpinBox, QComboBox, QTimeEdit, QLabel
from PyQt5.QtCore import QTime
from main import GoToClass, MeetingDatabase
import sqlite3
import qdarkstyle
# import qdarkgraystyle
from PyQt5.QtGui import QPixmap

class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.title = 'AutoMeet'
        self.left = 0
        self.top = 0
        self.width = 250
        self.height = 200
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)
        self.setStyleSheet("font-size: 14px;")
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
        self.tab3 = QWidget()
        self.tabs.resize(300, 200)

        # Add tabs
        self.tabs.addTab(self.tab1, "Main Page")
        self.tabs.addTab(self.tab2, "Add a Meet")
        self.tabs.addTab(self.tab3, "Eliminar Reunión")

        # Create first tab
        self.tab1_layout = QVBoxLayout()
        self.pushButton1 = QPushButton("Go to class")
        self.pushButton1.setStyleSheet("font-weight: bold;")

        self.pushButton1.clicked.connect(self.go_to_class)

        labelImage = QLabel(self)
        pixmap = QPixmap("logo21.png")
        labelImage.setPixmap(pixmap)

        self.tab1_layout.addWidget(labelImage)
        self.tab1_layout.addWidget(self.pushButton1)
        self.tab1.setLayout(self.tab1_layout)

        # Add tabs to widget
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        self.add_meeting_form()
        self.deleteTabWidget()
        self.initial_settings()

    def add_meeting_form(self):
        self.days = {
            "Lunes": "Mon",
            "Martes": "Tue",
            "Miércoles": "Wed",
            "Jueves": "Thu",
            "Viernes": "Fri",
            "Sábado": "Sat",
            "Domingo": "Sun"
            }

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
        self.widgets_group_2["Duración (horas)"].setMinimum(1)
        # Tab2 Main Layout
        self.tab2_layout = QVBoxLayout()
        self.tab2_layout.addWidget(self.group_box)
        self.tab2_layout.addWidget(self.group_box2)
        self.tab2.setLayout(self.tab2_layout)

        self.get_values_button = QPushButton("Submit")
        self.get_values_button.setStyleSheet("font-weight: bold;")
        self.get_values_button.clicked.connect(self.get_values)
        self.tab2_layout.addWidget(self.get_values_button)

    def get_values(self):
        self.values = list()
        for widget in self.widgets_group_1.values():
            if widget.text() == "":
                QMessageBox.critical(self, "ERROR", "Rellene todos los campos.")
                break
            else:
                self.values.append(widget.text())

        if len(self.values) == 3:
            self.day = self.widgets_group_2["Seleccione un día"].currentText()
            self.hour_String = self.widgets_group_2["Seleccione la hora"].time().toString()
            self.length = self.widgets_group_2["Duración (horas)"].value()
            self.time_handler()
        

    def time_handler(self):
        self.hour_list = self.hour_String.split(":")
        self.hour = self.hour_list[0]
        try:
            self.minute = int(self.hour_list[1])
            self.hour = int(self.hour_list[0])
        except ValueError:
            self.minute = int(self.hour_list[1][1])
            self.hour = int(self.hour_list[0][1])

        if self.minute <= 10:
            self.minMinute = 50 + self.minute
            self.maxMinute = self.minMinute - 1
            self.minHour = self.hour - 1
            self.maxHour = self.hour + int(self.length) - 1
        else:
            self.minMinute = self.minute - 10
            self.maxMinute = self.minMinute - 1
            self.minHour = self.hour
            self.maxHour = self.hour + int(self.length)
        self.add_meeting_zoom()

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

    def add_meeting_zoom(self):
        self.conn = sqlite3.connect('meetingdatabase.sqlite')
        self.cur = self.conn.cursor()
        self.cur.execute('''INSERT INTO ZoomDatabase (materia, dia, 
        hora, minuto, horaMinima, horaMaxima, minutoMin, minutoMax, 
        IDMeeting, Password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (self.values[0], self.days[self.day], self.hour, self.minute,
                          self.minHour, self.maxHour, self.minMinute,
                          self.maxMinute, self.values[1], self.values[2]))
        self.conn.commit()
        self.cur.close()
        self.delete_items()

    def delete_items(self):
        for widget in self.widgets_group_1.values():
            widget.setText("")

    def deleteTabWidget(self):
        self.deleteSubject = QLineEdit()
        self.hour_delete = QTimeEdit()
        self.day_delete = QComboBox()
        self.day_delete.addItems(self.days.keys())
        self.hour_delete.setTime(QTime.currentTime())
        self.hour_delete.setDisplayFormat("HH:mm")
        # Meeting group data
        self.group_box_delete = QGroupBox("Datos de la reunión a eliminar")
        delete_form_layout = QFormLayout()
        delete_form_layout.addRow("Materia:", self.deleteSubject)
        delete_form_layout.addRow("Día:", self.day_delete)
        delete_form_layout.addRow("Hora:", self.hour_delete)

        self.group_box_delete.setLayout(delete_form_layout)
        #main layout
        self.tab3_layout = QVBoxLayout()
        self.tab3_layout.addWidget(self.group_box_delete)
        self.tab3.setLayout(self.tab3_layout)
        # Date grou data
        self.delete_values_button = QPushButton("Eliminar")
        self.delete_values_button.setStyleSheet("font-weight: bold;")
        self.delete_values_button.clicked.connect(self.delete_meeting)
        self.tab3_layout.addWidget(self.delete_values_button)
    


    def delete_meeting(self):
        self.day_to_delete = self.day_delete.currentText()
        self.hour_String = self.hour_delete.time().toString()
        self.hour_list = self.hour_String.split(":")
        self.hour = self.hour_list[0]
        try:
            self.hour = int(self.hour_list[0])
        except ValueError:
            self.hour = int(self.hour_list[0][1])
        self.subject_to_delete = self.deleteSubject.text()

        if self.subject_to_delete == "":
            QMessageBox.critical(self, "ERROR", "Rellene todos los campos.")
        else:
            self.conn = sqlite3.connect('meetingdatabase.sqlite')
            self.cur = self.conn.cursor()
            self.cur.execute(
                f"SELECT materia FROM ZoomDatabase WHERE materia='{self.subject_to_delete}' AND dia='{self.days[self.day_to_delete]}' AND hora={self.hour}")
            if self.cur.fetchone() is None:
                QMessageBox.critical(self, "ERROR", "La reunión no está en la base de datos")
            else:
                self.cur.execute(
                    f"DELETE FROM ZoomDatabase WHERE materia='{self.subject_to_delete}' AND dia='{self.days[self.day_to_delete]}' AND hora={self.hour}")
                self.cur.close()
                self.conn.commit()
                QMessageBox.information(self, "SUCCESS", "La reunión fue eliminada")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = App()
    # setup stylesheet
    app.setStyleSheet(qdarkstyle.load_stylesheet_pyqt5())
    # app.setStyleSheet(qdarkgraystyle.load_stylesheet())
    # control = Controller(window)
    sys.exit(app.exec_())
