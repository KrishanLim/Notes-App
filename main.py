"""
Notes App where User can login and store their notes and mark them as done or not done
"""

import json
from getpass import getpass  # Used for password
import os
import sqlite3


class Database:  # Creates Database To store values
    def __init__(self, database="data.db"):
        self.database = database
        self.con = sqlite3.connect(self.database)
        self.cur = self.con.cursor()
        self.cur.execute(
            """CREATE TABLE IF NOT EXISTS login_info(id INTEGER PRIMARY KEY, username, password)"""
        )  # Creates Database if it does not exist
        self.cur.execute("CREATE TABLE IF NOT EXISTS Notes(id INTEGER PRIMARY KEY, user_id, Content , Done)")

    def add_user(self, data):           #Function to add new users
        self.cur.execute('SELECT EXISTS(SELECT 1 FROM login_info WHERE username=?)',(data['username']))
        if self.cur.fetchone[0]:
            print('User already exists')
        else:
            self.cur.execute("INSERT INTO login_info(username, password) VALUES=(?,?)",(data['username'],data['password']))
            self.con.commit()
        return
    
class User:
    def __init__(self, file="data.json"):  # Initializes variables
        self.file = file
        self.available = False
        self.notes = {
            "content": "",
            "done": False,
        }  # Dict to store notes content and done status
        self.name = {  # Dict stores username password and notes
            "username": "",
            "password": "",
            "notes": [],
        }
        self.users = []
        if os.path.exists(self.file):  # Loads users from data.json if it exists
            with open(self.file, "r") as f:
                if os.path.getsize(self.file) == 0:
                    self.users = []
                else:
                    self.users = json.load(f)

    def new_user(self):  # Func to add new user
        print("--New User-- \n")
        name = input("Enter your username: ").strip()
        password = getpass("Create your password: ").strip()
        print()
        for user in self.users:
            if name == user["username"]:
                print("username already exists")
                print()
                self.available = False
                return
        self.name = {
            "username": name,
            "password": password,
            "notes": [],
        }  # Sets self.name to new user details
        self.users.append(self.name)
        with open(self.file, "w") as f:
            json.dump(self.users, f, indent=2)  # Saves new user to data.json
        print("User created successfully")
        self.available = True
        print()
        print(self.users)
        return

    def existing_user(self):  # Func for existing user login
        print("--Existing User-- \n")
        username = input("Enter your username: ").strip()
        password = getpass("Enter your password: ").strip()
        print()
        for user in self.users:
            if username == user["username"] and password == user["password"]:
                print("login successful")
                self.name = user
                self.available = True
                print()
                return
        print("Invalid username or password")
        print()
        self.available = False
        return

    def view_users(self):
        if len(self.users) == 0:
            print("No users available")
            return 0
        for i, user in enumerate(self.users):
            print(f"{i+1}. {user['username']}")
        return

    def delete_user(self):
        print("--Delete User-- \n")
        if self.view_users() == 0:
            self.view_users()
            return
        while True:  # Loop until valid input
            try:
                n = int(input("Select user to delete (0 to cancel): "))
                print()
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if n < 0 or n > len(self.users):
                print("Please select a valid number from the list.")
                continue
            elif n == 0:
                print("--Delete cancelled-- \n")
                return
            elif n in range(1, len(self.users) + 1):
                for i, user in enumerate(self.users):
                    if n - 1 == i:
                        self.users.pop(i)
                        with open(self.file, "w") as f:
                            json.dump(self.users, f, indent=2)
                            return

    def add_notes(self):  # Func to add notes for user
        print("--Add Note-- \n")
        content = input("Enter note: \n").strip()
        print()
        self.notes = {
            "content": content,
            "done": False,
        }  # Sets note content and done status
        for note in self.name["notes"]:  # Checks if note already exists
            if content == note["content"]:
                print("Note already exists")
                self.available = False
                return
        self.available = True
        self.name["notes"].append(self.notes)  # Appends note to user's notes list
        print("Note added successfully")
        print()
        return

    def delete_notes(self):  # Func to delete notes
        print("--Delete Note-- \n")
        cancel = False
        self.view_notes()
        print()
        while True:  # Loop until valid input
            try:  # Input validation for note selection
                n = int(input("select note to delete (0 to cancel):"))
                print()
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if n < 0 or n > len(self.name["notes"]):
                print("Please select a valid number from the list.")
                continue
            elif n == 0:  # Cancels delete operation
                cancel = True
                print("Delete cancelled")
                print()
                return
            else:
                break
        for i, note in enumerate(self.name["notes"]):  # Deletes selected note
            if n - 1 == i:
                self.name["notes"].pop(i)
                print("Note deleted successfully")
                print()
        return

    def view_notes(self):  # Func to view notes
        for i, note in enumerate(self.name["notes"]):  # Displays notes with done status
            print(f"{i + 1}. {note['content']}    {'✅' if note['done'] else ''}")

    def mark_done(self):  # Func to mark notes as done
        print("--Mark Note as Done-- \n")
        self.view_notes()
        print()
        while True:  # Loop until valid input
            try:  # Input validation for note selection
                n = int(input("select note to mark as done:"))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if n < 1 or n > len(self.name["notes"]):
                print("Please select a valid number from the list.")
                continue
            else:
                break
        print()
        for i, note in enumerate(self.name["notes"]):  # Marks selected note as done`
            if n - 1 == i:
                if note["done"] == True:
                    print("Note is already marked as Done")
                    print()
                else:
                    note["done"] = True
                    print("Note marked as done")
                    print()
        return self.name["notes"]

    def mark_undone(self):  # Func to mark notes as not done
        print("--Unmark Note as Done-- \n")
        self.view_notes()
        print()
        while True:  # Loop until valid input
            try:  # Input validation for note selection
                n = int(input("select note to mark as udone:"))
                print()
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if n < 1 or n > len(self.name["notes"]):
                print("Please select a valid number from the list.")
                continue
            else:
                break
        for i, note in enumerate(self.name["notes"]):  # Marks selected note as not done
            if n - 1 == i:
                if note["done"] == False:
                    print("Note is already marked as undone")
                    print()
                else:
                    note["done"] = False
                    print("Note marked as undone")
                    print()
        return self.name["notes"]


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
