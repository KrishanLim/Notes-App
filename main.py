"""
Notes App where User can login and store their notes and mark them as done or not done
"""
from getpass import getpass               #Used for password

class User:
    def __init__(self):
        self.done = False
        self.notes = {'content': '', 'done': False}   #Dict to store notes content and done status
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
    
    def add_notes(self):          #Func to add notes for user
        self.notes['content']=input("Enter your note: ")
        self.name['notes'].append(self.notes)       #Appends notes to user's notes list
        print("Note added successfully")
        return self.name['notes']                      

    def view_notes(self):       #Func to view notes
        for i,note in enumerate(self.users['notes']):
            print(f'{i+1}. {note['content']}    {'✅' if note['done'] else ''}')
                    
    def mark_done(self):          #Func to mark notes as done
        self.view_notes()   
        while True:                #Loop until valid input
            try:                 #Input validation for note selection
                        n=int(input('select note to mark as done:'))
            except ValueError:
                        print("Invalid input. Please enter a number.")
                        continue
            if n<1 or n>len(self.users['notes']):
                 print('Please select a valid number')
                 continue
            else:
                break
        for i,note in enumerate(self.users['notes']):
          if i==n-1:
            note['done']=True
            print("Note marked as done")
            break   
            
                 


        
         
        
    


user=User()
user.new_user()
print(user.users)






