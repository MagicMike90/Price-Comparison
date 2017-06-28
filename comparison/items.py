# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field
from scrapy.loader.processors import Join, MapCompose, TakeFirst

from w3lib.html import remove_tags


class ComparisonItem(scrapy.Item):
    default_output_processor = TakeFirst()

    # Primary fields
    title = Field(input_processor = MapCompose(unicode.strip, unicode.title,remove_tags))
    price = Field(input_processor = MapCompose(lambda i: i.replace(',', '')))
    # title = Field()
    # price = Field()
    description = Field()
    address = Field()
    image_urls = Field()

    # Calculated fields
    images = Field()
    location = Field()

    # Housekeeping fields
    url = Field()
    project = Field()
    spider = Field()
    server = Field()
    date = Field()
