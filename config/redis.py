import redis.asyncio as redis
from dotenv import load_dotenv
import os

load_dotenv()

# r = redis.Redis(
#     host=os.getenv('REDIS_HOST', 'localhost'),
#     port=int(os.getenv('REDIS_PORT')),
#     decode_responses=True,
#     username=os.getenv('REDIS_USERNAME', ''),
#     password=os.getenv('REDIS_PASSWORD', ''),
# )

pool = redis.ConnectionPool(
    host=os.getenv('REDIS_HOST', 'localhost'),
    port=int(os.getenv('REDIS_PORT')),
    decode_responses=True,
    username=os.getenv('REDIS_USERNAME', ''),
    password=os.getenv('REDIS_PASSWORD', ''),
    max_connections=10,  
    socket_timeout=5,
    socket_connect_timeout=5,
    retry_on_timeout=True,
)

r = redis.Redis(connection_pool=pool)
