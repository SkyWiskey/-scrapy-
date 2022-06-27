import scrapy
from scrapy.spiders import CrawlSpider,Rule
from scrapy.linkextractors import LinkExtractor

from wxappUnion.items import WxappunionItem


class MyspiderSpider(CrawlSpider):
    name = 'mySpider'
    allowed_domains = ['wxapp-union.com']
    start_urls = ['https://www.wxapp-union.com/portal.php?mod=list&catid=2&page=1']

    rules = (
        Rule(LinkExtractor(allow=r'.+mod=list&catid=2&page=\d{1,}'),follow=True),
        Rule(LinkExtractor(allow=r'.+article-.+\.html'),callback='parse_item',follow=False),
    )
    def parse_item(self, response):
        _id = response.request.url.split('-')[-2]
        title = response.xpath("//h1/text()").get()
        author = response.xpath("//p[@class='authors']/a/text()").get()
        pub_date = response.xpath("//p[@class='authors']/span/text()").get()
        focus_num = response.xpath("//div[@class='focus_num cl']/a/text()").get()
        block_quote = response.xpath("//div[@class='blockquote']//text()").get()
        articles = response.xpath("//td[@id='article_content']//text()").getall()
        article = ''.join(text.strip() for text in articles )
        yield WxappunionItem(
            _id=_id,title=title,author=author,pub_date=pub_date,
            focus_num=focus_num,block_quote=block_quote,article=article
        )
