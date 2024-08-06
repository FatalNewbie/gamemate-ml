# database_test.py
from sqlalchemy.orm import Session
from data.database import get_db

def test_db_connection():
    db = next(get_db())
    try:
        result = db.execute("SELECT 1")
        print(result.fetchone())
    finally:
        db.close()

if __name__ == "__main__":
    test_db_connection()
