# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class News163Item(scrapy.Item):
    _id = scrapy.Field()
    category = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()
    pTime = scrapy.Field()
    from_where = scrapy.Field()
    src_list = scrapy.Field()
    article = scrapy.Field()
    origin_url = scrapy.Field()
