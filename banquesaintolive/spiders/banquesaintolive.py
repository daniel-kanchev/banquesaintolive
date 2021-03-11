import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst
from datetime import datetime
from banquesaintolive.items import Article


class BanquesaintoliveSpider(scrapy.Spider):
    name = 'banquesaintolive'
    start_urls = ['https://www.banquesaintolive.com/actualites/']

    def parse(self, response):
        links = response.xpath('//div[@class="hover-link"]/a/@href').getall()
        yield from response.follow_all(links, self.parse_article)

    def parse_article(self, response):
        if 'pdf' in response.url:
            return

        item = ItemLoader(Article())
        item.default_output_processor = TakeFirst()

        title = response.xpath('//h2/text()').get()
        if title:
            title = title.strip()

        date = response.xpath('//p[@class="c-new-date"]/text()').get()
        if date:
            date = date.strip()

        content = response.xpath('//div[@class="news-caption"]/p[2]//text()').getall()
        content = [text for text in content if text.strip()]
        content = "\n".join(content).strip()

        item.add_value('title', title)
        item.add_value('date', date)
        item.add_value('link', response.url)
        item.add_value('content', content)

        return item.load_item()
