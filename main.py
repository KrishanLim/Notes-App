"""
Notes App where User can login and store their notes and mark them as done or not done
"""
import base64               #Used for password

class User:
    def __init__(self):
        self.username = ''
        self.password = ''
        self.done = False
        self.notes = [{                     #Dict stores username password notes and done or not
            'username': self.username,
            'password': self.password,
            'notes': [
                {'Content':'' , 'Done': 'False'}
            ]
        }]

    def new_user(self):
        print("New User \n")
        self.username = input("Enter your username: ")
        self.password = input("Enter your password: ")




