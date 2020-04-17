# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import scraperwiki

class CrawlerPipeline(object):
    def process_item(self, item, spider):
        return item

class KomapssSaveToMorphPipeline(object):
    def process_item(self,item,spider):
        unique_keys = ['kompassId']
        scraperwiki.sql.save(unique_keys,dict(item),table_name='data')
        return item
