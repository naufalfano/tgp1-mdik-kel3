import redis.asyncio as redis

r = redis.Redis(
    host='redis-12234.c296.ap-southeast-2-1.ec2.redns.redis-cloud.com',
    port=12234,
    decode_responses=True,
    username="default",
    password="hSbzVlFJTaYhLjjrrmhzFcjT68iPdd5S",
)