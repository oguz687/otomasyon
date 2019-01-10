# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html

import pymongo
from scrapy.crawler import Settings
# from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy.utils.project import get_project_settings
from otomasyondb import Veritabani
from nltk.tokenize import word_tokenize


class SayfahasatPipeline(object):

    def __init__(self):
        SETTINGS = get_project_settings()
        connection = pymongo.MongoClient(
            SETTINGS['MONGODB_SERVER'],
            SETTINGS['MONGODB_PORT']
        )
        db = connection[SETTINGS['MONGODB_DB']]
        self.collection = db[SETTINGS['MONGODB_COLLECTION'][0]]

    def process_item(self, item, spider):
        orn = Veritabani()
        coll = orn.db.get_collection("sayfalars")
        sorgu = coll.find({}, {"url": 1, "_id": 0})
        urllist = sorgu.distinct("url")
        with open("dosya.txt","w+") as ds:
            for i in urllist:
                ds.write(i)
                ds.write("\n")
        self.valid1 = True
        if spider.name == "sayfaspider":
            for data in item:
                if not data:
                    self.valid1 = False
                    raise DropItem("Missing {0}!".format(data))
            if self.valid1:
                for url in item["url"]:
                    if not url in urllist:
                        try:
                            self.collection.insert_one(item)
                            return item
                        except Exception:
                            print(url, "      :bu sayfa var")
                    else:
                        print(url, " listede var")
        else:
            raise DropItem("KAYIP ITEM")


class SayfagirisPipeline(object):    # bu class anasayfalardan toplanan urllerin içine girer
                                     # ve tek tek okuyup veritabanına gönderir
    def __init__(self):
        SETTINGS = get_project_settings()
        connection = pymongo.MongoClient(
            SETTINGS['MONGODB_SERVER'],
            SETTINGS['MONGODB_PORT']
        )
        db = connection[SETTINGS['MONGODB_DB']]
        self.collection = db[SETTINGS['MONGODB_COLLECTION'][1]]

    def process_item(self, item, spider):
        orn2 = Veritabani()
        coll = orn2.db.get_collection("sayfalar111")
        sorgu = coll.find({}, {"url": 1, "_id": 0,"sayfa":0})
        urllist = sorgu.distinct("sayfa")
        with open("dosyae.txt","w+") as ds:
            for i in urllist:
                ds.write(urllist.count())
                ds.write("\n")
        with open("dosya3.txt", "w+") as ds:
            for i in urllist:
                ds.write(i)
                ds.write("\n")
        self.valid = True
        if spider.name =="sayfagiris":
            for data in item:
                if not data:
                    self.valid = False
                    raise DropItem("Missing {0}!".format(data))
            if self.valid:
                for url in item["url"]:
                    if url not in urllist:
                        try:
                            token=word_tokenize(item)
                            self.collection.insert_one(item)
                            return item
                        except Exception:
                            print(url, "      :bu daha önce eklendi")
                    else:
                        print(url, "  daha önce listelendi")
        else:
            raise DropItem("kayıp item")