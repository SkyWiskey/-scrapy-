# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ScwzItem(scrapy.Item):
    href = scrapy.Field()
    title = scrapy.Field()
    reply_time = scrapy.Field()
    article = scrapy.Field()
