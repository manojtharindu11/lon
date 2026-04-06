import mysql.connector
import os
from dotenv import load_dotenv


class DbConnect:
    def __init__(self):
        self.host = os.getenv("HOST", "localhost")
        self.user = os.getenv("USER", "root")
        self.password = os.getenv("PASSWORD", "")
        self.database = os.getenv("DATABASE", "")
        self.cursor = None
        self.connect()

    def connect(self):
        self.conn = mysql.connector.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
        )

        if self.conn.is_connected():
            print("Successfully connected to the database.")
            self.cursor = self.conn.cursor()

    def disconnect(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.conn.is_connected():
            self.conn.disconnect()
        print("Successfully close the database connection")

    def get_order_status(self, order_id: int):
        if self.cursor is not None:
            query = "SELECT status FROM order_tracking WHERE order_id = %s"

            self.cursor.execute(query, (order_id,))
            result = self.cursor.fetchone()

            if result is not None:
                return result[0]
            else:
                return None

        else:
            self.connect()
            return self.get_order_status(order_id)


if __name__ == "__main__":
    load_dotenv()
    mysql_conn = DbConnect()
