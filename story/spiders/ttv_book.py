# -*- coding: utf-8 -*-
import scrapy


class TTVBookSpider(scrapy.Spider):
    name = 'ttv_book'
    allowed_domains = ['truyen.tangthuvien.vn']
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'story.pipelines.TTVBookPipeline': 300,
        }
    }

    def __init__(self, book_url='', is_override=0, old_book_slug='', **kwargs):
        self.start_urls = [book_url]
        self.is_override = is_override
        self.old_book_slug = old_book_slug
        super().__init__(**kwargs)

    def parse(self, response):
        author = response.css('.author-info .author-photo p a::text').get(default='').strip()
        cats = response.css('.book-information .book-info .tag a::text').getall()
        if author in cats:
            cats.remove(author)

        story_data = {
            'name': response.css('.book-information .book-info h1::text').get(default='').strip(),
            'desc': response.css(".book-info-detail .book-intro > p").get(default='').strip(),
            'img': response.css('.book-information .book-img img').attrib['src'].strip(),
            'author': author,
            'cats': cats,
            'old_book_slug': self.old_book_slug,
            'is_override': self.is_override,
        }

        return story_data
