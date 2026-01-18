"""
Notes App where User can login and store their notes and mark them as done or not done
"""
from getpass import getpass  # Used for password


class User:
    def __init__(self):
        self.available = False
        self.notes = {'content': '', 'done': False }  # Dict to store notes content and done status
        self.name = {  # Dict stores username password and notes
            'username': '',
            'password': '',
            'notes': []
        }
        self.users = []  # list to store self.notes values

    def new_user(self):  # Func to add new user
        print("New User \n")
        name = input("Enter your username: ").strip()
        password = getpass("Create your password: ").strip()
        print()
        for user in self.users:  # Checks if user already exists
            if name == user['username'] and password == user['password']:
                print("User already exists")
                print()
                self.available = False
                return
        self.name = {'username': name, 'password': password, 'notes': []}  # Sets self.name to new user details
        print("User created successfully")
        self.available = True
        print()
        self.users.append(self.name)  # appends new user to users list
        print(self.users)
        return

    def existing_user(self):  # Func for existing user login
        print("Existing User \n")
        username = input("Enter your username: ").strip()
        password = getpass("Enter your password: ").strip()
        print()
        for i, user in enumerate(self.users):  # Checks if username and password match
            if user['username'] == username and user['password'] == password:
                print("Login Successful")
                print()
                self.name = self.users[i]  # Sets self.name to logged in user
                self.available = True
                return user
        print('Invalid username or password')
        print()
        self.available = False
        return

    def add_notes(self):  # Func to add notes for user
        content = input('Enter note: \n').strip()
        self.notes = {'content': content, 'done': False}  # Sets note content and done status
        if content in self.name['notes']['content']:  # Checks if note already exists
            print('Note already exists')
            print()
            self.available=False
            return
        self.available=True
        self.name['notes'].append(self.notes)   # Appends note to user's notes list
        print('Note added successfully')
        print()
        return

    def delete_notes(self):  # Func to delete notes
        cancel=False
        self.view_notes()
        while True:     # Loop until valid input
            try:      # Input validation for note selection
                n = int(input('select note to delete (0 to cancel):'))
                print()
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if n < 0 or n > len(self.name['notes']):
                print('Please select a valid number from the list.')
                continue
            elif n == 0:        # Cancels delete operation
                cancel=True
                print("Delete cancelled")
                print()
                return
            else:
                break
        for i, note in enumerate(self.name['notes']):  # Deletes selected note
            if n - 1 == i:
                self.name['notes'].pop(i)
                print("Note deleted successfully")
                print()
        return

    def view_notes(self):  # Func to view notes
        for i, note in enumerate(self.name['notes']):  # Displays notes with done status
            print(f'{i + 1}. {note['content']}    {'✅' if note['done'] else ''}')


    def mark_done(self):  # Func to mark notes as done
        self.view_notes()
        while True:  # Loop until valid input
            try:  # Input validation for note selection
                n = int(input('select note to mark as done:'))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if n < 1 or n > len(self.name['notes']):
                print('Please select a valid number from the list.')
                continue
            else:
                break
        for i, note in enumerate(self.name['notes']):  # Marks selected note as done`
            if n - 1 == i:
                if note['done'] == True:
                    print("Note is already marked as done")
                    print()
                else:
                    note['done'] = True
                    print("Note marked as done")
                    print()
        return self.name['notes']


    def mark_undone(self):  # Func to mark notes as not done
        self.view_notes()
        while True:  # Loop until valid input
            try:  # Input validation for note selection
                n = int(input('select note to mark as udone:'))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if n < 1 or n > len(self.name['notes']):
                print('Please select a valid number from the list.')
                continue
            else:
                break
        for i, note in enumerate(self.name['notes']):  # Marks selected note as not done
            if n - 1 == i:
                if note['done'] == False:
                    print("Note is already marked as undone")
                    print()
                else:
                    note['done'] = False
                    print("Note marked as undone")
                    print()
        return self.name['notes']


class NotesApp:  # Main Notes App class
    def __init__(self):  # Initializes User class
        self.user = User()

    def user_menu(self):  # Func to display user menu
        print('Welcome to Notes App')
        while True:  # Loop until user exits
            print('1. New User')
            print('2. Existing User')
            print('3. Exit')
            try:
                choice = int(input('Select an option: '))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if choice < 1 or choice > 3:
                print('Please select a valid option.')
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
                print('Exiting Notes App')
                break
        return

    def notes_menu(self):  # Func to display notes menu
        while True:  # Loop until user exits
            print('1. Add Note')
            print('2. View Notes')
            print('3. Delete Note')
            print('4. Mark Note as Done')
            print('5. Mark Note as Undone')
            print('6. Logout')
            try:
                choice = int(input('Select an option: '))
            except ValueError:
                print("Invalid input. Please enter a number.")
                continue
            if choice < 1 or choice > 6:
                print('Please select a valid option.')
                continue
            elif choice == 1:
                self.user.add_notes()
                if not self.user.available:
                    continue
            elif choice == 2:
                self.user.view_notes()
                inp=getpass('Press Enter to continue...')
                continue
            elif choice == 3:
                self.user.delete_notes()
                continue

            


app = NotesApp()
app.user_menu()
app .notes_menu()