from werkzeug.security import check_password_hash
# I need to define a User Class; it is doing user session management class which needs to some methods 

class User:

    # creating constructor of the class
    def __init__(self,username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def is_authenticated(self):
        return True    # only authenticated users allowed

    def is_active(self):
        return True # only active users allowed

    def is_anonymous(self):
        return False   # should be false because I'm not gonna create some anonymous user with this object

    def get_id(self):
        return self.username  # return unique identifier for eveery user

    def checkPassword(self, passowrd_input):
        return check_password_hash(self.password, passowrd_input)
        # checking inputed string password and our hashed passowrd from the database

