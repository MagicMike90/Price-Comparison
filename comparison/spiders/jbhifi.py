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

    # Rules for horizontal and vertical crawling
    rules = (
        Rule(LinkExtractor(restrict_xpaths='//*[contains(@class,"pagNum")]//a')),
        Rule(LinkExtractor(restrict_xpaths='//*[@id="productsContainer"]//a'),
             callback='parse_item')
    )

    # def parse(self, response):
    #     logger.info(response.url)
    #     # Get the next index URLs and yield Requests
    #     #
    #     # There will be a duplicated links
    #     # next_selector = response.xpath('//*[contains(@class,"main")]/li/a//@href')

    #     # category_selector = response.xpath('//*[contains(@class,"main")]//a/@href');
    #     # for url in category_selector.extract():
    #     #     logger.info(url)
    #     #     yield Request(urlparse.urljoin(response.url, url))

    #     # next_selector = response.xpath('//*[contains(@class,"pagNum")]//a/@href')
    #     # for url in next_selector.extract():
    #     #     yield Request(urlparse.urljoin(response.url, url))

    #     # # Get item URLs and yield Requests
    #     # item_selector = response.xpath('//*[@id="productsContainer"]//a/@href')
    #     # for url in item_selector.extract():
    #     #     yield Request(urlparse.urljoin(response.url, url),
    #     #                   callback=self.parse_item)

    #     # page = response.url.split("/")[-2]
    #     # filename = 'price-%s.html' % page
    #     # with open(filename, 'wb') as f:
    #     #     f.write(response.body)
    #     # self.log('Saved file %s' % filename)

    def parse_item(self, response):
        logger.info(response.url)
        # Create the loader using the response
        l = ItemLoader(item=ComparisonItem(), response=response)

        # # Load fields using XPath expressions
        l.add_xpath('title', '//*[contains(@class,"primary")]//h1/text()')
        l.add_xpath('price', '//*[contains(@class,"overview")]//*[contains(@class,"amount")]/text()',
                    re='[,.0-9]+')
        # l.add_xpath('description', '//div[@id="tab1"]//*[contains(@class,"cms-content")]',
        #             MapCompose(unicode.strip), Join())
        # l.add_xpath('address',
        #             '//*[@itemtype="http://schema.org/Place"][1]/text()',
        #             MapCompose(unicode.strip))
        l.add_xpath('image_urls', '//*[@class="gallery"]//img[1]/@src',
                    MapCompose(lambda i: urlparse.urljoin(response.url, i)))


        # Housekeeping fields
        l.add_value('url', response.url)
        l.add_value('project', self.settings.get('BOT_NAME'))
        l.add_value('spider', self.name)
        l.add_value('server', socket.gethostname())
        # l.add_value('date', datetime.datetime.now())
        return l.load_item()

        # i = {}
        # #i['domain_id'] = response.xpath('//input[@id="sid"]/@value').extract()
        # #i['name'] = response.xpath('//div[@id="name"]').extract()
        # #i['description'] = response.xpath('//div[@id="description"]').extract()
        # return i
