# -*- coding: utf-8 -*-
from story.redis_client import redisClient


class BasePipeline(object):

    def process_item(self, item, spider):
        if item:
            redis_stream_name = item['redis_stream_name']
            del item['redis_stream_name']

            redisClient.xadd(
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


class NewWuxiaWorldBookPipeline(BasePipeline):

    def __init__(self):
        super().__init__()

        
class WuxiaWorldBookPipeline(BasePipeline):

    def __init__(self):
        super().__init__()


class WuxiaWorldChapterPipeline(BasePipeline):

    def __init__(self):
        super().__init__()
