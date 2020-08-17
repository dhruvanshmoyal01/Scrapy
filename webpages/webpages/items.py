# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class WebpagesItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class HouseMarket(scrapy.Item):
	tag = scrapy.Field()
	title = scrapy.Field()
	price = scrapy.Field()
	address = scrapy.Field()
	description = scrapy.Field()
	agent = scrapy.Field()
	contact_number = scrapy.Field()
	img_url = scrapy.Field()