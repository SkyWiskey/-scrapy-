import re

import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

from scwz.items import ScwzItem


class ScwnspiderSpider(CrawlSpider):
    name = 'scwnSpider'
    allowed_domains = ['ly.scol.com.cn']
    start_urls = ['https://ly.scol.com.cn/welcome/showlist?keystr=wzrd&total=4959&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+keystr=wzrd&total=\d+&page=\d{1,}'),follow=True),
        Rule(LinkExtractor(allow=r'.+tid=\d+'),callback='parse_item',follow=False)
    )
    def parse_item(self, response):
        href = response.request.url
        title = ''.join(t.strip() for t in response.xpath("//h2[@class='clearfix']/text()").getall())
        reply_time_text = response.xpath("//h2[@class='clearfix']/i/text()").get().strip()
        reply_time = ' '.join(re.sub(r'\s',';',reply_time_text).split(';')[2:4])
        article = ''.join(t.strip() for t in response.xpath("//div[@class='c1']/p[position()>1]/text()").getall())
        print(title,reply_time,article)
        print('='*20)
        yield ScwzItem(href=href,title=title,reply_time=reply_time,article=article)

