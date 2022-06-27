# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class XiaoshuoItem(scrapy.Item):
    novel_title = scrapy.Field()
    chapter_title = scrapy.Field()
    article = scrapy.Field()
