# -*- coding: utf-8 -*-
import scrapy
import json
import re
import datetime


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
        is_full = "Đã hoàn thành" in response.css('.book-information .book-info .tag span::text').getall()
        author = response.css('.author-info .author-photo p a::text').get(default='').strip()
        cats = response.css('.book-information .book-info .tag a::text').getall()
        if author in cats:
            cats.remove(author)

        source_like = response.css('.book-information .book-info').xpath("//p//span[re:test(@class, '\.*-like$')]/text()").get(default='').strip()
        if source_like:
            source_like = int(source_like)

        source_view = response.css('.book-information .book-info').xpath("//p//span[re:test(@class, '\.*-view$')]/text()").get(default='').strip()
        if source_view:
            source_view = int(source_view)

        source_follow = response.css('.book-information .book-info').xpath("//p//span[re:test(@class, '\.*-follow$')]/text()").get(default='').strip()
        if source_follow:
            source_follow = int(source_follow)

        source_last_update = response.css('.catalog-content-wrap').xpath('//h3//em//text()').get(default='')
        match = re.compile(r'.+ (\d{0,2})\/(\d{0,2})\/(\d{4}) (\d{0,2}):(\d{0,2}).+').match(source_last_update)
        if match:
            date, month, year, hour, minute = match.groups()
            date = datetime.datetime(int(year), int(month), int(date), int(hour), int(minute))
            source_last_update = date.isoformat()

        source_total_chapter = response.css('.content-nav-wrap .nav-wrap').xpath('//ul//li//a[@onclick=$val]//text()', val='changeTab(2)').get()
        match = re.compile(r'.*\((\d{1,10}).*').match(source_total_chapter)
        if match:
            source_total_chapter = int(match.groups()[0])

        story_data = {
            'book': json.dumps({
                'name': response.css('.book-information .book-info h1::text').get(default='').strip(),
                'desc': response.css(".book-info-detail .book-intro > p").get(default='').strip(),
                'img': response.css('.book-information .book-img img').attrib['src'].strip(),
                'author': author,
                'cats': json.dumps(cats),
                'is_full': 1 if is_full else 0,
                'source_like': source_like,
                'source_view': source_view,
                'source_follow': source_follow,
                'source_last_update': source_last_update,
                'source_total_chapter': source_total_chapter,
                'id': self.id,
            }),
            'redis_stream_name': self.redis_stream_name
        }

        return story_data
