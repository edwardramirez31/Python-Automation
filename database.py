import sqlite3, time, pyautogui

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
        hour = int(input("Enter the class hour: ").strip().title())
        meeting = input("Enter the Zoom ID-Meeting: ").strip().title()
        password = input("Enter the meeting password: ").strip().title()
        self.cur.execute('INSERT INTO Database (Subject, Day, Hour, IDMeeting, Password) VALUES (?, ?, ?, ?, ?)', (subject, day, hour, meeting, password))
        self.conn.commit()

    def retrieveMeeting(self, day, hour):
        self.cur.execute("SELECT IDMeeting, Password FROM Database WHERE Day='{}' AND Hour={} OR Hour={}+1".format(day, hour, hour,))
        return self.cur.fetchone()

    def deleteMeeting(self, day, hour):
        self.cur.execute('DELETE FROM Database WHERE Day={} AND Hour={}'.format(day, hour,))

class EntryZoom:
    def __init__(self):
        pass

    def get_time(self):
        self.current_time = time.ctime().split()
        self.day = self.current_time[0]
        self.hour = self.current_time[3].split(":")[0]
        return self.day, int(self.hour)



def main():
    zoomDatabase = MeetingDatabase()
    zoomDatabase.createTable()
    zoomDatabase.addingMeeting()
    entry = EntryZoom()
    day, hour = entry.get_time()
    print(day)
    id, password = zoomDatabase.retrieveMeeting(day, hour)
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
    zoomDatabase.cur.close()



if __name__ == '__main__':
    main()
