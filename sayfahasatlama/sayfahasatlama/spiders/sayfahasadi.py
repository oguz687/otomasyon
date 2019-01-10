from __future__ import absolute_import
import scrapy
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy import Selector
from scrapy.settings import Settings
from scrapy.http import Request
from scrapy.crawler import CrawlerRunner
from scrapy.utils.log import configure_logging
import time



class Sayfahasadı(scrapy.Spider):
    from otomasyondb import Veritabani
    name = "sayfaspider"
    allowed_domains = ["trthaber.com/", ]
    start_urls=[]
    print("bu ikinci sinyaldir")
    for sayi in range(1,3):
        start_urls.append("https://www.trthaber.com/haber/ekonomi/%s.sayfa.html" % sayi)

    def parse(self, response):
        altsayfalar = Selector(response).xpath('.//div[@class="katListe2"]')
        for altsayfa in altsayfalar:

            urls = altsayfa.xpath('.//div[@class="row"]//a//@href').extract()
            # item["title"] = altsayfa.xpath('.//div[@class="row"]//a//div[@class="txt"]//@title').extract()

            for url in urls:
                yield response.follow(url,self.parse_switch_page)

    def parse_switch_page(self,response):
        sayfalar = Selector(response).xpath('.//div[@id="trtdty"]')
        item = SayfahasatItem()
        for sayfa in sayfalar:
            item["url2"] = sayfa.xpath(".//p").extract()
            item["sayfa"] = sayfa.xpath(".//p").extract()
            yield item





# class Sayfagiris(scrapy.Spider):
#     from otomasyondb import Veritabani
#     name="sayfagiris"
#     custom_settings = {}
#     allowed_domains = ["trthaber.com/", ]
#     start_urls = []
#     print("bu bir sinyaldir")
#     orn = Veritabani()
#     coll = orn.db.get_collection("sayfalars")
#     sorgu = coll.find({}, {"url": 1, "_id": 0})
#     urllist = sorgu.distinct("url")
#     for url in urllist:
#         print("kırr  ",url)
#         start_urls.append(url)
#     if len(urllist) != 0:
#         custom_setting = {"ITEM_PIPELINES": {"sayfahasatlama.sayfahasatlama.pipelines.SayfagirisPipeline": 100,}
#         }
#         custom_settings.update(custom_setting)
#
#
#     def parse(self, response):
#         sayfalar = Selector(response).xpath('.//div[@class="katListe2"]')
#         item = SayfahasatItem()
#         for sayfa in sayfalar:
#             item["url2"] = sayfa.xpath(".//head").extract()   #//link[@rel='canonical']//@href"
#             item["sayfa"] = sayfa.xpath(".//body").extract()  #div[@class="news-detail-content"]//p//text()
#         yield item


if __name__ == "__main__" :

    from sayfahasatlama.sayfahasatlama.items import SayfahasatItem
    from twisted.internet import reactor
    from twisted.internet.defer import inlineCallbacks

    process = CrawlerProcess(get_project_settings())
    process.crawl(Sayfahasadı)
    # process.crawl(Sayfagiris)
    process.start()

    # configure_logging()
    # runner = CrawlerRunner()
    # @inlineCallbacks
    # def crawl():
    #     yield runner.crawl(Sayfahasadı)
    #     yield runner.crawl(Sayfagiris)
    #     reactor.stop()
    # crawl()
    # reactor.run()


