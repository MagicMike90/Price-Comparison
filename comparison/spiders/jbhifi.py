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

logger = logging.getLogger('JbhifiSpider')

class JbhifiSpider(CrawlSpider):
    name = 'jbhifi'
    allowed_domains = ['jbhifi.com.au']
    start_urls = [
        # 'https://www.jbhifi.com.au/',
        'https://www.jbhifi.com.au/computers-tablets/tablets/']

    def parse(self, response):
        logger.info(response.url)
        # Get the next index URLs and yield Requests
        #
        # There will be a duplicated links
        # next_selector = response.xpath('//*[contains(@class,"main")]/li/a//@href')
        next_selector = response.xpath('//*[contains(@class,"main")]/li/a//@href')
        for url in next_selector.extract():
            logger.info(url)
            yield Request(urlparse.urljoin(response.url, url))

        # Get item URLs and yield Requests
        item_selector = response.xpath('//*[contains(@class,"photo-box")]/a/@href')
 
        for url in item_selector.extract():
            logger.info(url)
            yield Request(urlparse.urljoin(response.url, url),
                          callback=self.parse_item)

        # page = response.url.split("/")[-2]
        # filename = 'price-%s.html' % page
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        # self.log('Saved file %s' % filename)

    def parse_item(self, response):
        logger.info(response.url)
        # Create the loader using the response
        l = ItemLoader(item=HNItem(), response=response)

        # # Load fields using XPath expressions
        l.add_xpath('title', '//*[@class="name"][1]/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('title', '//*[@class="product-name"][1]/text()',
                    MapCompose(unicode.strip, unicode.title))
        l.add_xpath('price', './/*[@class="amount"][1]/text()',
                    MapCompose(lambda i: i.replace(',', ''), float),
                    re='[,.0-9]+')
        l.add_xpath('description', '//*[@class="short-description"][1]/text()',
                    MapCompose(unicode.strip), Join())
        # l.add_xpath('address',
        #             '//*[@itemtype="http://schema.org/Place"][1]/text()',
        #             MapCompose(unicode.strip))
        # l.add_xpath('image_urls', '//*[@itemprop="image"][1]/@src',
        #             MapCompose(lambda i: urlparse.urljoin(response.url, i)))
        return l.load_item()

        # i = {}
        # #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # #i['name'] = response.xpath('//div[@id="name"]').extract()
        # #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i
