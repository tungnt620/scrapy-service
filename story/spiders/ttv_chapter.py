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

    def __init__(self, book_url='', book_slug='', chapter_num=1, is_override=0, old_chapter_slug='', **kwargs):
        self.start_urls = [book_url]
        self.chapter_num = chapter_num
        self.book_slug = book_slug
        self.old_chapter_slug = old_chapter_slug
        self.is_override = is_override

        super().__init__(**kwargs)

    def get_chapter_data(self, response):
        name = response.css('.content .chapter h2::text').get(default='')

        name = name.split(':')
        name = name[1].strip() if len(name) > 1 else ''

        content = response.css('.content .chapter-c-content .box-chap:not(.hidden)::text').get(default='').strip()

        return {
            'book_slug': self.book_slug,
            'no': self.chapter_num,
            'name': name,
            'text': content,
            'old_chapter_slug': self.old_chapter_slug,
            'is_override': self.is_override,
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
