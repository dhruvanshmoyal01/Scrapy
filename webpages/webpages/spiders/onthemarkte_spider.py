import scrapy
from scrapy import Selector
from ..items import HouseMarket

class onthemarket_spider(scrapy.Spider):
	name = "onthemarket"
	page_number = 1
	start_urls = [
		'https://www.onthemarket.com/for-sale/property/manchester/?page=0&view=grid'
	]

	def parse(self, response):
		self.log('status: '+str(response.status))
		items = HouseMarket()
		all_houses = response.css("li.result").extract()
		for house in all_houses:
			house = Selector(text = house)
			items['tag'] = house.css('span.exclusive-banner-text::text').extract()
			items['title'] = house.css('div.gradient span.title a::text').extract()
			items['address'] = house.css('div.gradient span.address a::text').extract()
			items['price'] = house.css('div.gradient p.price-text a::text').extract()
			items['description'] = house.css('div.gradient p.description::text').extract()
			items['agent'] = house.css('div.agent p.marketed-by a::text').extract()
			items['contact_number'] = house.css('div.telephone a::text').extract()
			items['img_url'] = house.css('picture img::attr(src)').extract()
			yield items

		next_page = 'https://www.onthemarket.com/for-sale/property/london/?page='+str(onthemarket_spider.page_number)+'&view=grid'
		if onthemarket_spider.page_number <= 42:
			onthemarket_spider.page_number += 1
			yield response.follow(next_page, callback = self.parse)