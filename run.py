from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from app.db_connect import DbConnect

load_dotenv()
mysql_connect = None


async def lifespan(app: FastAPI):
    global mysql_connect
    mysql_connect = DbConnect()
    yield
    mysql_connect.disconnect()


app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Hello World!"}


@app.post("/")
async def handle_request(request: Request):
    payload = await request.json()
    intent = payload["queryResult"]["intent"]["displayName"]
    parameters = payload["queryResult"]["parameters"]
    output_context = payload["queryResult"]["outputContexts"]

    if intent == "track.order - context: ongoing-tracking":
        return track_order(parameters)


def track_order(parameters: dict):
    order_id = parameters["order_id"]
    order_status = mysql_connect.get_order_status(order_id)

    if order_status:
        fulfillment_text = (
            f"The order status for order id: {order_id} is: {order_status}"
        )
    else:
        fulfillment_text = f"No order found with order id: {order_id}"

    return JSONResponse(content={"fulfillmentText": fulfillment_text})
