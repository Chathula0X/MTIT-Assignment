class UserDataService:
    def __init__(self):
        self.users = []
        self.current_id = 1

    def get_all(self):
        return self.users

    def get_by_id(self, user_id: int):
        return next((u for u in self.users if u["id"] == user_id), None)

    def get_by_email(self, email: str):
        return next((u for u in self.users if u["email"] == email), None)

    def create(self, user_data: dict):
        user_data["id"] = self.current_id
        self.current_id += 1
        self.users.append(user_data)
        return user_data

    def update(self, user_id: int, update_data: dict):
        for i, user in enumerate(self.users):
            if user["id"] == user_id:
                self.users[i].update(update_data)
                return self.users[i]
        return None

    def delete(self, user_id: int):
        for i, user in enumerate(self.users):
            if user["id"] == user_id:
                del self.users[i]
                return True
        return False