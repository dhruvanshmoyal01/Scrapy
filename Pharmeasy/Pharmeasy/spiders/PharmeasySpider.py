import scrapy
import json
from pprint import pprint

class PharmeasySpider(scrapy.Spider):
	name = 'pharmeasy'
	page_number = 1
	start_urls = [
		'https://pharmeasy.in/api/otc/getCategoryProducts?categoryId=89&page=0'
	]

	def parse(self, response):
		data = response.text
		data = json.loads(data)
		
		for offer in data['data']['products']:
			product = {
				'product_name' : offer['name'],
				'product_id' : offer['productId'],
				'manufacturer' : offer['manufacturer'],
				'mrp_price' : offer['mrpDecimal'],
				'discountPercent' : offer['discountPercent'],
				'discount' : offer['discountDecimal'],
				'sell_price' : offer['salePriceDecimal'],
				'Availability' : offer['isAvailable'],
				'img_urls' : offer['images']
			}
			#print(json.dumps(product, indent = 2))
			yield product
			next_page = 'https://pharmeasy.in/api/otc/getCategoryProducts?categoryId=89&page='+str(PharmeasySpider.page_number)
			if PharmeasySpider.page_number < 30:
				PharmeasySpider.page_number += 1
				yield response.follow(next_page, callback = self.parse)