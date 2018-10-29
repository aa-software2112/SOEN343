from app.classes.user_container import User


class Admin(User):

    def __init__(self, row):
        super().__init__(row)
