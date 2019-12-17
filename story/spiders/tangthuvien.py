# -*- coding: utf-8 -*-
import scrapy


class TangthuvienSpider(scrapy.Spider):
    name = 'tangthuvien'
    allowed_domains = ['truyen.tangthuvien.vn']
    start_urls = []
    custom_settings = {
        'ITEM_PIPELINES': {
            'story.pipelines.StoryPipeline': 300,
        }
    }

    story_data = {
        'name': '',
        'desc': '',
        'chapter_data': {
            'no': 1,
            'name': '',
            'content': '',
        }
    }
    is_already_fetch_list_chapter = False
    is_already_get_chapter_url = False

    def __init__(self, story_url='', chapter_num=1, **kwargs):
        self.start_urls = [story_url]
        self.chapter_num = chapter_num
        super().__init__(**kwargs)

    def get_chapter_data(self, response):
        name = response.css('.content .chapter h2::text').get(default='')
        name = name.split(':')
        name = name[1].strip() if len(name) > 1 else ''

        content = response.css('.content .chapter-c-content .box-chap:not(.hidden)::text').get(default='').strip()

        return {
            'no': self.chapter_num,
            'name': name,
            'content': content
        }

    def parse(self, response):
        if not self.story_data['name']:
            # Crawl story data
            name = response.css('.book-information .book-info h1::text').get(default='').strip()
            desc = response.css(".book-info-detail .book-intro > p").get(default='').strip()
            self.story_data['name'] = name
            self.story_data['desc'] = desc

            chapter_one_url = response.css('.book-information .book-info .J-getJumpUrl::attr(href)').get(default='').strip()
            yield scrapy.Request(chapter_one_url, callback=self.parse)
        else:
            # Crawl chapter data
            if self.chapter_num == 1:
                self.story_data['chapter_data'] = self.get_chapter_data(response)
                yield self.story_data
            elif not self.is_already_fetch_list_chapter:
                load_chap_url = response.css('body').re(r'https:\/\/truyen.tangthuvien.vn\/story\/chapters\?story_id=[0-9]+&chapter_id=[0-9]+')
                if len(load_chap_url) > 0:
                    load_chap_url = load_chap_url[0].strip()
                    self.is_already_fetch_list_chapter = True
                    yield scrapy.Request(load_chap_url, callback=self.parse)
            elif not self.is_already_get_chapter_url:
                chap_url = response.css('.link-chap-{}::attr(href)'.format(self.chapter_num)).get(default='').strip()
                self.is_already_get_chapter_url = True
                yield scrapy.Request(chap_url, callback=self.parse)
            else:
                self.story_data['chapter_data'] = self.get_chapter_data(response)
                yield self.story_data
