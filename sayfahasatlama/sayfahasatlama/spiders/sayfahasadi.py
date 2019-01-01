from __future__ import absolute_import
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import Selector
from scrapy.settings import Settings
from scrapy.http import Request


class Sayfahasadı(scrapy.Spider):
    name = "sayfaspider"
    allowed_domains = ["sabah.com.tr", ]
    start_urls = ["https://www.sabah.com.tr/ekonomi/",
                  "https://www.sabah.com.tr/ekonomi/2/", ]


    def parse(self, response):
        altsayfalar = Selector(response).xpath('/html/body/section/div/div[9]/div[3]')
        item = SayfahasatItem()
        itemtemp=[]
        for altsayfa in altsayfalar:

            item["url"] = altsayfa.xpath('/figure/a').extract()
            item["title"] = altsayfa.xpath('/figure/figcaption/a').extract()
            itemtemp.append(item["url"])
        yield item
    #     if itemtemp is not None:
    #         for i in itemtemp:
    #             next_page = response.urljoin(str(i))
    #             yield scrapy.Request(next_page, callback=self.parse_item)
    #
    # def parse_item(self, response):
    #     altsayfalar = Selector(response).xpath('//*[@id="articleBody"]')
    #     item = SayfahasatItem()
    #     for altsayfa in altsayfalar:
    #         item["sayfa"] = altsayfa.xpath('//p//text()').extract()
    #
    #         yield item


if __name__ == "__main__":
    from sayfahasatlama.sayfahasatlama.items import SayfahasatItem
    process = CrawlerProcess(get_project_settings())
    process.crawl(Sayfahasadı)
    process.start()
# else:
#     from sayfahasatlama.items import SayfahasatItem

