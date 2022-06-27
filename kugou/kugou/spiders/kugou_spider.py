import re
import time
import json
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from kugou.items import KugouItem


class KugouSpiderSpider(CrawlSpider):
    name = 'kugou_spider'
    allowed_domains = ['kugou.com']
    start_urls = ['https://www.kugou.com/yy/rank/home/1-6666.html?from=rank']

    rules = (
        Rule(LinkExtractor(allow=r'.+/yy/rank/home/.+\?from=rank'), callback='parse_item', follow=True),
    )

    def parse_item(self, response):
        title = response.xpath("//div[@id='pc_temp_title']/h3/text()").get()
        re_hash = re.compile('"Hash":"(.*?)"', re.S | re.I)
        re_album_id = re.compile('"album_id":(\d+)', re.S | re.I)
        hashs = re_hash.findall(response.text)
        album_ids = re_album_id.findall(response.text)
        for hash_, album_id in zip(hashs, album_ids):
            detail_url = 'https://wwwapi.kugou.com/yy/index.php?'
            params = f'r=play/getdata&callback=jQuery191047607680768471194_1644064048672&hash={hash_}&dfid=3Mnjyo0Eq2HS1Ep23j0Bh6Gp&appid=1014&mid=1861a2e009fc7db9c76b10f5c4695c7b&platid=4&album_id={album_id}&_={int(time.time()*1000)}'
            url = detail_url + params
            yield scrapy.Request(url=url,callback=self.parse_detail,meta={'info':title})

    def parse_detail(self,response):
        try:
            title = response.meta.get('info')
            start = response.text.find('{"status"')
            song_data = json.loads(response.text[start:-2])['data']
            song_url = song_data['play_url']
            song_name = song_data['song_name']
            yield KugouItem(title = title,song_name = song_name,file_urls = [song_url])
        except:
            pass