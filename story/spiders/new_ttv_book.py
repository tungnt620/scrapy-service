# -*- coding: utf-8 -*-
import scrapy
import json


class TTVBookSpider(scrapy.Spider):
    name = 'new_ttv_book'
    allowed_domains = ['truyen.tangthuvien.vn']
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'story.pipelines.NewTTVBookPipeline': 300,
        }
    }
    page = 0

    def __init__(self, redis_stream_name='', **kwargs):
        self.redis_stream_name = redis_stream_name
        self.start_url = 'https://truyen.tangthuvien.vn/tong-hop?ord=new&page='
        self.start_urls = [self.start_url + str(self.page)]
        super().__init__(**kwargs)

    def get_books(self, response):
        books = []

        book_slugs = response.css('.rank-view-list ul li .book-mid-info h4 a::attr(href)').getall()
        for i in range(len(book_slugs)):
            slug = book_slugs[i]
            slug_parts = slug.split("/")
            if slug_parts[len(slug_parts) - 1] == "":
                slug = slug_parts[len(slug_parts) - 2]
            else:
                slug = slug_parts[len(slug_parts) - 1]
            books.append({
                'source': 'ttv',
                'source_id': slug,
            })

        book_names = response.css('.rank-view-list ul li .book-mid-info h4 a::text').getall()
        for i in range(len(book_names)):
            books[i]['name'] = book_names[i]

        if len(books):
            return {
                'books': json.dumps(books),
                'redis_stream_name': self.redis_stream_name
            }
        else:
            return None

    def parse(self, response):
        books = self.get_books(response)
        if books:
            self.page += 1
            yield books
        else:
            return None

        yield scrapy.Request(self.start_url + str(self.page), callback=self.parse)
