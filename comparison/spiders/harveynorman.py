# -*- coding: utf-8 -*-
import datetime
import socket
import scrapy

from urllib.parse import urlparse
from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader

from comparison.items import ComparisonItem

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

class HarveynormanSpider(CrawlSpider):
    name = "harveynorman"
    allowed_domains = ["harveynorman.com"]
    start_urls = ['http://harveynorman.com/']

    # Rules for horizontal and vertical crawling
    rules = (
        # Rule(LinkExtractor(restrict_xpaths='//*[contains(@class,"next")]')),
        # Rule(LinkExtractor(restrict_xpaths='//*[@id="nav"]//a/@href'),
        #      callback='parse_item')
        Rule(LinkExtractor(restrict_xpaths=('//*[@id="nav"]//a/@href')))
    )

    def parse(self, response):
        # # Create the loader using the response
        # l = ItemLoader(item=PropertiesItem(), response=response)

        # # Load fields using XPath expressions
        # l.add_xpath('title', '//*[@itemprop="name"][1]/text()',
        #             MapCompose(unicode.strip, unicode.title))
        # l.add_xpath('price', './/*[@itemprop="price"][1]/text()',
        #             MapCompose(lambda i: i.replace(',', ''), float),
        #             re='[,.0-9]+')
        # l.add_xpath('description', '//*[@itemprop="description"][1]/text()',
        #             MapCompose(unicode.strip), Join())
        # l.add_xpath('address',
        #             '//*[@itemtype="http://schema.org/Place"][1]/text()',
        #             MapCompose(unicode.strip))
        # l.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src',
        #             MapCompose(lambda i: urlparse.urljoin(response.url, i)))

        # return l.load_item()
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
