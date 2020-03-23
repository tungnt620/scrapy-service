import redis
from story.target import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD

redisClient = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
