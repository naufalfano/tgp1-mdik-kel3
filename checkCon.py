from sqlalchemy import text
from config.database import Engine
import asyncio

async def test_connection():
    try:
        async with Engine.connect() as connection:
            result = await connection.execute(text("SELECT 1"))
            rows = result.fetchall()
            for row in rows:
                print(f"Connection successful: {row[0]}")
            return True
        
    except Exception as e:
        print(f"Connection failed: {e}")
        return False

async def main():
    result = await test_connection()
    await Engine.dispose()

if __name__ == "__main__":
    asyncio.run(main())