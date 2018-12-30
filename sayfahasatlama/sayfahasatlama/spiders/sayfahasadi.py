from __future__ import absolute_import
import scrapy
from scrapy.crawler import CrawlerProcess
from sayfahasatlama.sayfahasatlama.items import SayfahasatItem
from scrapy import Selector

class Sayfahasadı(scrapy.Spider):
    name = "sayfaspider"
    allowed_domains = ["stackoverflow.com"]

    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest"
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="summary"]/h3')

        for question in questions:
            item = SayfahasatItem()
            item["title"] = question.xpath('a[@class="question-hyperlink"]/text()').extract()[0]
            item["url"] = question.xpath('a[@class="question-hyperlink"]/@href').extract()[0]
            yield item


if __name__ == "__main__":
    process = CrawlerProcess({'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'})
    process.crawl(Sayfahasadı)
    process.start()

