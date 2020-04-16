# -*- coding: utf-8 -*-
import scrapy


class HotelsSpider(scrapy.Spider):
    name = 'hotels'
    allowed_domains = ['hotelscombined.com']
    start_urls = ['https://hotelscombined.com/Countries/All']
    host = "https://www.hotelscombined.com"

    def parse(self, response):
        countryList = response.xpath('//div[@id="hc_browseBy"]/div/div[contains(@class,"hc_m_content")]//li/a/@href').extract()
        for country in countryList:
            link = self.host + country
            yield scrapy.http.Request(url=link,callback=self.parseCountryPage)

    def parseCountryPage(self,response):
        hotelsLink = response.xpath('//a[@data-ceid="all_hotels"]/@href').get()
        print(hotelsLink)
