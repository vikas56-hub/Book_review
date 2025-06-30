import redis
import json

try:
    redis_client = redis.Redis(host="localhost", port=6379, db=0)
    redis_client.ping()
    print("✅ Connected to Redis")
except redis.ConnectionError:
    redis_client = None
    print("❌ Redis not running — caching disabled")


def get_books_from_cache():
    if redis_client:
        data = redis_client.get("books")
        if data:
            return json.loads(data)
    return None


def set_books_to_cache(books):
    if redis_client:
        redis_client.set("books", json.dumps(books))
