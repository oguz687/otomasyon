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
    allowed_domains = ["internethaber.com/ekonomi", ]
    start_urls=[]
    for sayi in range(1,10):
        start_urls.append("http://www.internethaber.com/ekonomi?page=%s" % sayi)

    def parse(self, response):
        altsayfalar = Selector(response).xpath('//div[@class="wrap ctgry"]')
        item = SayfahasatItem()
        for altsayfa in altsayfalar:

            item["url"] = altsayfa.xpath('.//ul[@class="list"]//li/a[1]//@href').extract()
            item["title"] = altsayfa.xpath('.//ul[@class="list"]//li/a[1]//@title').extract()

            yield item


class Sayfagiris(scrapy.Spider):
    name="sayfagiris"
    custom_settings={}
    allowed_domains = ["internethaber.com/ekonomi/", ]
    start_urls = []
    orn = Veritabani()
    coll = orn.db.get_collection("sayfalars")
    sorgu = coll.find({}, {"url": 1, "_id": 0})
    urllist = sorgu.distinct("url")
    for url in urllist:
        start_urls.append(url)
    if len(urllist) != 0:
        custom_setting = {"ITEM_PIPELINES": {'sayfahasatlama.sayfahasatlama.pipelines.SayfagirisPipeline': 100,}
        }
        custom_settings.update(custom_setting)


    def parse(self, response):
        sayfalar = Selector(response).xpath('/html')
        item = SayfahasatItem()
        for sayfa in sayfalar:
            item["url"] = sayfa.xpath("/head//link[@rel='canonical']")
            item["sayfa"] = sayfa.xpath('//div[@class="time"]//div[@class="news-detail-content"]//p//text()').extract()
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


