# -*- coding: utf-8 -*-
import scrapy
import json
from html.parser import HTMLParser
from scrapy.http import Request
from story.redis_client import redisClient


class TTVChapterSpider(scrapy.Spider):
    name = 'wuxiaworld_chapter'
    allowed_domains = ['wuxiaworld.com']
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'story.pipelines.WuxiaWorldChapterPipeline': 300,
        }
    }

    def __init__(self, redis_stream_name='', chapter_url='', book_id='', order_no=1, **kwargs):
        self.start_urls = [chapter_url]
        self.book_id = book_id
        self.order_no = order_no
        self.redis_stream_name = redis_stream_name

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

    def get_chapter_data(self, response):
        name = self.get_name(response)
        content = self.get_content(response)

        return {
            'chapter': json.dumps({
                'name': name,
                'text': content,
                'book_id': self.book_id,
                'order_no': self.order_no,
            }),
            'redis_stream_name': self.redis_stream_name,
        }

    def get_name(self, response):
        chapter_data = {}

        class MyHTMLParser(HTMLParser):
            def __init__(self, chapter_data_para):
                self.chapter_data = chapter_data_para
                super().__init__(convert_charrefs=True)

            def handle_data(self, data):
                if data and data != '\n':
                    self.chapter_data['name'] = data

        chapter_name_html = response.css('.section-content .panel .caption').get(default='')
        MyHTMLParser(chapter_data).feed(chapter_name_html)
        return chapter_data['name']

    def get_content(self, response):
        chapter_data = {'content': ''}

        class MyHTMLParser(HTMLParser):
            def __init__(self, chapter_data_para):
                self.chapter_data = chapter_data_para
                super().__init__(convert_charrefs=True)

            def handle_starttag(self, tag, attrs):
                if tag == 'hr':
                    self.chapter_data['content'] += ' {{pause_some_second}} '

            def handle_endtag(self, tag):
                if tag == 'p':
                    self.chapter_data['content'] += '. '

            def handle_data(self, data):
                if data and data.strip() not in ['Previous Chapter', '\n', 'Next Chapter']:
                    self.chapter_data['content'] += data

        chapter_content_html = response.css('.section-content #chapter-content').get(default='')

        if 'Enable auto unlock' in chapter_content_html \
                or 'karma or a VIP subscription to access' in chapter_content_html \
                or 'Purchase/Earn karma' in chapter_content_html \
                or 'Subscribe to VIP' in chapter_content_html:
            return 'vip_content'
        else:
            MyHTMLParser(chapter_data).feed(chapter_content_html)

            content = chapter_data['content'].strip()
            if content.startswith('.'):
                content = content[1:]

            content = content.strip(' \n.')
            if content.endswith('{{pause_some_second}}'):
                content = content[: len(content) - len('{{pause_some_second}}')]

            return content

    def parse(self, response):
        return self.get_chapter_data(response)
