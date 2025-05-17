from sqlalchemy import text
from config.database import Engine

def test_connection():
    try:
        with Engine.connect() as connection:
            result = connection.execute(text("SELECT 1"))
            for row in result:
                print(f"Connection successful: {row[0]}")
            return True
        
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

if __name__ == "__main__":
    test_connection()