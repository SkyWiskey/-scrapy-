import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import  LinkExtractor

from jianshu.items import JianshuItem
class MyspiderSpider(CrawlSpider):
    name = 'mySpider'
    allowed_domains = ['jianshu.com']
    start_urls = ['https://www.jianshu.com/']

    rules = (
        Rule(LinkExtractor(allow=r'.+/p/[0-9a-z]{12}'),callback='parse_item',follow=True),
    )

    def parse_item(self, response):
        _id = response.request.url.split('/')[-1]
        title = response.xpath("//h1[@class='_1RuRku']/text()").get()
        author = response.xpath("//div[@class='_3U4Smb']//a[@class='_1OhGeD']/text()").get()
        pub_date = response.xpath("//div[@class='s-dsoj']/time/text()").get()
        words = response.xpath("//div[@class='s-dsoj']/span[2]/text()").get()
        read_count = response.xpath("//div[@class='s-dsoj']/span[3]/text()").get()
        like_count = response.xpath("//span[@class='_1LOh_5']/text()").get()[:-3]
        article = ''.join(response.xpath("//article/p/text()").getall())
        src_list = [response.urljoin(src) for src in response.xpath("//article/div//img/@data-original-src").getall()]
        srcs = tuple(src_list) if src_list else None

        yield JianshuItem(
            _id=_id,title=title,author=author,pub_date=pub_date,
            words=words,read_count=read_count,like_count=like_count,
            article=article,srcs=srcs
        )
