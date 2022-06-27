# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class JianshuItem(scrapy.Item):
    _id = scrapy.Field()
    title = scrapy.Field()
    author = scrapy.Field()
    pub_date = scrapy.Field()
    words = scrapy.Field()
    read_count = scrapy.Field()
    like_count = scrapy.Field()
    article = scrapy.Field()
    srcs = scrapy.Field()
