import time
import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def wait_for_db():
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    
    print('Waiting for database...')
    print(f"dbname={dbname}, user={user}, password={password}, host={host}")
    
    while True:
        try:
            conn = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host
            )
            conn.close()
            print("Database is ready!")
            break
        except psycopg2.OperationalError:
            print("Database is not ready. Waiting...")
            time.sleep(1)

if __name__ == "__main__":
    wait_for_db()