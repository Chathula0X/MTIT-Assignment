from data_service import PaymentDataService

class PaymentService:
    def __init__(self):
        self.data_service = PaymentDataService()

    def get_all(self):
        return self.data_service.get_all()

    def get_by_id(self, payment_id: int):
        return self.data_service.get_by_id(payment_id)

    def create(self, payment):
        data = payment.dict()
        data["status"] = "pending"
        return self.data_service.create(data)

    def update(self, payment_id: int, payment):
        return self.data_service.update(payment_id, payment.dict(exclude_unset=True))

    def delete(self, payment_id: int):
        return self.data_service.delete(payment_id)