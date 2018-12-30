from __future__ import absolute_import
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import Selector
from scrapy.settings import Settings


class Sayfahasadı(scrapy.Spider):
    name = "sayfaspider"
    allowed_domains = ["stackoverflow.com"]
    start_urls = [
        "http://stackoverflow.com/questions?pagesize=50&sort=newest"
    ]

    def parse(self, response):
        questions = Selector(response).xpath('//div[@class="summary"]/h3')
        with open("dosya.txt","w+") as ds:
            ds.write(str(response.css("title")))
            ds.write("\n")
        for question in questions:
            item = SayfahasatItem()
            item["title"] = question.xpath('a[@class="question-hyperlink"]/text()').extract()[0]
            item["url"] = question.xpath('a[@class="question-hyperlink"]/@href').extract()[0]

            yield item


if __name__ == "__main__":
    from sayfahasatlama.sayfahasatlama.items import SayfahasatItem
    process = CrawlerProcess(get_project_settings())
    process.crawl(Sayfahasadı)
    process.start()
else:
    from sayfahasatlama.items import SayfahasatItem

