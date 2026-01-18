"""
Notes App where User can login and store their notes and mark them as done or not done
"""
from getpass import getpass               #Used for password

class User:
    def __init__(self):
        self.done = False
        self.name = {                     #Dict stores username password and notes
            'username': '',
            'password': '',
            'notes': []
        }
        self.users=[]               #list to store self.notes values

    def new_user(self):             #Func to add new user
        print("New User \n")
        self.name['username'] =input("Enter your username: ")
        self.name['password'] =getpass("Create your password: ")
        for user in self.users:                    #Checks if user already exists
            if self.name==user:                      
                print("User already exists")
                self.done=True
                return 
        self.users.append(self.name)    #appends new user to users list
        return self.users
    
    def existing_user(self):              #Func for existing user login
        print("Existing User \n")
        username =input("Enter your username: ")
        password =getpass("Enter your password: ")
        for user in self.users:
            if user['username']==username and user['password']==password:
                print("Login Successful")
                return user
        print('Invalid username or password')

        
         
        
    


user=User()
user.new_user()
print(user.users)






