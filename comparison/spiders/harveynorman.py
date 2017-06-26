# -*- coding: utf-8 -*-
import datetime
import urlparse
import socket
import logging


from comparison.items import ComparisonItem

from scrapy.loader.processors import MapCompose, Join
from scrapy.loader import ItemLoader

from scrapy.spiders import CrawlSpider, Rule
from scrapy.http import Request
from scrapy.linkextractors import LinkExtractor


logger = logging.getLogger('test')

class HarveynormanSpider(CrawlSpider):
    name = "harveynorman"
    allowed_domains = ["harveynorman.com"]
    start_urls = ['http://www.harveynorman.com.au/computers-tablets/computers/apple-mac-computers']

    # def parse(self, response):
    #     logger.info('Parse function called on %s', response.url)

    # Rules for horizontal and vertical crawling
    # rules = (
    #     Rule(LinkExtractor(restrict_xpaths='//*[@title="Next"]')),
    #     Rule(LinkExtractor(restrict_xpaths='//*[contains(@class, "level0")]'),
    #          callback='parse_item')
    #     # Rule(LinkExtractor(restrict_xpaths=('//*[@id="nav"]//a/@href')))
    # )

    def parse(self, response):
        # logger.info(response.url)
        # Get the next index URLs and yield Requests
        next_selector = response.xpath('//*[contains(@class,"icn-next-page")]//@href')
        for url in next_selector.extract():
            yield Request(urlparse.urljoin(response.url, url))

        # Get item URLs and yield Requests
        item_selector = response.xpath('//*[@itemprop="url"]/@href')
        for url in item_selector.extract():
            yield Request(urlparse.urljoin(response.url, url),
                          callback=self.parse_item)

    def parse_item(self, response):
        logger.info(self)
        logger.info(response.url)
        # Create the loader using the response
        l = ItemLoader(item=PropertiesItem(), response=response)

        # # Load fields using XPath expressions
        l.add_xpath('title', '//*[@itemprop="name"][1]/text()',
                    MapCompose(unicode.strip, unicode.title))
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
        # page = response.url.split("/")[-2]
        # filename = 'quotes-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)
        open_in_browser(response)
        self.log (response)
