# -*- coding: utf-8 -*-
import scrapy
from urllib.parse import urlparse
from crawler.items import KompassItem

class KompassSpider(scrapy.Spider):
    name = 'kompass'
    allowed_domains = ['www.kompass.com']
    start_urls = ['http://www.kompass.com/selectcountry/']
    headers = {
                        'Host': 'www.kompass.com',
                        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
                        'Accept-Language': 'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
                        'Accept-Encoding': 'gzip, deflate, br',
                        'Connection': 'keep-alive',
                        'Cookie': 'timezoneoffset=-480; JSESSIONID=C7ADE871E9FFE662092EFBC9577BB3E8; _k_cty_lang=en_WW; ROUTEID=.4; cookie_kompass_allowedCookies=Wysistat%2Cws_cookie_dns%2Cwschkvisit24,c1%2Cs1%2Cns_cookietest%2Cns_session,__atuvc%2Cuid,_jsuid%2C_eventqueue,__utma%2C__utmb%2C__utmc%2C__utmz%2C__utmv,undefined; _ga=GA1.2.1870237197.1586939938; _gid=GA1.2.1377952042.1586939938; __gads=ID=b79ef136af449277:T=1586939940:S=ALNI_MYCYXkM6Lr8daMgtaw-eHUmdpNfzQ',
                        'Upgrade-Insecure-Requests': '1',
                        'Pragma': 'no-cache',
                        'Cache-Control': 'no-cachen'
            }

    def start_requests(self):
        url = "http://www.kompass.com/selectcountry/"
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        yield scrapy.http.Request(url,headers=self.headers)

    def parse(self, response):
        countryList = response.xpath('//div[contains(@class,"countries-liste")]/ul//a/@href').extract()
        #for country in countryList:
        country = countryList[0]
        domain = country.replace("https://","").replace(":/","")
        link = "https://" + domain + "/en"
        headers = self.headers
        headers['Host'] = domain
        request = scrapy.http.Request(url=link,callback=self.parseCountryPage,headers=headers,dont_filter=True)
        request.meta['domain'] = domain
        yield request

    def parseCountryPage(self,response):
        domain = response.meta['domain']
        categorySection = response.xpath('//div[contains(@class,"enterprise")]')
        for category in categorySection:
            categoryName = category.xpath('div/a/strong/text()').get()
            subCategories = category.xpath('ul/li/a')
            for subCategory in subCategories:
                subCategoryName = subCategory.xpath('@title').get()
                subCategoryLink = subCategory.xpath('@href').get()
                link = "https://" + domain + subCategoryLink
                headers = self.headers
                headers['Host'] = domain
                request =  scrapy.http.Request(url=link,callback=self.parseCategoryPage,headers=headers,dont_filter=True)
                request.meta['category'] = categoryName
                request.meta['subCategory'] = subCategoryName
                request.meta['domain'] = domain
                yield request

    def parseCategoryPage(self,response):
        category = response.meta['category']
        subCategory = response.meta['subCategory']
        domain = response.meta['domain']
        companyList = response.xpath('//div[@id="resultatDivId"]/div/div/h2/a/@href').extract()
        for company in companyList:
            fakeDomain = "us.kompass.com"
            link = company.replace(domain+"/en",fakeDomain)
            headers = self.headers
            headers['Host'] = fakeDomain
            request = scrapy.http.Request(url=link,callback=self.parseCompanyPage,headers=headers,dont_filter=True)
            request.meta['category'] = category
            request.meta['subCategory'] = subCategory
            request.meta['domain'] = fakeDomain
            yield request
        nextPage = response.xpath('//li[contains(@class,"searchItemLi") and contains(@class,"active")]/following-sibling::li')
        link = nextPage.xpath('a/@href').get()
        if link is not None:
            headers = self.headers
            headers['Host'] = domain
            pageRequest = scrapy.http.Request(url=link,callback=self.parseCategoryPage,headers=headers,dont_filter=True)
            pageRequest.meta['category'] = category
            pageRequest.meta['domain'] = domain
            pageRequest.meta['subCategory'] = subCategory
            yield pageRequest

    def parseCompanyPage(self,response):
        category = response.meta['category']
        subCategory = response.meta['subCategory']
        name = response.xpath('//div[contains(@class,"blockNameCompany")]/h1/text()').get()
        country = response.xpath('//span[@itemprop="addressCountry"]/text()').get()
        kompassId = response.xpath('//tr[contains(@class,"trKid")]/td/text()').get()
        distributor = response.xpath('//i[contains(@class,"distributor")]/following-sibling::a/text()').extract()
        supplier = response.xpath('//i[contains(@class,"supplier")]/following-sibling::a/text()').extract()
        service = response.xpath('//i[contains(@class,"service")]/following-sibling::a/text()').extract()
        activities = response.xpath('//div[contains(@class,"activitiesTree")]//a/text()').extract()
        websites = response.xpath('//div[contains(@class,"listWww")]/p/a/@href').get()
        description = response.xpath('//div[@itemprop="description"]/text()').get()
        importCountries = response.xpath('//div[@id="importCountries"]/text()').get()
        exportCountries = response.xpath('//div[@id="exportCountries"]/text()').get()
        name = name.replace('\r\n'," ").strip()
        item = KompassItem()
        item['category'] = category
        item['subCategory'] = subCategory
        item['name'] = name
        item['country'] = country
        item['kompassId'] = kompassId
        item['distributor'] = distributor
        item['supplier'] = supplier
        item['service'] = service
        item['activities'] = activities
        item['website'] = websites
        item['description'] = description
        item['importCountries'] = importCountries
        item['exportCountries'] = exportCountries
        yield item
