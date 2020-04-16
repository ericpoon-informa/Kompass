import random
from scrapy import signals
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware

class RandomUserAgentMiddleware(UserAgentMiddleware):
    
    def __init__(self,settings,user_agent='Scrapy'):
        self.user_agent_list = settings.get('USER_AGENT_LIST')
        if settings.get('USER_AGENT') is not None:
            self.user_agent = settings.get('USER_AGENT')
        else:
            self.user_agent = user_agent

    @classmethod
    def from_crawler(cls,crawler):
        o = cls(crawler.settings)
        crawler.signals.connect(o.spider_opened,signal=signals.spider_opened)
        return o

    def process_request(self,request,spider):
        if self.user_agent_list:
            user_agent = random.choice(self.user_agent_list)
        else:
            user_agent = self.user_agent
        request.headers.setdefault(b'User-Agent',user_agent)
