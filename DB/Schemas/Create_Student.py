import psycopg2
from loguru import logger
import time
import os
from dotenv import load_dotenv

load_dotenv()
db_name = os.getenv('POSTGRES_DB')
db_user = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_host = os.getenv('POSTGRES_HOST')
db_port = os.getenv('POSTGRES_PORT')


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
        except (Exception, psycopg2.DatabaseError) as error:
            print("Schema Not Created Errors:", error)
            time.sleep(10)
            continue


if __name__ == "__main__":
    create_schema()
