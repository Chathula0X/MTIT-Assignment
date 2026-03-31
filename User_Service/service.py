from data_service import UserDataService

class UserService:
    def __init__(self):
        self.data_service = UserDataService()

    def get_all(self):
        return self.data_service.get_all()

    def get_by_id(self, user_id: int):
        return self.data_service.get_by_id(user_id)

    def register(self, user):
        existing = self.data_service.get_by_email(user.email)
        if existing:
            raise Exception("Email already registered")
        return self.data_service.create(user.dict())

    def login(self, email: str, password: str):
        user = self.data_service.get_by_email(email)
        if not user or user["password"] != password:
            return None
        return user

    def update(self, user_id: int, user):
        return self.data_service.update(user_id, user.dict(exclude_unset=True))

    def delete(self, user_id: int):
        return self.data_service.delete(user_id)