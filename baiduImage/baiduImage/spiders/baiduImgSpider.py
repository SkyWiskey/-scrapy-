import json
import re

import scrapy
from urllib.parse import unquote,quote
from baiduImage.items import BaiduimageItem



class BaiduimgspiderSpider(scrapy.Spider):
    name = 'baiduImgSpider'
    allowed_domains = ['image.baidu.com']
    start_urls = []
    for page in range(1,11):
        url = f'https://image.baidu.com/search/acjson?tn=resultjson_com&logid\
        =9819857186307892840&ipn=rj&ct=201326592&is=&fp=result&fr=&word={quote("长腿")}&cg=girl&queryWord={quote("长腿")}&cl=2&lm=-1&ie=utf-8\
        &oe=utf-8&adpicid=&st=-1&z=&ic=0&hd=&latest=&copyright=&s=&se=&tab=&wid\
        th=&height=&face=0&istype=2&qc=&nc=1&expermode=&nojc=&isAsync=&pn={page*30}&rn=\
        30&gsm=5a&1653317376453='
        start_urls.append(url)
    #可以在爬虫文件中指定管道
    # custom_settings = {
    #     'ITME_PIPELINES':{
    #         ''
    #     }
    # }

    def parse(self, response):
        category = unquote(self.start_urls[0].split('queryWord=')[-1].split('&')[0])
        print(category)
        resp = json.loads(response.text)
        links = resp['data']
        image_urls = list()
        for link in links:
            if link:
                image_url = link['thumbURL']
                image_urls.append(image_url)
        yield BaiduimageItem(category=category,image_urls=image_urls)