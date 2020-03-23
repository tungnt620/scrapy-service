# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
from story.redis_client import redisClient


class TTVBookSpider(scrapy.Spider):
    name = 'wuxiaworld_test'
    allowed_domains = ['wuxiaworld.com']
    start_urls = ['https://www.wuxiaworld.com/profile/karma']
    custom_settings = {
        'ITEM_PIPELINES': {
            'story.pipelines.WuxiaWorldBookPipeline': 300,
        }
    }

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def start_requests(self):
        for url in self.start_urls:
            yield Request(
                url,
                cookies={
                    'WuxiaWorld.Auth': redisClient.get('wuxiaworld_auth').decode('ascii'),
                },
                callback=self.parse
            )

    def parse(self, response):
        print('Purchase History' in response.text)
        print(response.text)
        return {}
