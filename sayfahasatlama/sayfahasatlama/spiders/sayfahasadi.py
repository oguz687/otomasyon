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
    allowed_domains = ["trthaber.com/"]
    print("bu ikinci sinyaldir")
    start_urls = []
    for sayi in range(1, 2):
        start_urls.append("https://www.trthaber.com/haber/ekonomi/%s.sayfa.html" % sayi, )

    def parse(self, response):
        altsayfalar = Selector(response).xpath('.//div[@class="katListe2"]')
        urllist = []
        for altsayfa in altsayfalar:
            urls = altsayfa.xpath('.//div[@class="row"]//a//@href').extract()
            urllist.extend(urls)
        for url2 in urllist:
            url = "https://www.trthaber.com/" + url2
            print(url)
            yield response.follow(url, callback=self.parse_switch_page, dont_filter=True, meta={"item": url})

    def parse_switch_page(self, response):
        sayfalar = Selector(response).xpath('.//div[@id="trtdty"]')
        item = SayfahasatItem()
        for sayfa in sayfalar:
            item["url"] = response.meta["item"]
            item["sayfa"] = sayfa.xpath(".//p//text()[normalize-space()]").extract()
            yield item


if __name__ == "__main__":
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
