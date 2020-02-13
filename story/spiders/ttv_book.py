# -*- coding: utf-8 -*-
import scrapy
import json


class TTVBookSpider(scrapy.Spider):
    name = 'ttv_book'
    allowed_domains = ['truyen.tangthuvien.vn']
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'story.pipelines.TTVBookPipeline': 300,
        }
    }

    def __init__(self, redis_stream_name='', book_url='', id='', **kwargs):
        self.start_urls = [book_url]
        self.id = id
        self.redis_stream_name = redis_stream_name
        super().__init__(**kwargs)

    def parse(self, response):
        author = response.css('.author-info .author-photo p a::text').get(default='').strip()
        cats = response.css('.book-information .book-info .tag a::text').getall()
        if author in cats:
            cats.remove(author)

        story_data = {
            'book': json.dumps({
                'name': response.css('.book-information .book-info h1::text').get(default='').strip(),
                'desc': response.css(".book-info-detail .book-intro > p").get(default='').strip(),
                'img': response.css('.book-information .book-img img').attrib['src'].strip(),
                'author': author,
                'cats': json.dumps(cats),
                'id': self.id,
            }),
            'redis_stream_name': self.redis_stream_name
        }

        return story_data
