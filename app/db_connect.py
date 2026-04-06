import mysql.connector
import os
from dotenv import load_dotenv
import logging
from typing import Dict


class DbConnect:
    def __init__(self):
        self.host = os.getenv("HOST", "localhost")
        self.user = os.getenv("USER", "root")
        self.password = os.getenv("PASSWORD", "")
        self.database = os.getenv("DATABASE", "ape_kama_db")
        self.connect()

    def connect(self):
        try:
            self.conn = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database,
            )

            if self.conn.is_connected():
                logging.info("Connected to database.")
        except mysql.connector.Error as e:
            logging.info(f"Database connection error: {e}")

    def ensure_connection(self):
        conn = getattr(self, "conn", None)
        if conn is None or not conn.is_connected():
            self.connect()

        if getattr(self, "conn", None) is None or not self.conn.is_connected():
            raise RuntimeError("Database connection not available")

    def disconnect(self):
        if hasattr(self, "conn") and self.conn.is_connected():
            self.conn.close()
            logging.info("Database connection closed")

    def get_order_status(self, order_id: int):
        self.ensure_connection()

        with self.conn.cursor() as cursor:
            cursor.execute(
                "SELECT status FROM order_tracking WHERE order_id = %s", (order_id,)
            )
            result = cursor.fetchone()

            if result is not None:
                return result[0]
            else:
                return None

    def save_order(self, order_dict: Dict[str, int]):
        self.ensure_connection()
        try:
            with self.conn.cursor() as cursor:
                food_names = tuple(order_dict.keys())
                placeholders = ", ".join(["%s"] * len(food_names))

                query = f"""
                    SELECT name, item_id, price
                    FROM food_items
                    WHERE name IN ({placeholders})
                """
                cursor.execute(query, food_names)
                results = cursor.fetchall()

                if results is None:
                    raise ValueError(f"{' ,'.join(food_names)} not found")

                db_items = {name: (item_id, price) for name, item_id, price in results}

                for food_item in order_dict.keys():
                    if food_item not in db_items:
                        raise ValueError(f"{food_item} not found")

                cursor.execute("SELECT MAX(order_id) FROM orders")
                max_order_id = cursor.fetchone()[0]

                if max_order_id is None:
                    order_id = 1
                else:
                    order_id = max_order_id + 1

                for food_item, quantity in order_dict.items():
                    item_id, price = db_items[food_item]

                    cursor.execute(
                        "INSERT INTO orders(order_id, item_id, quantity, total_price) VALUES (%s,%s,%s,%s)",
                        (
                            order_id,
                            item_id,
                            int(quantity),
                            float(price) * float(quantity),
                        ),
                    )

                    logging.info(
                        f"{food_item} - {quantity} = {float(quantity) * float(price)} added to database."
                    )

                self.conn.commit()
                return order_id

        except Exception as e:
            self.conn.rollback()
            logging.exception(f"Save order failed: {e}")
            return -1

    def get_order_total(self, order_id: int) -> float:
        self.ensure_connection()
        try:
            with self.conn.cursor() as curser:
                curser.execute(
                    """SELECT SUM(total_price)
                       FROM orders
                       WHERE order_id=%s
                    """,
                    (order_id,),
                )

                result = curser.fetchone()

                if result is None:
                    raise ValueError(f"Something went wrong with order id: {order_id}")

                total_price = result[0]
                return total_price
        except Exception as e:
            logging.exception(f"Database error: {e}")

    def insert_order_tracking(self, order_id: int, status: str):
        self.ensure_connection()
        try:
            with self.conn.cursor() as curser:
                curser.execute(
                    """INSERT INTO order_tracking(order_id, status)
                       VALUES(%s, %s)
                    """,
                    (order_id, status),
                )

                self.conn.commit()

        except Exception as e:
            self.conn.rollback()
            logging.exception(f"Database error: {e}")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, force=True)
    load_dotenv()
    mysql_conn = DbConnect()
    mysql_conn.save_order({"Pizza": 2})
