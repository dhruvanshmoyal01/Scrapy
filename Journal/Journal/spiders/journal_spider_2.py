import scrapy
from ..items import JournalItem
from scrapy import Selector

class JournalSpider(scrapy.Spider):
	name = "journal2"
	page_number = 2
	start_urls = [
		"https://www.thegreenjournal.com/issue/S0167-8140(15)X0003-X?page=1"
	]

	def parse(self, response):
		items = JournalItem()
		articles = response.css(".article-details").extract()
		for article in articles:
			article = Selector(text = article)
			items['title'] = article.css(".title a::text").extract()
			items['author'] = article.css('.authors::text').extract()
			items['published_in'] = article.css('.published-online::text').extract()
			yield items

		next_page = "https://www.thegreenjournal.com/issue/S0167-8140(15)X0003-X?page="+str(JournalSpider.page_number)+""
		if JournalSpider.page_number <= 34:
			JournalSpider.page_number += 1
			yield response.follow(next_page, callback = self.parse)