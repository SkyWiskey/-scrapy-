import scrapy
import re
from xiaoshuo.items import XiaoshuoItem


class XiaoshuoSpiderSpider(scrapy.Spider):
    name = 'xiaoshuo_spider'
    allowed_domains = ['m.50zw.org']
    start_urls = ['https://m.50zw.org/']

    #小说六大种类
    def parse(self, response):
        type_urls = response.xpath("//div[@class='more']/a/@href").getall()
        for type_url in type_urls:
            url = response.urljoin(type_url)
            yield scrapy.Request(url = url,callback=self.parse_type)
            break

    #分别对每个种类小说解析提取
    def parse_type(self,response):
        novels = response.xpath("//table[@class='list-item']//div[@class='article']/a[1]/@href").getall()
        for novel in novels:
            url = novel.replace('book/','chapters_')
            yield scrapy.Request(url=url,callback=self.parse_novel)

        #小说列表翻页
        next_url = response.xpath("//table[@class='page-book']//td[1]/a/@href").get()
        if next_url:
            yield scrapy.Request(url=response.urljoin(next_url),callback=self.parse_type)

    #解析每个小说的每个章节
    def parse_novel(self,response):
        title_text = response.xpath("//li[@class='title']/h1/text()").get()
        novel_title = re.sub(r'章节目录','',title_text)
        chapter_url = response.xpath("//li[2]/a/@href").get()
        yield scrapy.Request(url=chapter_url,callback=self.parse_chapter,meta={'info':novel_title})

    #获取每个章节的内容
    def parse_chapter(self,response):
        novel_title = response.meta.get('info')
        chapter_title = response.xpath("//h1[@id='nr_title']/text()").get()
        article_text = ''.join(response.xpath("//div[@id='nr1']/text()").getall())
        article = re.sub(r'\s','',article_text)

        item = XiaoshuoItem(
            novel_title = novel_title,chapter_title=chapter_title,article=article
        )
        yield item
        #每个章节翻页
        next_page = response.xpath("//a[@id='pb_next']/@href").get()
        if not next_page:
            return
        yield scrapy.Request(url=response.urljoin(next_page),callback=self.parse_chapter,meta={'info':novel_title})