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
        self.valid1 = True
        if spider.name == "sayfaspider":
            for data in item:
                if not data:
                    self.valid1 = False
                    raise DropItem("Missing {0}!".format(data))
            if self.valid1:
                self.collection.create_index([("sayfalar",pymongo.GEO2D)], unique=True)
                self.collection.insert_one(item)
                return item
        else:
            raise DropItem("KAYIP ITEM")


class SayfagirisPipeline(object):

    def __init__(self):
        SETTINGS = get_project_settings()
        connection = pymongo.MongoClient(
            SETTINGS['MONGODB_SERVER'],
            SETTINGS['MONGODB_PORT']
        )
        db = connection[SETTINGS['MONGODB_DB']]
        self.collection = db[SETTINGS['MONGODB_COLLECTION'][1]]

    def process_item(self, item, spider):
        self.valid = True
        if spider.name =="sayfagiris":
            for data in item:
                if not data:
                    self.valid = False
                    raise DropItem("Missing {0}!".format(data))
            if self.valid:
                self.collection.insert_one(dict(item))
                return item
        else:
            raise DropItem("kayıp item")