from data import user_db


class DiscountCodeService:
    def __init__(self):
        self.DB = user_db.UserDB()

    def get_user(self, user_id):
        return self.DB.users.get(user_id)
