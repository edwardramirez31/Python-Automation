import sqlite3
import time
import pyautogui
import getpass
import sys
import os
from selenium import webdriver
import webbrowser


class MeetingDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('meetingdatabase.sqlite')
        self.cur = self.conn.cursor()

    def createTable(self):
        self.cur.execute('DROP TABLE IF EXISTS Database')
        self.cur.execute(
            'CREATE TABLE Database (Subject TEXT, Day TEXT, Hour INTEGER, IDMeeting TEXT, Password TEXT)')

    def addingMeeting(self):
        try:
            subject = input("Enter the subject: ").strip().title()
            day = input("Enter the class day: ").strip().title()[:3]
            hour = int(input("Enter the class hour: ").strip())
            meeting = input("Enter the Zoom ID-Meeting: ").strip()
            password = input("Enter the meeting password: ").strip()
            self.cur.execute('INSERT INTO Database (Subject, Day, Hour, IDMeeting, Password) VALUES (?, ?, ?, ?, ?)',
                             (subject, day, hour, meeting, password))
            self.conn.commit()
        except ValueError:
            print("Put the correct Values")

    def retrieveMeeting(self, day, hour, minute):
        self.cur.execute(
            "SELECT IDMeeting, Password FROM Database WHERE Day='{}' AND (Hour={} OR Hour={}+1 AND {}>49)".format(day, hour, hour, minute))
        return self.cur.fetchone()

    def deleteMeeting(self):
        try:
            subject = input(
                "Enter the subject that you want to delete: ").strip().title()
            day = input("Enter the class day: ").strip().title()[:3]
            hour = int(input("Enter the hour: "))
            self.cur.execute(
                f"SELECT Subject FROM Database WHERE Subject='{subject}' AND Day='{day}' AND Hour={hour}")
            if self.cur.fetchone() is None:
                print("You have enter bad data. It's not in the database")
            else:
                self.cur.execute(
                    f"DELETE FROM Database WHERE Subject='{subject}' AND Day='{day}' AND Hour={hour}")
                self.conn.commit()
                print("You have deleted the meeting")
        except ValueError:
            print("Put the data in the right form")


class MeetDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('meetingdatabase.sqlite')
        self.cur = self.conn.cursor()

    def addingMeeting(self):
        try:
            subject = input("Enter the subject: ").strip().title()
            day = input("Enter the class day: ").strip().title()[:3]
            hour = int(input("Enter the class hour: ").strip())
            meeting = input("Enter the Meeting URL: ").strip()
            self.cur.execute('INSERT INTO GoogleMeet (Subject, Day, Hour, MeetingURL) VALUES (?, ?, ?, ?)',
                             (subject, day, hour, meeting))
            self.conn.commit()
        except ValueError:
            print("Put the data in its correct form")

    def retrieveMeetURL(self, day, hour, minute):
        self.cur.execute(
            'SELECT MeetingURL FROM GoogleMeet WHERE Day=? AND (Hour=? AND ?<50 OR (Hour=?+1 AND ?>49))', (day, hour, minute, hour, minute))
        return self.cur.fetchone()


class EntryZoom:
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
        time.sleep(0.5)
        pyautogui.write(id)
        pyautogui.press('enter')
        time.sleep(1.5)
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
        driver = webdriver.Chrome(PATH)
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
    entry = EntryZoom()
    googleMeet = MeetDatabase()
    while True:
        print("1.Create Table")
        print("2.Add Meetings")
        print("3.Delete Meetings")
        print("4.Go to class")
        print("5.Adding Meet URL")
        print("6.Go to Meet Class")
        print("7.Exit")
        print("*"*40)
        answer = input("What do you want to do?(1-7): ").strip()

        if answer == "1":
            zoomDatabase.createTable()
            print("You have made a new table.")
            staying()
        elif answer == "2":
            zoomDatabase.addingMeeting()
            print("Meeting added to your database")
            staying()
        elif answer == "3":
            zoomDatabase.deleteMeeting()
            staying()
        elif answer == "4":
            day, hour, minute = entry.get_time()
            meetid_password = zoomDatabase.retrieveMeeting(day, hour, minute)
            if meetid_password is None:
                print(
                    "This class doesn't exist. Check the data and remember that you can enter until 10 minutes before class.")
            else:
                id, password = meetid_password
                entry.robotic_arm(id, password)
            staying()
        elif answer == "7":
            print("Until the next one.")
            zoomDatabase.cur.close()
            break
        elif answer == "5":

            googleMeet.addingMeeting()

        elif answer == "6":
            day, hour, minute = entry.get_time()
            meetURL = googleMeet.retrieveMeetURL(day, hour, minute)
            if meetURL is None:
                print(
                    "This class doesn't exist. Check the data and remember that you can enter until 10 minutes before class.")
            else:
                entry.meetEntry(meetURL[0])
            staying()

        else:
            print("Invalid. Try again")
            print("*"*40)


if __name__ == '__main__':
    ADMIN_PASSWORD = "CONTRASEA."
    print("Welcome to your Zoom-Automation Manager")
    print("*"*40)
    try:
        while True:
            getpassword = getpass.getpass("Enter your main Password: ")
            if getpassword == ADMIN_PASSWORD:
                main()
                break
            else:
                print("Invalid access.\nTry again or press Ctrl-C to exit")
                print("*"*40)

    except KeyboardInterrupt:
        print("\nUntil the next one")
