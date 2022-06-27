import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from qichezhijia.items import QichezhijiaItem

class QichezhijiaSpiderSpider(CrawlSpider):
    name = 'qichezhijia_spider'
    allowed_domains = ['car.autohome.com.cn']
    start_urls = ['https://car.autohome.com.cn/pic/series/18.html']

    rules = (
        Rule(LinkExtractor(allow=r'https://car.autohome.com.cn/pic/series/18.+'),
             callback='parse_page', follow=True),
    )

    def parse_page(self, response):
        category = response.xpath("//div[@class='uibox']//div[@class='uibox-title']/text()").get()
        srcs = response.xpath("//div[@class='uibox']//div[2]/ul/li/a/img/@src").getall()
        srcs = list(map(lambda x:x.replace("480x360_0_q95_c42_autohomecar__",''),srcs))
        src_list = list(map(lambda x:response.urljoin(x),srcs))
        yield QichezhijiaItem(category = category,image_urls = src_list)

    def parse_image(self,response):
        pass