import scrapy
from ..items import JournalItem
from scrapy import Selector

class JournalSpider(scrapy.Spider):
	name = "journal"
	page_number = 2
	start_urls = [
		"https://www.sciencedirect.com/journal/annals-of-oncology/vol/29/suppl/S7?page=1"
	]

	def parse(self, response):
		items = JournalItem()
		articles = response.css("dl.article-content").extract()
		for article in articles:
			article = Selector(text = article)			
			items['title'] = article.css('.js-article-title::text').extract()
			items['author'] = article.css('.js-article__item__authors::text').extract()
			items['page_range'] = article.css('.js-article-page-range::text').extract()

			yield items

		next_page = "https://www.sciencedirect.com/journal/annals-of-oncology/vol/29/suppl/S7?page="+str(JournalSpider.page_number)+""
		if JournalSpider.page_number <= 3:
			JournalSpider.page_number += 1
			yield response.follow(next_page, callback = self.parse)