import scrapy
from news_163.items import News163Item

class NewsSpiderSpider(scrapy.Spider):
    name = 'news_spider'
    # allowed_domains = ['news.163.com/']
    start_urls = ['https://news.163.com/']

    def __init__(self):
        super(NewsSpiderSpider, self).__init__()
        self.module_urls = list()

    def parse(self, response):
        nv_list = response.xpath("//div[@class='ns_area list']/ul/li")
        for i in [1,2,4,5]:
            category = nv_list[i].xpath(".//a/text()").get()
            href = nv_list[i].xpath(".//a/@href").get()
            self.module_urls.append(href)
            yield scrapy.Request(url=href,callback=self.parse_module,
                                 meta={'info':category})

    # 解析分类
    def parse_module(self,response):
        category = response.meta.get('info')
        div_list = response.xpath("//div[@class='ndi_main']/div")
        for div in div_list:
            try:
                title = div.xpath(".//div[@class='news_title']/h3/a/text()").get()
                href = div.xpath(".//div[@class='news_title']/h3/a/@href").get()
                tags = tuple(div.xpath(".//div[@class='news_tag']//a/text()").getall())
                yield scrapy.Request(url=href,callback=self.parse_detail,meta={
                    'info':(category,title,tags)
                })
            except:
                pass

    # 解析每个分类下的每篇文章
    def parse_detail(self,response):
        category,title,tags = response.meta.get('info')
        url = response.request.url
        _id = url.split('/')[-1].split('.')[0]
        if  response.xpath("//div[@class='post_info']/text()[1]").get()  != None:
            date = response.xpath("//div[@class='post_info']/text()[1]").get().strip().replace('来源:','')
        else:
            date = None
        if response.xpath("//div[@class='post_info']/a[1]/text()").get() != None:
            from_where = response.xpath("//div[@class='post_info']/a[1]/text()").get().strip()
        else:
            from_where = None
        articles = ''
        src_list = list()
        p_list =  response.xpath("//div[@class='post_body']//p")
        for p in p_list:
            if len(p.xpath(".//img")) > 0:
                src = p.xpath(".//img/@src").get()
                src_list.append(src)
            if len(p.xpath(".//style")) > 0:
                pass
            else:
                articles += ''.join(p.xpath(".//text()").getall()).strip() + '\n'
        item = News163Item(
            _id = _id,
            category=category,title=title,tags=str(tags),pTime=date,from_where=from_where,
            article=articles,src_list=str(src_list),origin_url=url
        )
        yield item