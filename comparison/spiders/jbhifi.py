# -*- coding: utf-8 -*-
import datetime
import urlparse
import socket
import logging


from comparison.items import ComparisonItem

from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader

from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule

logger = logging.getLogger('test')

class JbhifiSpider(CrawlSpider):
    name = 'jbhifi'
    allowed_domains = ['jbhifi.com.au']
    start_urls = ['https://www.jbhifi.com.au/']

    rules = (
        Rule(LinkExtractor(allow=r'Items/'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        page = response.url.split("/")[-2]
        filename = 'price-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
        # i = {}
        # #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # #i['name'] = response.xpath('//div[@id="name"]').extract()
        # #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i
