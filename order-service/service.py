from data_service import OrderDataService

class OrderService:
    def __init__(self):
        self.data_service = OrderDataService()

    def get_all(self):
        return self.data_service.get_all()

    def get_by_id(self, order_id: int):
        return self.data_service.get_by_id(order_id)

    def create(self, order):
        order_dict = order.dict()
        order_dict["status"] = "pending"
        return self.data_service.create(order_dict)

    def update(self, order_id: int, order):
        update_data = order.dict(exclude_unset=True)
        return self.data_service.update(order_id, update_data)

    def delete(self, order_id: int):
        return self.data_service.delete(order_id)