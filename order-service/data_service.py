import secrets
from datetime import datetime, timezone


def _new_object_id() -> str:
    return secrets.token_hex(12)


class OrderDataService:
    def __init__(self):
        self.orders = []
        self.current_id = 1

    def get_all(self):
        return self.orders

    def get_by_id(self, order_id: int):
        for order in self.orders:
            if order.get("order_id") == order_id:
                return order
        return None

    def create(self, order_data: dict):
        oid = self.current_id
        self.current_id += 1

        items_out = []
        for it in order_data.get("items", []):
            line = dict(it)
            line["_id"] = _new_object_id()
            items_out.append(line)

        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

        doc = {
            "order_id": oid,
            "_id": _new_object_id(),
            "customerId": order_data["customerId"],
            "name": order_data["name"],
            "phone": order_data["phone"],
            "menuId": order_data["menuId"],
            "items": items_out,
            "totalPrice": order_data["totalPrice"],
            "status": order_data.get("status", "pending"),
            "createdAt": now,
            "__v": 0,
        }
        self.orders.append(doc)
        return doc

    def update(self, order_id: int, update_data: dict):
        for i, order in enumerate(self.orders):
            if order.get("order_id") == order_id:
                if "items" in update_data and update_data["items"] is not None:
                    items_out = []
                    for it in update_data["items"]:
                        line = dict(it)
                        if "_id" not in line:
                            line["_id"] = _new_object_id()
                        items_out.append(line)
                    update_data = {**update_data, "items": items_out}
                self.orders[i].update(update_data)
                return self.orders[i]
        return None

    def delete(self, order_id: int):
        for i, order in enumerate(self.orders):
            if order.get("order_id") == order_id:
                del self.orders[i]
                return True
        return False
