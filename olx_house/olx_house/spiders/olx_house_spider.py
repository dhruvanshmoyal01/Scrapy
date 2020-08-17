import scrapy
from pprint import pprint
import json
import csv

class HouseSpider(scrapy.Spider):
	name = 'house_spider'
	page = 1
	start_urls = [ 
		'https://www.olx.in/api/relevance/search?category=1725&facet_limit=100&lang=en&location=1000001&location_facet_limit=20&showAllCars=true&user=1731a5db9dfx3971ff23&page='+str(page-1)
	]

	#def __init__(self):
	#	with open('results.csv', 'a', encoding = 'UTF-8') as csv_file:
	#		csv_file.write('title,description,location,features,data,price\n')
	
	def parse(self, response):
		data = response.text
		data = json.loads(data)

		for offer in data['data']:
			house = {
				'title' : offer['title'],
				'description' : offer['description'].replace('\n', ' '),
				'location' : offer['locations_resolved']['SUBLOCALITY_LEVEL_1_name']+ ' ' +
							 offer['locations_resolved']['ADMIN_LEVEL_3_name']+ ' ' +
							 offer['locations_resolved']['ADMIN_LEVEL_1_name']+ ' '+
							 offer['locations_resolved']['COUNTRY_name'],
				'features' : offer['main_info'],
				'data' : offer['display_date'],
				'price' : offer['price']['value']['display']
			}
			print(json.dumps(house, indent = 2))
			#with open('results.csv', 'a', encoding = 'UTF-8') as csv_file:
			#	writer = csv.DictWriter(csv_file, fieldnames = house.keys())
			#	writer.writerow(house)
			
			#yield house
			
			next_page = 'https://www.olx.in/api/relevance/search?category=1725&facet_limit=100&lang=en&location=1000001&location_facet_limit=20&showAllCars=true&user=1731a5db9dfx3971ff23&page='+str(HouseSpider.page)
			if HouseSpider.page <= 10:
				HouseSpider.page += 1
				yield response.follow(next_page, callback = self.parse)