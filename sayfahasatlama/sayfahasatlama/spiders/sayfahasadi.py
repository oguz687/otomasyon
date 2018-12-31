from __future__ import absolute_import
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import Selector
from scrapy.settings import Settings
from scrapy.http import Request


class Sayfahasadı(scrapy.Spider):
    name = "sayfaspider"
    allowed_domains = ["milliyet.com.tr"]
    start_urls = ["http://www.milliyet.com.tr/ekonomi/",]


    def parse(self, response):
        altsayfalar = Selector(response).xpath('//*[@id="_MiddleLeft1"]/div[4]/ul')
        item = SayfahasatItem()
        for altsayfa in altsayfalar:

            item["url"] = altsayfa.xpath('//li//a[@class="nHPhoto"]//@href').extract()
            item["title"] = altsayfa.xpath('//li//a[@class="nHText"]//p/text()').extract()
            yield item


if __name__ == "__main__":
    from sayfahasatlama.sayfahasatlama.items import SayfahasatItem
    process = CrawlerProcess(get_project_settings())
    process.crawl(Sayfahasadı)
    process.start()
# else:
#     from sayfahasatlama.items import SayfahasatItem

