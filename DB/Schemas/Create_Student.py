import psycopg2
from loguru import logger
import time
import os
from dotenv import load_dotenv
import sys
import json

load_dotenv()


def serialize(record):
    subset = {
        "timestamp": record["time"].strftime("%Y-%m-%d %H:%M:%S.%f")[:-3],
        "message": record["message"],
        "level": record["level"].name,
        "function": record["function"],
        "line": record["line"],
        "file": record["file"].name,
        "module": record["module"]
    }
    return json.dumps(subset)


def patching(record):
    record["extra"]["serialized"] = serialize(record)


logger.remove()
logger = logger.patch(patching)
logger.add(sys.stderr, format="{extra[serialized]}", backtrace=True)

db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT')

if not all([db_name, db_user, db_password, db_host, db_port]):
    logger.error({"One or more required environment "
                 "variables are not set or empty."})
    exit(1)


def create_schema():
    while True:
        try:
            conn = psycopg2.connect(
                database=db_name,
                user=db_user, password=db_password,
                host=db_host, port=db_port)
            cur = conn.cursor()
            create_table_query = """
            CREATE TABLE IF NOT EXISTS students (
                ID SERIAL PRIMARY KEY,
                name VARCHAR(255),
                email VARCHAR(255),
                age INTEGER,
                phone VARCHAR(50)
                )"""
            cur.execute(create_table_query)
            # Make the changes to the database persistent
            conn.commit()
            # Close cursor and communication with the database
            cur.close()
            conn.close()
            logger.info("Schema Created")
            break
        except Exception as error:
            logger.error({f"message:Schema Not Created Errors: {error}"})
            time.sleep(10)
            continue


if __name__ == "__main__":
    create_schema()
