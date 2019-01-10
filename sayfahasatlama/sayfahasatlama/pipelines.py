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
                for url in item["url2"]:
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
