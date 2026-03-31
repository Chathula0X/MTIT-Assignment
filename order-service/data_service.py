
class OrderDataService:
    def __init__(self):
        self.orders = []
        self.current_id = 1

    def get_all(self):
        return self.orders

    def get_by_id(self, order_id: int):
        for order in self.orders:
            if order["id"] == order_id:
                return order
        return None

    def create(self, order_data: dict):
        order_data["id"] = self.current_id
        self.current_id += 1
        self.orders.append(order_data)
        return order_data

    def update(self, order_id: int, update_data: dict):
        for i, order in enumerate(self.orders):
            if order["id"] == order_id:
                self.orders[i].update(update_data)
                return self.orders[i]
        return None

    def delete(self, order_id: int):
        for i, order in enumerate(self.orders):
            if order["id"] == order_id:
                del self.orders[i]
                return True
        return False