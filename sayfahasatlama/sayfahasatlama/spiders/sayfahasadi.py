from __future__ import absolute_import
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import Selector
from scrapy.settings import Settings
from scrapy.http import Request
# from twisted.internet import reactor, defer
# from scrapy.crawler import CrawlerRunner
# from scrapy.utils.log import configure_logging

from otomasyondb import Veritabani


class Sayfahasadı(scrapy.Spider):
    name = "sayfaspider"
    allowed_domains = ["ekonomi.haber7.com/turkiye-ekonomisi/", ]
    start_urls=[]
    for sayı in range(2):
        start_urls.append("http://ekonomi.haber7.com/turkiye-ekonomisi/p%s" % sayı)

    def parse(self, response):
        altsayfalar = Selector(response).xpath('//*[@class="infinite-item"]')
        item = SayfahasatItem()
        for altsayfa in altsayfalar:

            item["url"] = altsayfa.xpath('.//a//@href').extract()
            item["title"] = altsayfa.xpath('.//a//div[@class="title"]//text()').extract()
            item["summary"] = altsayfa.xpath('.//a//div[@class="summary"]//text()').extract()

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

class Sayfagiris(scrapy.Spider):
    name="sayfagiris"
    allowed_domains = ["ekonomi.haber7.com/turkiye-ekonomisi/", ]
    start_urls = []
    orn = Veritabani()
    coll = orn.db.get_collection("sayfalars")
    sorgu = coll.find({}, {"url": 1, "_id": 0})
    urllist = sorgu.distinct("url")
    for url in urllist:
        start_urls.append(url)

    def parse(self, response):
        sayfalar = Selector(response).xpath('//div[@class="news-content"]')
        item = SayfahasatItem()
        for sayfa in sayfalar:
            item["sayfa"] = sayfa.xpath('.//p//text()').extract()
        yield item






if __name__ == "__main__" :

    from sayfahasatlama.sayfahasatlama.items import SayfahasatItem
    process = CrawlerProcess(get_project_settings())
    process.crawl(Sayfahasadı)
    process.crawl(Sayfagiris)
    process.start()


    # configure_logging()
    # runner = CrawlerRunner()
    # @defer.inlineCallbacks
    # def crawl():
    #     yield runner.crawl(Sayfahasadı)
    #     yield runner.crawl(Sayfagiris)
    #     reactor.stop()
    # crawl()
    # reactor.run()


