import re

import scrapy

from shicimingju.items import ShicimingjuItem


class MyspiderSpider(scrapy.Spider):
    name = 'mySpider'
    allowed_domains = ['shicimingju.com']
    start_urls = []
    for page in range(1,653):
        url = f'https://www.shicimingju.com/category/all_{page}'
        start_urls.append(url)

    # 获取每个诗人名称 以及url
    def parse(self, response):
        poet_info = response.xpath("//h3/a")
        for info in poet_info:
            poet_name = info.xpath("./text()").get()
            poet_url = info.xpath("./@href").get()
            yield scrapy.Request(
                url=response.urljoin(poet_url),callback=self.parse_poet,meta={'info':poet_name}
            )

    # 解析每个诗人的所有诗词
    def parse_poet(self,response):
        poet = response.meta.get('info')
        poem_infos = response.xpath("//div[@class='shici_list_main']")
        for info in poem_infos:
            poem_id = info.xpath(".//h3/a/@href").get().split('/')[-1].split('.')[0]
            poem_title = info.xpath(".//h3/a/text()").get()
            poem_text = ''.join(info.xpath("div//text()").getall())
            poem_re = re.sub(r'\s','',poem_text).replace('展开全文','').replace('收起','')
            poem = poem_re.replace('其一','其一：').replace('其二','其二：')
            yield ShicimingjuItem(
                _id=poem_id,poet=poet,poem_title=poem_title,poem=poem
            )
        next_url = response.xpath("//div[@id='list_nav_part']/a[last()-1]/@href").get()
        yield scrapy.Request(
            url=response.urljoin(next_url),callback=self.parse_poet,meta={'info':poet}
        )
