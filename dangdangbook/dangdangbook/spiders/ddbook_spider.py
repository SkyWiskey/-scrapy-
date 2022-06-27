import scrapy
from dangdangbook.items import DangdangbookItem


class DdbookSpiderSpider(scrapy.Spider):
    name = 'ddbook_spider'
    allowed_domains = ['book.dangdang.com']
    start_urls = ['http://book.dangdang.com/']

    def parse(self, response):
        book_lis = response.xpath("//div[@class='sub']/ul/li")
        for li in book_lis[3:-2]:
            category = li.xpath(".//a/text()").get()
            link = li.xpath(".//a/@href").get()
            yield scrapy.Request(url=link,callback=self.parse_category,meta={'info':category})


    def parse_category(self,response):
        category = response.meta.get('info')
        details = response.xpath("//dl[@class='primary_dl']//a")
        for d in details:
            title = d.xpath(".//@title").get()
            href_text = d.xpath(".//@href").get()
            end = href_text.find("#")
            href = href_text[:end]
            yield scrapy.Request(url=href,callback=self.parse_title,dont_filter=True,meta = {'info':(category,title)})


    def parse_title(self,response):
        category,title = response.meta.get('info')
        book_lis = response.xpath("//ul[@class='bigimg']/li")
        for li in book_lis:
            try:
                book_name = li.xpath(".//a/@title").get().strip()
                book_price = li.xpath(".//p[@class='price']/span[@class='search_now_price']/text()").get().strip()
                book_author = ''.join(li.xpath(".//p[@class='search_book_author']/span[1]//text()").getall()).strip()
                pub_time = li.xpath(".//p[@class='search_book_author']/span[2]//text()").get().replace('/','').strip()
                book_press = li.xpath(".//p[@class='search_book_author']/span[3]/a/text()").get().strip()
                book_comment_count = li.xpath(".//a[@class='search_comment_num']/text()").get().strip()
                book_intro = li.xpath(".//p[@class='detail']/text()").get()
                yield DangdangbookItem(category = category,title = title,
                                       book_name = book_name,book_price = book_price,
                                       book_author = book_author,pub_time = pub_time,
                                       book_press = book_press,book_comment_count = book_comment_count,
                                       book_intro = book_intro)
            except:
                pass


        next_url = response.xpath("//li[@class='next']/a/@href").get()
        if next_url:
            yield scrapy.Request(url = response.urljoin(next_url),callback=self.parse_title,
                                 dont_filter=True,meta={'info':(category,title)})