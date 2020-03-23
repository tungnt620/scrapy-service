# -*- coding: utf-8 -*-
import scrapy
import json


class TTVBookSpider(scrapy.Spider):
    name = 'wuxiaworld_book'
    allowed_domains = ['wuxiaworld.com']
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'story.pipelines.WuxiaWorldBookPipeline': 300,
        }
    }

    def __init__(self, redis_stream_name='', book_url='', id='', **kwargs):
        self.start_urls = [book_url]
        self.id = id
        self.redis_stream_name = redis_stream_name
        super().__init__(**kwargs)

    def parse(self, response):
        author = response.css('.novel-body dd::text').extract()[1].strip()
        chapter_urls = response.css('.novel-content .chapter-item a').xpath('@href').getall()
        desc = response.xpath("//h3[contains(text(), 'Synopsis')]/following-sibling::div//p//text()").extract()
        desc_formatted = ''
        for part in desc:
            desc_formatted += part + ' . '

        story_data = {
            'book': json.dumps({
                'desc': desc_formatted,
                'author': author,
                'chapter_urls': json.dumps(chapter_urls),
                'id': self.id,
            }),
            'redis_stream_name': self.redis_stream_name
        }

        return story_data
