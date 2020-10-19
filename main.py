import sqlite3
import time
import pyautogui
# import getpass
import sys
import os
import webbrowser
# from selenium import webdriver
pyautogui.FAILSAFE = False


class MeetingDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('meetingdatabase.sqlite')
        self.cur = self.conn.cursor()

    def createTable(self):
        self.cur.execute('DROP TABLE IF EXISTS Database')
        self.cur.execute(
            '''CREATE TABLE Database (Subject TEXT, Day TEXT, 
            Hour INTEGER, IDMeeting TEXT, Password TEXT) ''')

    def gettingValues(self):

        try:
            self.subject = input("Enter the subject: ").strip().title()
            self.day = input(
                "Enter the class day (Example: Tuesday): ").strip().title()[:3]
            self.digitalHour = input(
                "Enter the class hour (Ex: 7:30, 15:00): ").split(':')
            self.classLength = input("Enter the Class Length(Ex: 2): ").strip()
            self.hour = int(self.digitalHour[0])

            try:
                self.minute = int(self.digitalHour[1])
            except ValueError:
                self.minute = int(self.digitalHour[1][1])
            if self.minute <= 10:
                self.minMinute = 50 + self.minute
                self.maxMinute = self.minMinute - 1
                self.minHour = self.hour - 1
                self.maxHour = self.hour + int(self.classLength) - 1
            else:
                self.minMinute = self.minute - 10
                self.maxMinute = self.minMinute - 1
                self.minHour = self.hour
                self.maxHour = self.hour + int(self.classLength)
        except ValueError:
            print("Put the correct Values")

    def addingToZoomDatabase(self):
        meeting = input("Enter the Zoom ID-Meeting: ").strip()
        password = input("Enter the meeting password: ").strip()
        self.cur.execute('''INSERT INTO ZoomDatabase (materia, dia, 
        hora, minuto, horaMinima, horaMaxima, minutoMin, minutoMax, 
        IDMeeting, Password) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (self.subject, self.day, self.hour, self.minute,
                          self.minHour, self.maxHour, self.minMinute,
                          self.maxMinute, meeting, password))
        self.conn.commit()

    def retrieveZoomMeeting(self, day, hour, minute):
        self.cur.execute(
            """SELECT IDMeeting, Password FROM ZoomDatabase WHERE dia='{}' 
            AND (hora={} OR (horaMinima={} AND {}>=minutoMin) OR 
            (horaMaxima={} AND minutoMax>={}))""".format(day, hour, hour, minute, hour, minute))
        return self.cur.fetchone()

    def deleteMeeting(self):
        try:
            subject = input(
                "Enter the subject that you want to delete: ").strip().title()
            day = input("Enter the class day: ").strip().title()[:3]
            digitalHour = input(
                "Enter the class hour (Ex: 7:30, 15:00): ").split(':')
            hour = int(digitalHour[0])
            self.cur.execute(
                f"SELECT materia FROM ZoomDatabase WHERE materia='{subject}' AND dia='{day}' AND hora={hour}")
            if self.cur.fetchone() is None:
                print("You have enter bad data. It's not in the database")
            else:
                self.cur.execute(
                    f"DELETE FROM ZoomDatabase WHERE materia='{subject}' AND dia='{day}' AND hora={hour}")
                self.conn.commit()
                print("You have deleted the meeting")
        except ValueError:
            print("Put the data in the right form")

    def addingToMeetDatabase(self):
        url = input("Enter the URL meeting: ").strip()
        self.cur.execute('''INSERT INTO MeetDatabase (materia, 
        dia, hora, minuto, horaMinima, horaMaxima, minutoMin, 
        minutoMax, url) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                         (self.subject, self.day, self.hour, self.minute, self.minHour,
                          self.maxHour, self.minMinute, self.maxMinute, url))
        self.conn.commit()

    def retrieveGoogleMeet(self, day, hour, minute):
        self.cur.execute('''SELECT url FROM MeetDatabase WHERE dia='{}' 
        AND (hora={} OR (horaMinima={} AND {}>=minutoMin) OR 
        (horaMaxima={} AND minutoMax>={}))'''.format(day, hour, hour, minute, hour, minute))
        return self.cur.fetchone()


class GoToClass:
    def __init__(self):
        pass

    def get_time(self):
        self.current_time = time.ctime().split()
        self.day = self.current_time[0]
        self.hour_min_sec = self.current_time[3].split(":")
        return self.day, int(self.hour_min_sec[0]), int(self.hour_min_sec[1])

    def robotic_arm(self, id, password):
        pyautogui.press('win')
        pyautogui.write('zoom')
        pyautogui.press('enter')

        coordinates = pyautogui.locateCenterOnScreen("button.png")
        while coordinates is None:
            coordinates = pyautogui.locateCenterOnScreen("button.png")
        # x, y = coordinates

        # time.sleep(0.5)
        pyautogui.click(coordinates)
        time.sleep(1)
        pyautogui.write(id)
        pyautogui.press('enter')
        time.sleep(2.5)
        pyautogui.write(password)
        pyautogui.press('enter')

    def meetEntry(self, url):
        PATH = 'C:/Program Files (x86)/Google/Chrome/Application/chrome.exe %s'
        webbrowser.get(PATH).open_new(url)
        time.sleep(3.5)
        # Para desactivar micrófono y cámara
        pyautogui.hotkey('ctrl', 'd')
        pyautogui.hotkey('ctrl', 'e')
        # Para ir al botón unirse
        for i in range(6):
            pyautogui.press('tab')
        # Presionar el botón "Unirse"
        pyautogui.press('enter')

    def meetEntrySelenium(self, url):
        PATH = os.getcwd() + "\\chromedriver.exe"
        options = webdriver.ChromeOptions()
        options.add_argument(
            r"--user-data-dir=C:\\Users\\Casa De Jose\\AppData\\Local\\Google\\Chrome\\User Data")
        options.add_argument("start-maximized")
        driver = webdriver.Chrome(PATH, options=options)
        driver.get(url)


def staying():
    answer = input("Do you want to stay?(yes/no): ").strip().lower()
    if answer == "yes" or answer == "y":
        print("*"*40)
        print("Welcome back.")
    elif answer == "no" or answer == "n":
        print("Until the next one")
        sys.exit(0)


def main():
    # create the instances
    zoomDatabase = MeetingDatabase()
    entry = GoToClass()
    googleMeet = MeetingDatabase()
    while True:
        print("1.Create Table")
        print("2.Add a Zoom Meeting")
        print("3.Delete a Zoom Meeting")
        print("4.Go to Zoom Class")
        print("5.Adding Google Meet URL")
        print("6.Go to Meet Class")
        print("7.Exit")
        print("*"*50)
        answer = input("What do you want to do?(1-7): ").strip()

        if answer == "1":
            zoomDatabase.createTable()
            print("You have made a new table.")
            staying()
        elif answer == "2":
            try:
                meetings = int(
                    input("How many meetings do you want to add?(Example: 2): "))
                n = 0
                while meetings > n:
                    zoomDatabase.gettingValues()
                    zoomDatabase.addingToZoomDatabase()
                    print("Meeting added to your database")
                    print("*"*50)
                    n += 1
            except ValueError:
                print("Enter a digit please.")

            staying()
        elif answer == "3":
            zoomDatabase.deleteMeeting()
            staying()
        elif answer == "4":
            day, hour, minute = entry.get_time()
            meetid_password = zoomDatabase.retrieveZoomMeeting(
                day, hour, minute)
            if meetid_password is None:
                print(
                    "This class doesn't exist. Check the data and remember that you can enter until 10 minutes before class.")
            else:
                id, password = meetid_password
                entry.robotic_arm(id, password)
            staying()

        elif answer == "5":
            googleMeet.gettingValues()
            googleMeet.addingToMeetDatabase()
            staying()

        elif answer == "6":
            day, hour, minute = entry.get_time()
            meetURL = googleMeet.retrieveGoogleMeet(day, hour, minute)
            if meetURL is None:
                print(
                    "This class doesn't exist. Check the data and remember that you can enter until 10 minutes before class.")
            else:
                entry.meetEntry(meetURL[0])
            staying()

        elif answer == "7":
            print("Until the next one.")
            zoomDatabase.cur.close()
            break
        elif answer == "8":
            day, hour, minute = entry.get_time()
            meetURL = googleMeet.retrieveGoogleMeet(day, hour, minute)
            if meetURL is None:
                print(
                    "This class doesn't exist. Check the data and remember that you can enter until 10 minutes before class.")
            else:
                entry.meetEntrySelenium(meetURL[0])
            staying()

        else:
            print("Invalid. Try again")
            print("*"*40)


if __name__ == '__main__':
    # ADMIN_PASSWORD = "CONTRASEA."
    print("Welcome to your Zoom-Automation Manager")
    print("*"*40)
    main()
    # try:
    # while True:
    #     getpassword = getpass.getpass("Enter your main Password: ")
    #     if getpassword == ADMIN_PASSWORD:
    #         main()
    #         break
    #     else:
    #         print("Invalid access.\nTry again or press Ctrl-C to exit")
    #         print("*"*40)

    # except KeyboardInterrupt:
    #     print("\nUntil the next one")
