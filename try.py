class User:
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.notes = 'notes'
        self.list=[{
            'username':username,
            'password':password,
            'notes':self.notes
        }]

user=User('username','password',)
print(user.list)