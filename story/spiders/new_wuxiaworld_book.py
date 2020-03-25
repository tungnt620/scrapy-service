# -*- coding: utf-8 -*-
import scrapy
import json

from scrapy.http import JsonRequest


class TTVBookSpider(scrapy.Spider):
    name = 'new_wuxiaworld_book'
    allowed_domains = ['wuxiaworld.com']
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'story.pipelines.NewWuxiaWorldBookPipeline': 300,
        }
    }

    def __init__(self, redis_stream_name='', **kwargs):
        self.redis_stream_name = redis_stream_name
        super().__init__(**kwargs)

    def start_requests(self):
        return [
            JsonRequest(
                url="https://www.wuxiaworld.com/api/novels/search",
                method='POST',
                body=json.dumps({
                    "title": "", "tags": [], "language": "Any", "genres": [], "active": None,
                    "sortType": "Name", "sortAsc": True, "searchAfter": None, "count": 1000
                }),
                callback=self.parse
            )
        ]

    def get_books(self, response):
        books = []

        resp_json = json.loads(response.body.decode('utf-8'))
        raw_books_data = resp_json['items']

        for book in raw_books_data:
            books.append({
                'name': book['name'],
                'img': book['coverUrl'],
                'cats': json.dumps(book['tags'] + book['genres']),
                # 'source_total_chapter': book['chapterCount'], # Not get because it out update
                'source_abbreviation': book['abbreviation'].lower(),
                'source': 'wuxiaworld',
                'source_id': book['slug'],
            })

        if len(books):
            return {
                'books': json.dumps(books),
                'redis_stream_name': self.redis_stream_name
            }
        else:
            return None

    def parse(self, response):
        books = self.get_books(response)
        yield books
