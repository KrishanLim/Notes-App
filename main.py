"""
Notes App where User can login and store their notes and mark them as done or not done
"""

class User:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.done = False
        self.notes = [{
            'username': username,
            'password': password,
            'notes': [
                {'Content':'' , 'Done': 'False'}
            ]
        }]

    def new_user(self):
        print("New User")

            username = input("Enter your username: ")
            password = input("Enter your password: ")
