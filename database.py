import sqlite3, time, pyautogui, getpass, sys

class MeetingDatabase:
    def __init__(self):
        self.conn = sqlite3.connect('meetingdatabase.sqlite')
        self.cur = self.conn.cursor()

    def createTable(self):
        self.cur.execute('DROP TABLE IF EXISTS Database')
        self.cur.execute('CREATE TABLE Database (Subject TEXT, Day TEXT, Hour INTEGER, IDMeeting TEXT, Password TEXT)')

    def addingMeeting(self):
        subject = input("Enter the subject: ").strip().title()
        day = input("Enter the class day: ").strip().title()
        hour = int(input("Enter the class hour: ").strip().title()
        meeting = input("Enter the Zoom ID-Meeting: ").strip().title()
        password = input("Enter the meeting password: ").strip().title()
        self.cur.execute('INSERT INTO Database (Subject, Day, Hour, IDMeeting, Password) VALUES (?, ?, ?, ?, ?)', (subject, day, hour, meeting, password))
        self.conn.commit()

    def retrieveMeeting(self, day, hour, minute):
        self.cur.execute("SELECT IDMeeting, Password FROM Database WHERE Day='{}' AND (Hour={} OR Hour={}+1 AND {}>49)".format(day, hour, hour, minute))
        return self.cur.fetchone()

    def deleteMeeting(self):
        subject = input("Enter the subject that you want to delete: ").strip().title()
        day = input("Enter the class day: ").strip().title()
        hour = int(input("Enter the hour: "))
        self.cur.execute(f"SELECT Subject FROM Database WHERE Subject='{subject}' AND Day='{day}' AND Hour={hour}")
        if self.cur.fetchone() is None:
            print("You have enter bad data. It's not in the database")
        else:
            self.cur.execute(f"DELETE FROM Database WHERE Subject='{subject}' AND Day='{day}' AND Hour={hour}")
            self.conn.commit()
            print("You have deleted the meeting")


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
        time.sleep(2)
        x, y = pyautogui.locateCenterOnScreen("button.png")
        time.sleep(0.5)
        pyautogui.click(x, y)
        time.sleep(0.5)
        pyautogui.write(id)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.write(password)
        pyautogui.press('enter')

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
    while True:
        print("1.Create Table")
        print("2.Add Meetings")
        print("3.Delete Meetings")
        print("4.Go to class")
        print("5.Exit")
        print("*"*40)
        answer = input("What do you want to do?(1-5): ")

        if answer.strip() == "1":
            zoomDatabase.createTable()
            print("You have made a new table.")
            staying()
        elif answer.strip() == "2":
            zoomDatabase.addingMeeting()
            print("Meeting added to your database")
            staying()
        elif answer.strip() == "3":
            zoomDatabase.deleteMeeting()
            staying()
        elif answer.strip() == "4":
            day, hour, minute = entry.get_time()
            meetid_password = zoomDatabase.retrieveMeeting(day, hour, minute)
            if meetid_password is None:
                print("This class doesn't exist. Check the data and remember that you can enter until 10 minutes before class.")
            else:
                id, password = meetid_password
                entry.robotic_arm(id, password)
            staying()
        elif answer.strip() == "5":
            print("Until the next one.")
            zoomDatabase.cur.close()
            break
        else:
            print("Invalid. Try again")
            print("*"*40)

if __name__ == '__main__':
    ADMIN_PASSWORD = "CONTRASEÑA."
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
               
