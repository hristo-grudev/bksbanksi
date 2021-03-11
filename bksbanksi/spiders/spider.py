import scrapy

from scrapy.loader import ItemLoader

from ..items import BksbanksiItem
from itemloaders.processors import TakeFirst


class BksbanksiSpider(scrapy.Spider):
	name = 'bksbanksi'
	start_urls = ['https://www.bksbank.si/novice']

	def parse(self, response):
		post_links = response.xpath('//a[contains(@class, "news-item-btn")]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//div[@class="news-pagination"]//a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="content-large"]/h1//text()').getall()
		title = [p.strip() for p in title]
		title = ' '.join(title).strip()
		description = response.xpath('//div[@class="content-large"]/p[position()>1]//text()[normalize-space()]|//div[@class="portlet-boundary portlet-bordered portlet-journal-content"]//text()[normalize-space()]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="content-large"]/p//text()').get()

		item = ItemLoader(item=BksbanksiItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
