# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HaoduanziItem(scrapy.Item):
    title = scrapy.Field()
    article = scrapy.Field()
