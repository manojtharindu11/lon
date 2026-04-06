from typing import List, Optional
from fastapi.responses import JSONResponse


class OrderService:
    def __init__(self, db, parameters: dict):
        self.db = db

        order_id = parameters.get("order_id")
        self.order_id: Optional[int] = int(order_id) if order_id is not None else None

        food_items = parameters.get("food-item")
        self.food_items: Optional[List[str]] = food_items if food_items else None

        quantities = parameters.get("number")
        self.quantities: Optional[List[int]] = quantities if quantities else None

    def complete_order(self):
        pass

    def remove_order(self):
        pass

    def add_order(self):
        if len(self.food_items) != len(self.quantities):
            fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities."
        else:
            fulfillment_text = f"Received {self.food_items} and {self.quantities}"

        return JSONResponse(content={"fulfillmentText": fulfillment_text})

    def track_order(self):
        order_status = self.db.get_order_status(self.order_id)

        if order_status:
            fulfillment_text = (
                f"The order status for order id: {self.order_id} is: {order_status}"
            )
        else:
            fulfillment_text = f"No order found with order id: {self.order_id}"

        return JSONResponse(content={"fulfillmentText": fulfillment_text})
