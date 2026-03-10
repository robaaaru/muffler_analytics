import psycopg2
import os
from dotenv import load_dotenv


load_dotenv()

def get_connection():
    return psycopg2.connect(
        host = os.getenv("DB_HOST"),
        database = os.getenv("DB_NAME"),
        user = os.getenv("DB_USER"),
        password = os.getenv("DB_PASSWORD"),
        port = os.getenv("DB_PORT")
    )

if __name__ == "__main__":
    conn = get_connection()
    print('Connection established')
    conn.close()
    

