"""
Notes App where User can login and store their notes and mark them as done or not done
"""

import sqlite3
import bcrypt


class Database:  # Creates Database To store values
    def __init__(self, database="data.db"):
        self.database = database
        self.con = sqlite3.connect(self.database)  # SQL Connect
        self.cur = self.con.cursor()  # Cursor
        self.id = 0
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS login_info(id INTEGER PRIMARY KEY, username TEXT COLLATE NOCASE, password)"""
        )  # Creates Table for user info If it does not exist
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Notes(id INTEGER PRIMARY KEY, user_id, Content , Done)"
        )  # Creates Table for User Notes

    def add_user(self, data):  # Function to add new users
        self.cur.execute(  # Checks if username already exists
            "SELECT EXISTS(SELECT 1 FROM login_info WHERE username=?)",
            (data["username"],),
        )
        if self.cur.fetchone()[0]:
            print("User already exists")
            return True
        else:
            self.cur.execute(  # Adds Username and password to database
                "INSERT INTO login_info (username, password) VALUES (?,?)",
                (
                    data["username"],
                    data["password"],
                ),
            )
            self.con.commit()
        self.cur.execute(
            "SELECT id FROM login_info WHERE username=?", (data["username"],)
        )
        self.id = self.cur.fetchone()[0]
        return False

    def view_users(self):  # View users
        self.cur.execute("SELECT COUNT(*) FROM login_info")
        count = self.cur.fetchone()[0]
        if count < 1:
            print("No user exists")
            return
        self.cur.execute("SELECT username FROM login_info")
        users = self.cur.fetchall()
        for i, user in enumerate(users, start=1):
            print(f"{i}. {user[0]}")
        return count

    def delete_user(
        self, num
    ):  # Func to delete User from Table login_info from database
        self.cur.execute("SELECT username FROM login_info")
        users = self.cur.fetchall()
        for i, user in enumerate(users, start=1):  # Lopps over the usernames
            if num == i:
                self.cur.execute(
                    "DELETE FROM Notes WHERE user_id=(SELECT id FROM login_info WHERE username=?)",
                    (user[0],),
                )  # deletes notes before username
                self.cur.execute(
                    "DELETE FROM login_info WHERE username=?", (user[0],)
                )  # Deletes Userdata
                print(f"User {user[0]} Deleted")
                break
        self.con.commit()
        return

    def user_exists(self, data):  # Checks Username/password
        self.cur.execute(  # Checks if username already exists
            "SELECT EXISTS(SELECT 1 FROM login_info WHERE username=? )",
            (data["username"],),
        )
        if self.cur.fetchone():  # if user exists check password
            self.cur.execute(
                "SELECT password FROM login_info WHERE username = ?",
                (data["username"],),
            )
            password = self.cur.fetchone()[0]
            check = bcrypt.checkpw(data["password"].encode("utf-8"), password)
            if check:
                self.cur.execute(
                    "SELECT username, id FROM login_info WHERE username=?",
                    (data["username"],),
                )
                username, self.id = self.cur.fetchone()
                print("Welcome ", username)
                return True  # Return True if password matched

        print("Username or Password Error")
        return False  # Username does not match

    def add_notes(self, note):  # Func to add notes to database
        self.cur.execute(  # Checks if note already exists
            "SELECT EXISTS(SELECT 1 FROM Notes WHERE Content=? AND user_id=?)",
            (note["content"], self.id),
        )
        if not self.cur.fetchone()[0]:
            self.cur.execute(  # Adds user id, Content and Done status to the table
                "INSERT INTO Notes(user_id, Content, Done) VALUES(?,?,?)",
                (
                    self.id,
                    note["content"],
                    note["done"],
                ),
            )
            self.con.commit()  # Commits
            print("Note Added Sucessfully")
            return False
        else:
            print("Note already exists")  # Note already Exists
        return True

    def view_notes(self):
        self.cur.execute("SELECT COUNT(*) FROM Notes WHERE user_id=?", (self.id,))
        count = self.cur.fetchone()[0]  # No of rows in Notes database
        if count > 0:
            self.cur.execute(
                "SELECT Content, Done FROM Notes WHERE user_id=?", (self.id,)
            )
            notes = self.cur.fetchall()
            for i, note in enumerate(notes, start=1):
                print(
                    f'{i}. {note[0]}      {"✅" if note[1] else ""}'
                )  # Displays Done or not done
        else:
            print("No notes Available")
        print()
        return count

    def delete_note(
        self, data
    ):  # Func to delete Content From Table Notes from database
        self.cur.execute("SELECT Content FROM Notes WHERE user_id=?", (self.id,))
        notes = self.cur.fetchall()
        for i, note in enumerate(notes, start=1):
            if i == data:
                self.cur.execute(
                    "DELETE FROM Notes WHERE Content= ? AND user_id=?",
                    (note[0], self.id),
                )
                print("Note Deleted successfully")
        self.con.commit()
        return

    def done(self, data, done=True):  # Func to update done status from Table Notes
        self.cur.execute("SELECT Content, Done FROM Notes WHERE user_id=?", (self.id,))
        notes = self.cur.fetchall()
        for i, note in enumerate(notes, start=1):
            if data == i:
                if note[1]:
                    print("Note Already Marked Done")
                    return
                self.cur.execute(
                    "UPDATE Notes SET Done=? WHERE Content=?",
                    (
                        done,
                        note[0],
                    ),
                )
                print("Marked Done sucessfully")
        self.con.commit()
        return

    def undone(self, data, done=False):  # Func to update done status from Table Notes
        self.cur.execute("SELECT Content, Done FROM Notes WHERE user_id=?", (self.id,))
        notes = self.cur.fetchall()
        for i, note in enumerate(notes, start=1):
            if data == i:
                if not note[1]:
                    print("Note Already Unmarked Done")
                    return
                self.cur.execute(
                    "UPDATE Notes SET Done=? WHERE Content=?",
                    (
                        done,
                        note[0],
                    ),
                )
                print("Note Unmarked Done sucessfully")
        self.con.commit()
        return


class User:
    def __init__(self):  # Initializes variables
        self.db = Database()  # Connects to Database Class
        self.available = False
        self.id = 0

    def user_input(self, high):
        while True:
            try:
                ans = int(input("Select an Option \n press 0 to Exit: "))
                print()
            except ValueError:
                print()
                print("Invalid Input. Enter a Number")
                print()
            if ans < 0 or ans > high:
                print("Enter a valid option")
                print()
            elif ans == 0:
                print("Exit.")
                print()
                break
            else:
                break
        return ans

    def new_user(self):  # Func to add new user
        print()
        print("--New User-- \n")
        while True:
            username = input("Enter your username: ").strip()
            if len(username) == 0:
                print("Username cannot be empty")
                continue
            break
        while True:  # User authentication for strong password
            print()
            password = input(
                "Create a strong password: "
            ).strip()  # User enters password
            contains_digit = any(
                char.isdigit for char in password
            )  # checks if the password contains number
            if len(password) < 8:  # checks the length of the password
                print("Password must be at least 8 characters")
                continue
            elif not contains_digit:
                print("Passwrod must have at least one digit")
                continue
            elif password.isalnum():
                print("Password must contain at least one symbol")
                continue
            elif not any(char.isupper() for char in password):
                print("password must have at least one Uppercase character")
                continue
            elif " " in password:
                print("password must not contain any spaces")
                continue
            break
        password_bytes = password.encode("utf-8")  # Changes into bytes
        hashed_password = bcrypt.hashpw(
            password_bytes, bcrypt.gensalt()
        )  # Hash password using gensalt
        print()
        name = {
            "username": username,
            "password": hashed_password,
        }
        self.available = self.db.add_user(
            name
        )  # Returns True if user exists False if Not
        return self.available

    def existing_user(self):  # Func for existing user login
        print("--Existing User-- \n")
        username = input("Enter your username: ").strip()
        password = input("Enter your password: ").strip()
        name = {
            "username": username,
            "password": password,
        }
        print()
        exists = self.db.user_exists(name)
        print()
        return exists

    def view_users(self):
        self.db.view_users()
        return

    def delete_user(self):
        print("--Delete User-- \n")
        count = self.db.view_users()
        if count < 0:
            print("No user Available")
            return
        ans = self.user_input(count)
        if ans == 0:
            return
        self.db.delete_user(ans)
        return

    def add_notes(self):  # Func to add notes for user
        print("--Add Note-- \n")
        content = input("Enter note: \n").strip()
        note = {
            "content": content,
            "done": False,
        }  # Sets note content and done status
        exists = self.db.add_notes(note)
        print()
        return exists

    def view_notes(self):
        print("--View Notes-- \n")
        self.db.view_notes()

    def delete_notes(self):  # Func to delete notes
        print("--Delete Note-- \n")
        high = self.db.view_notes()
        if high < 1:  # Returns if no notes available
            return
        print()
        ans = self.user_input(high)
        if ans == 0:
            return
        self.db.delete_note(ans)  # deletes the selected note
        return

    def mark_done(self):  # Func to mark notes as done
        print("--Mark Note as Done-- \n")
        count = self.db.view_notes()
        if count < 1:
            return
        print()
        ans = self.user_input(count)
        self.db.done(ans)
        return

    def mark_undone(self):  # Func to mark notes as not done
        print("--Unmark Note as Done-- \n")
        count = self.db.view_notes()
        if count < 1:
            return
        ans = self.user_input(count)
        self.db.undone(ans)
        return


class NotesApp:  # Main Notes App class
    def __init__(self):  # Initializes User class
        self.Exit = False
        self.user = User()

    def user_input(self, low, high):
        while True:
            try:
                ans = int(input(f"Enter Number From 1 to {high}"))
            except ValueError:
                print("Enter a number")
            if ans < low or ans > high:
                print("Select a valid option")
                continue
            else:
                break
        return ans

    def user_menu(self):  # Func to display user menu
        print()
        print("*" * 30)
        print("Welcome to Notes App")
        print("*" * 30)
        print()
        while True:  # Loop until user exits
            print("1. New User")
            print("2. Existing User")
            print("3. Delete User")
            print("4. Exit")
            print()
            ans = self.user_input(1, 4)
            if ans == 4:
                self.Exit = True
                break
            elif ans == 1:
                self.user.new_user()
                if self.user.available:
                    continue
                break
            elif ans == 2:
                exist = self.user.existing_user()
                if exist:
                    break
                continue
            elif ans == 3:
                self.user.delete_user()
                continue

    def notes_menu(self):  # Func to display notes menu
        while True:  # Loop until user exits
            print("1. Add Note")
            print("2. View Notes")
            print("3. Delete Note")
            print("4. Mark Note as Done")
            print("5. Mark Note as Undone")
            print("6. Logout")
            print()
            ans = self.user_input(1, 6)
            if ans == 6:
                print("Logging out...")
                return
            elif ans == 1:
                self.user.add_notes()
                continue
            elif ans == 2:
                self.user.view_notes()
                print()
                inp = input("Press Enter to continue...")
                print()
                continue
            elif ans == 3:
                self.user.delete_notes()
                continue
            elif ans == 4:
                self.user.mark_done()
                continue
            elif ans == 5:
                self.user.mark_undone()
                continue


class RunApp:
    def run(self):
        app = NotesApp()
        while True:
            app.user_menu()
            if app.Exit:
                return
            app.notes_menu()


if __name__ == "__main__":
    run = RunApp()
    run.run()
