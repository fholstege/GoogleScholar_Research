# -*- coding: utf-8 -*-
import scrapy


class GscholarSpider(scrapy.Spider):
    name = 'gscholar'
    allowed_domains = ['scholar.google.com']
    start_urls = ['http://scholar.google.com/']

    def parse(self, response):
        pass
