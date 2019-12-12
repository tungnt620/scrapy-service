# -*- coding: utf-8 -*-
import scrapy


class TangthuvienSpider(scrapy.Spider):
    name = 'tangthuvien'
    allowed_domains = ['truyen.tangthuvien.vn']
    start_urls = ['https://truyen.tangthuvien.vn/']

    def parse(self, response):
        pass
