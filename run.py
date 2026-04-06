from fastapi import FastAPI
from fastapi import Request
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from app.db_connect import DbConnect
from app.order_service import OrderService

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

    order_service = OrderService(mysql_connect, parameters)

    intent_handler_dict = {
        "track.order - context: ongoing-tracking": order_service.track_order,
        "order.add - context: ongoing-order": order_service.add_order,
        "order.remove - context: ongoing-order": order_service.remove_order,
        "order.complete - context: ongoing-order": order_service.complete_order,
    }
    return intent_handler_dict[intent]()
