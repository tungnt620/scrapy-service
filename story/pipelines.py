# -*- coding: utf-8 -*-
import redis
from story.target import REDIS_HOST, REDIS_PORT, REDIS_PASSWORD


class BasePipeline(object):

    def __init__(self):
        redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, password=REDIS_PASSWORD)
        self.redisClient = redis_client
        super().__init__()

    def process_item(self, item, spider):
        if item:
            redis_stream_name = item['redis_stream_name']
            del item['redis_stream_name']

            self.redisClient.xadd(
                redis_stream_name,
                item,
            )

        return item


class NewTTVBookPipeline(BasePipeline):

    def __init__(self):
        super().__init__()


class TTVBookPipeline(BasePipeline):

    def __init__(self):
        super().__init__()


class TTVChapterPipeline(BasePipeline):

    def __init__(self):
        super().__init__()
