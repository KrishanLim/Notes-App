"""
Notes App where User can login and store their notes and mark them as done or not done
"""
import base64               #Used for password

class User:
    def __init__(self):
        self.done = False
        self.name = {                     #Dict stores username password notes and done or not
            'username': '',
            'password': '',
            'notes': []
        }
        self.users=[]               #list to store self.notes values

    def new_user(self):             #Func to add new user
        print("New User \n")
        self.name['username'] =input("Enter your username: ")
        self.name['password'] =input("Create your password: ")
        self.users.append(self.name)


user=User()
user.new_user()






