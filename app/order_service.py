from typing import List, Optional
from venv import logger
from fastapi.responses import JSONResponse
from app.generic_helper import extracting_session_id
from app.generic_helper import get_str_from_food_dict


class OrderService:
    in_progress_order: dict = {}

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

    def complete_order(self):
        if self.session_id not in OrderService.in_progress_order:
            fulfillment_text = "I am having trouble finding your order. Sorry! Can you place a new order"
            logger.warning(fulfillment_text)

        else:
            order = OrderService.in_progress_order[self.session_id]
            order_id = self.db.save_order(order)

            if order_id == -1:
                fulfillment_text = (
                    "Sorry, I couldn't process your order due to backend error."
                    "Please place a new order again"
                )
                logger.warning(fulfillment_text)

            else:
                order_total = self.db.get_order_total(order_id)

                fulfillment_text = (
                    "Awesome. We have place your order. "
                    f"Here is your order id:{int(order_id)}. "
                    f"Your order total is Rs.{order_total}"
                )

                logger.info(fulfillment_text)

                del OrderService.in_progress_order[self.session_id]
                self.db.insert_order_tracking(order_id, "in progress")

        return JSONResponse(content={"fulfillmentText": fulfillment_text})

    def remove_order(self):
        pass

    def add_order(self):
        if (
            len(self.food_items) != len(self.quantities)
            or len(self.quantities) == 0
            or len(self.food_items) == 0
        ):
            fulfillment_text = "Sorry I didn't understand. Can you please specify food items and quantities."
            logger.warning(fulfillment_text)
        else:
            food_dict = dict(zip(self.food_items, self.quantities))

            if self.session_id in OrderService.in_progress_order:
                current_food_dict = OrderService.in_progress_order[self.session_id]
                current_food_dict.update(food_dict)
            else:
                OrderService.in_progress_order[self.session_id] = food_dict

            order_str = get_str_from_food_dict(
                OrderService.in_progress_order[self.session_id]
            )
            fulfillment_text = (
                f"So far you have: {order_str}. Do you need anything else?"
            )

            logger.info(fulfillment_text)

        return JSONResponse(content={"fulfillmentText": fulfillment_text})

    def track_order(self):
        order_status = self.db.get_order_status(self.order_id)

        if order_status:
            fulfillment_text = (
                f"The order status for order id: {self.order_id} is: {order_status}"
            )
        else:
            fulfillment_text = f"No order found with order id: {self.order_id}"

        logger.info(fulfillment_text)
        return JSONResponse(content={"fulfillmentText": fulfillment_text})
