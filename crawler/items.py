# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class KompassItem(scrapy.Item):
    category = scrapy.Field()
    subCategory = scrapy.Field()
    name = scrapy.Field()
    country = scrapy.Field()
    kompassId = scrapy.Field()
    distributor = scrapy.Field()
    supplier = scrapy.Field()
    service = scrapy.Field()
    activities = scrapy.Field()
    website = scrapy.Field()
    description = scrapy.Field()
    importCountries = scrapy.Field()
    exportCountries = scrapy.Field()
    products = scrapy.Field()
