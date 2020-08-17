import scrapy
import json
import requests
import string

class UrbanDictSpider(scrapy.Spider):
	name = 'urban_dictionary'
	url = 'https://www.urbandictionary.com/popular.php?character='

	def start_requests(self):
		with open('urban_dictionary_data.json', 'w') as f:
			f.write('')
		for letter in string.ascii_uppercase:
			next_page = self.url + letter
			yield scrapy.Request(url = next_page, callback = self.parse)	
			#comment to scrape entire dictionary
			break

	def parse(self, response):
		all_words = response.css('li.word') 
		links = []
		for item in all_words:
			word = item.css('a::text').get()
			short_desc = requests.get('https://api.urbandictionary.com/v0/tooltip?term='+word+
								'&key=ab71d33b15d36506acf1e379b0ed07ee').json()['string'].replace('\n',' ').replace('<b>','').replace('</b>','').replace('\r','')
			links.append({
				'word' : word, 
				'short_desc' : short_desc,
				'link': item.css('a::attr(href)').get()
			})
			
		for link in links:
			yield response.follow(url = link['link'], meta = {
													'word' : link['word'],
													'short_desc' : link['short_desc']
													}, 
													callback = self.parse_link)
			
	def parse_link(self, response):
		word = response.meta.get('word')
		short_desc = response.meta.get('short_desc')
		top_def = response.css('div.def-panel')[0]
		word_data = {
			'word': word,
			'short_desc': short_desc,
			'meaning' : ''.join(top_def.css('div.meaning *::text').extract()),
			'example' : ''.join(top_def.css('div.example *::text').extract()),
			'contributor' : top_def.css('div.contributor a::text').get()
		}
		with open('urban_dictionary_data.json', 'a') as f:
			f.write(json.dumps(word_data, indent = 2) + '\n')