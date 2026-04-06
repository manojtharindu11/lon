from typing import List, Optional
from fastapi.responses import JSONResponse
from app.generic_helper import extracting_session_id
from app.generic_helper import get_str_from_food_dict


class OrderService:
    def __init__(self, db, parameters: dict, output_context: dict):
        self.db = db

        order_id = parameters.get("order_id")
        self.order_id: Optional[int] = int(order_id) if order_id is not None else None

        food_items = parameters.get("food-item")
        self.food_items: Optional[List[str]] = food_items if food_items else None

        quantities = parameters.get("number")
        self.quantities: Optional[List[int]] = quantities if quantities else None

        session_string = output_context[0].get("name")
        self.session_id: str = (
            extracting_session_id(session_string) if session_string else None
        )

        self.in_progress_order: dict = {}

    def complete_order(self):
        pass

    def remove_order(self):
        pass

    def add_order(self):
        if (
            len(self.food_items)
            != len(self.quantities) | len(self.quantities)
            == 0 | len(self.food_items)
            == 0
        ):
            fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities."
        else:
            food_dict = dict(zip(self.food_items, self.quantities))

            if self.session_id in self.in_progress_order:
                current_food_dict = self.in_progress_order[self.session_id]
                self.in_progress_order[self.session_id] = current_food_dict.update(
                    self.food_dict
                )
            else:
                self.in_progress_order[self.session_id] = food_dict

            order_str = get_str_from_food_dict(self.in_progress_order[self.session_id])
            fulfillment_text = (
                f"So far you have: {order_str}. Do you need anything else?"
            )

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
