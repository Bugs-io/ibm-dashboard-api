class UserModel(db.Entity):
    def __init__(self, user_id, name):
        self.user_id = user_id
        self.name = name

class UserRepository:
    def __init__(self):
        self.db = db

    def get(self, user_id):
        user = self.db.UserModel.get(user_id=user_id)
        return User(user.user_id, user.name)

    def save(self, user: User):

        self.db.UserModel(user.user_id, user.name)
