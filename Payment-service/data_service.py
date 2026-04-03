class PaymentDataService:
    def __init__(self):
        self.payments = []
        self.current_id = 1

    def get_all(self):
        return self.payments

    def get_by_id(self, payment_id: int):
        return next((p for p in self.payments if p["id"] == payment_id), None)

    def create(self, data: dict):
        data["id"] = self.current_id
        self.current_id += 1
        self.payments.append(data)
        return data

    def update(self, payment_id: int, update_data: dict):
        for i, payment in enumerate(self.payments):
            if payment["id"] == payment_id:
                self.payments[i].update(update_data)
                return self.payments[i]
        return None