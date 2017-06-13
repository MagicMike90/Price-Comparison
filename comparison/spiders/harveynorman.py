# -*- coding: utf-8 -*-
import scrapy


class HarveynormanSpider(scrapy.Spider):
    name = "harveynorman"
    allowed_domains = ["harveynorman.com"]
    start_urls = ['http://harveynorman.com/']

    def parse(self, response):
        pass
