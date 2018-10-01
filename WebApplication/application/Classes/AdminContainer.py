from application.Classes.UserContainer import User

class Admin(User):

    def __init__(self, row):
        super().__init__(row)