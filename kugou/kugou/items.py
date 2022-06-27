# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class KugouItem(scrapy.Item):
    title = scrapy.Field()
    song_name = scrapy.Field()
    song_url = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()