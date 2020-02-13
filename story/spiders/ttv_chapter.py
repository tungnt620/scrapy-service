# -*- coding: utf-8 -*-
import scrapy


class TTVChapterSpider(scrapy.Spider):
    name = 'ttv_chapter'
    allowed_domains = ['truyen.tangthuvien.vn']
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'story.pipelines.TTVChapterPipeline': 300,
        }
    }
    is_already_fetch_chapter_one = False
    is_already_fetch_list_chapter = False
    is_already_get_chapter_url = False

    def __init__(self, redis_stream_name='', book_url='', book_id='', chapter_num=1, old_chapter_id='', **kwargs):
        self.start_urls = [book_url]
        self.chapter_num = chapter_num
        self.book_id = book_id
        self.old_chapter_id = old_chapter_id
        self.redis_stream_name = redis_stream_name

        super().__init__(**kwargs)

    def get_chapter_data(self, response):
        name = response.css('.content .chapter h2::text').get(default='')

        name = name.split(':')
        name = name[1].strip() if len(name) > 1 else ''

        content = response.css('.content .chapter-c-content .box-chap:not(.hidden)::text').get(default='').strip()

        return {
            'no': self.chapter_num,
            'name': name,
            'text': content,
            'book_id': self.book_id,
            'old_chapter_id': self.old_chapter_id,
            'redis_stream_name': self.redis_stream_name,
        }

    def parse(self, response):
        if not self.is_already_fetch_chapter_one:
            chapter_one_url = response.css('.book-information .book-info .J-getJumpUrl::attr(href)').get(
                default='').strip()
            self.is_already_fetch_chapter_one = True
            yield scrapy.Request(chapter_one_url, callback=self.parse)
        else:
            # Crawl chapter data
            if self.chapter_num == 1:
                yield self.get_chapter_data(response)
            elif not self.is_already_fetch_list_chapter:
                load_chap_url = response.css('body').re(
                    r'https:\/\/truyen.tangthuvien.vn\/story\/chapters\?story_id=[0-9]+&chapter_id=[0-9]+')
                if len(load_chap_url) > 0:
                    load_chap_url = load_chap_url[0].strip()
                    self.is_already_fetch_list_chapter = True
                    yield scrapy.Request(load_chap_url, callback=self.parse)
            elif not self.is_already_get_chapter_url:
                chap_url = response.css('.link-chap-{}::attr(href)'.format(self.chapter_num)).get(default='').strip()
                self.is_already_get_chapter_url = True
                yield scrapy.Request(chap_url, callback=self.parse)
            else:
                yield self.get_chapter_data(response)
