"""
Notes App where User can login and store their notes and mark them as done or not done
"""

import json
import bcrypt
import sqlite3


class Database:  # Creates Database To store values
    def __init__(self, database="data.db"):
        self.database = database
        self.con = sqlite3.connect(self.database)  # SQL Connect
        self.cur = self.con.cursor()  # Cursor
        self.id = 0
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS login_info(id INTEGER PRIMARY KEY, username, password)"""
        )  # Creates Table for user info If it does not exist
        self.cur.execute(
            "CREATE TABLE IF NOT EXISTS Notes(id INTEGER PRIMARY KEY, user_id, Content , Done)"
        )  # Creates Table for User Notes

    def add_user(self, data):  # Function to add new users
        self.cur.execute(  # Checks if username already exists
            "SELECT EXISTS(SELECT 1 FROM login_info WHERE username=?)",
            (data["username"]),
        )
        if self.cur.fetchone[0]:
            print("User already exists")
            return True
        else:
            self.cur.execute(  # Adds Username and password to database
                "INSERT INTO login_info(username, password) VALUES=(?,?)",
                (data["username"], data["password"]),
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
        for i, user in enumerate(users):
            print(f"{i}. {user}")
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
            "SELECT EXISTS(SELECT 1 FROM login_info WHERE username=? and)",
            (data["username"],),
        )
        if self.cur.fetchone[0]:  # if user exists check password
            self.cur.execute(
                "SELECT password FROM login_info WHERE username = ", (data["username"],)
            )
            password = self.cur.fetchone()
            check = bcrypt.checkpw(
                password.encrypt("utf-8"), data["password"].encrypt("utf-8")
            )
            if check:
                self.cur.execute(
                    "SELECT id FROM login_info WHERE username=?", (data["username"],)
                )
                self.id = self.cur.fetchone()[0]
                print("Welcome ", data["username"])
                return True  # Return True if password matched
        print("Username or Password Error")
        return False  # Username does not match

    def add_notes(self, note):  # Func to add notes to database
        self.cur.execute(  # Checks if note already exists
            "SELECT EXISTS(SELECT 1 FROM Notes if Content=?)", (note["content"],)
        )
        if self.cur.fetchone()[0]:
            self.cur.execute(  # Adds user id, Content and Done status to the table
                "INSERT INTO Notes(user_id, Content, Done) WHERE VALUES (?,?,?)",
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
                self.cur.execute("DELETE FROM Notes WHERE Content=?", (note[0],))
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
                    "UPDATE Done=? FROM Notes WHERE Content=?",
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
                    "UPDATE Done=? FROM Notes WHERE Content=?",
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
            if ans < 0 and ans > high:
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
        print("--New User-- \n")
        username = input("Enter your username: ").strip().upper()
        password = input("Create your password: ").strip()  # User enters password
        password_bytes = password.encode("utf-8")  # Changes into bytes
        hashed_password = bcrypt.hashpw(
            password_bytes, bcrypt.gensalt()
        )  # Hash password using gensalt
        decoded_password = hashed_password.decode(
            "utf-8"
        )  # Decoded from bytes to string to save in database
        print()
        name = {
            "username": username,
            "password": decoded_password,
        }
        self.available = self.db.add_user(
            name
        )  # Returns True if user exists False if Not
        return self.available

    def existing_user(self):  # Func for existing user login
        print("--Existing User-- \n")
        username = input("Enter your username: ").strip().upper()
        password = ("Enter your password: ").strip()
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
        if self.db.view_users() < 0:
            print("No user Available")
            return
        count = self.db.view_users()
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

    def user_menu(self):  # Func to display user menu
        print()
        print("*" * 30)
        print("Welcome to Notes App")
        print("*" * 30)
        print()
        while True:  # Loop until user exits
            print("1. New User")
            print("2. Existing User")
            print("3. Exit")
            print()
            try:
                choice = int(input("Select an option: "))
                print()
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if choice < 1 or choice > 3:
                print("Please select a valid option.")
                continue
            elif choice == 1:
                self.user.new_user()
                if self.user.available:
                    break
                else:
                    continue
            elif choice == 2:
                self.user.existing_user()
                if not self.user.available:
                    continue
                else:
                    break
            elif choice == 3:
                with open(self.user.file, "w") as f:
                    json.dump(self.user.users, f, indent=2)
                print("Exiting Notes App")
                self.Exit = True
                break
        return

    def notes_menu(self):  # Func to display notes menu
        while True:  # Loop until user exits
            print("1. Add Note")
            print("2. View Notes")
            print("3. Delete Note")
            print("4. Mark Note as Done")
            print("5. Mark Note as Undone")
            print("6. Logout")
            print()
            try:
                choice = int(input("Select an option: "))
                print()
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if choice < 1 or choice > 6:
                print("Please select a valid option.")
                continue
            elif choice == 1:
                self.user.add_notes()
                if not self.user.available:
                    continue
            elif choice == 2:
                print("--View Notes-- \n")
                self.user.view_notes()
                print()
                inp = getpass("Press Enter to continue...")
                print()
                continue
            elif choice == 3:
                self.user.delete_notes()
                continue
            elif choice == 4:
                self.user.mark_done()
                continue
            elif choice == 5:
                self.user.mark_undone()
                continue
            elif choice == 6:
                print("Logging out...")
                print()
                return


class RunApp:
    def run(self):
        app = NotesApp()
        while True:
            app.user_menu()
            if app.Exit:
                return
            app.notes_menu()


# run=RunApp()
# run.run()
