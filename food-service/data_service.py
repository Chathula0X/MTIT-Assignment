class FoodDataService:
    def __init__(self):
        self.foods = []
        self.current_id = 1

    def get_all(self):
        return self.foods

    def get_by_id(self, food_id: int):
        return next((f for f in self.foods if f["id"] == food_id), None)

    def create(self, data: dict):
        data["id"] = self.current_id
        self.current_id += 1
        self.foods.append(data)
        return data

    def update(self, food_id: int, update_data: dict):
        for i, food in enumerate(self.foods):
            if food["id"] == food_id:
                self.foods[i].update(update_data)
                return self.foods[i]
        return None

    def delete(self, food_id: int):
        for i, food in enumerate(self.foods):
            if food["id"] == food_id:
                del self.foods[i]
                return True
        return False