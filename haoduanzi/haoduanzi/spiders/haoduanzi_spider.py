import scrapy
from haoduanzi.items import HaoduanziItem


class HaoduanziSpiderSpider(scrapy.Spider):
    name = 'haoduanzi_spider'
    allowed_domains = ['haoduanzi.com']
    start_urls = ['http://www.haoduanzi.com/category/?1-1.html']

    def parse(self, response):
        contents = response.xpath("//ul[@class='list-box']/li")
        try:
            for content in contents:
                title = content.xpath(".//div[1]//*[@class='s2']/text()").get()
                article = ''.join(text.strip().replace('\n','') for text in content.xpath(".//div[2]//text()").getall())
                item = HaoduanziItem(title = title,article = article)
                yield item
        except:
            pass
        next_url = response.xpath("//a[@id='next_page']/@href").get()
        if not next_url:
            return
        else:
            yield scrapy.Request(next_url,callback=self.parse)

