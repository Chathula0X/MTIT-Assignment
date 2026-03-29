from data_service import FoodDataService

class FoodService:
    def __init__(self):
        self.data_service = FoodDataService()

    def get_all(self):
        return self.data_service.get_all()

    def get_by_id(self, food_id: int):
        return self.data_service.get_by_id(food_id)

    def create(self, food):
        return self.data_service.create(food.dict())

    def update(self, food_id: int, food):
        return self.data_service.update(food_id, food.dict(exclude_unset=True))

    def delete(self, food_id: int):
        return self.data_service.delete(food_id)