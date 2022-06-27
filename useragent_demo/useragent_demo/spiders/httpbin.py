import scrapy
import json

class HttpbinSpider(scrapy.Spider):
    name = 'httpbin'
    allowed_domains = ['httpbin.org']
    start_urls = ['http://httpbin.org/user-agent']

    def parse(self, response):
        useragent = json.loads(response.text)["user-agent"]
        name = 'sky'
        password = '123456'
        print('='*50)
        print(useragent)
        yield scrapy.Request(self.start_urls[0],callback=self.parse_i,dont_filter=True,meta={
            'info':(name,password)
        })

    def parse_i(self,response):
        name,password = response.meta['info']
        print(name,password)
