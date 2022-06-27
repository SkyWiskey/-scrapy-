import re
import scrapy
from douban_book.items import DoubanBookItem

class DoubanSpiderSpider(scrapy.Spider):
    name = 'douban_spider'
    allowed_domains = ['book.douban.com']
    start_urls = ['https://book.douban.com/tag/?view=type']

    def parse(self,response):
        categorys = response.xpath("//div[@class='article']/div[2]/div")
        book_type = None
        for category in categorys:
            category_name = category.xpath(".//a/@name").get().strip()
            if category_name:
                book_type = category_name
            book_tds = category.xpath(".//table/tbody/tr/td")
            for book_td in book_tds:
                type_name = book_td.xpath(".//a/text()").get()
                type_link = book_td.xpath(".//a/@href").get()
                type_link = response.urljoin(type_link)
                yield scrapy.Request(url=type_link,callback=self.parse_book_type,
                                     meta={'info':(book_type,type_name)})
                break
            # break

    def parse_book_type(self,response):
        book_type,type_name = response.meta.get('info')
        book_lis = response.xpath("//li[@class='subject-item']")
        for book in book_lis:
            title = book.xpath(".//h2/a/@title").get()
            score = book.xpath(".//span[@class='rating_nums']/text()").get()
            com_count_text = book.xpath(".//span[@class='pl']/text()").get()
            com_count = re.sub(r'\s', '', com_count_text)
            info_texts = book.xpath(".//div[@class='pub']/text()").get()
            infos = re.sub(r'\s', '', info_texts)
            intro_text = book.xpath(".//div[@class='info']/p/text()").get()
            intro = re.sub(r'\s','',intro_text)
            detail_url = book.xpath(".//h2/a/@href").get()
            item = DoubanBookItem(
                book_type = book_type,type_name = type_name,
                title = title,score = score,com_count = com_count,infos = infos,
                intro = intro,detail_url = detail_url
            )
            yield item

        next_url = response.xpath("//span[@class='next']/a/@href").get()
        if not next_url:
            return
        yield scrapy.Request(url = response.urljoin(next_url),callback=self.parse_book_type
                             ,meta={'info':(book_type,type_name)})