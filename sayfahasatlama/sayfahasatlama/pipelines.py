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
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize
from nltk.text import Text
from nltk.tokenize import RegexpTokenizer
from string import punctuation, digits
from TurkishStemmer import TurkishStemmer as tust
import re
import string
from snowballstemmer import TurkishStemmer, stemmer
import pathlib


class SayfahasatPipeline(object):

    def __init__(self):
        SETTINGS = get_project_settings()
        connection = pymongo.MongoClient(
            SETTINGS['MONGODB_SERVER'],
            SETTINGS['MONGODB_PORT'])
        db = connection[SETTINGS['MONGODB_DB']]
        self.collection = db[SETTINGS['MONGODB_COLLECTION']]

    def process_item(self, item, spider):

        raw = str(item["data"])
        tokensayfa2 = word_tokenize(raw, language="turkish", preserve_line=True)
        stopwordss = stopwords.words("turkish")
        ekleme2 = ["“", "xa0", "\n", "\t", "\r", ".", ", ", "[", "]", "?", " ", '"', "'", '``', "''", "’", ","]
        ekleme = list(punctuation)
        stopwordss.extend(ekleme)
        stopwordss.extend(ekleme2)
        tokenstopword = []
        ss = stemmer("turkish")
        ps = tust()
        for t in tokensayfa2:
            if not t in stopwordss:
                s = re.sub(r"\b\d+\b", "", t)
                s = re.sub(r"[']+", "", s)
                s = re.sub(r"[.]+", "", s)
                s = re.sub(r"\\xa0", "", s)
                s1 = re.sub(r"\\r\\n\\t", "", s)
                s2 = ps.stem(s1)
                if len(s2) != 0 and len(s2) != 1 and s2 != ",":
                    tokenstopword.append(s2.lower())

        hashurl = "".join(item["url"])
        hashurl2 = hash(hashurl)
        konupath = pathlib.PurePath(item["url"])
        konu = konupath.parts[3]
        self.collection.insert_one({"url": hashurl2, "target": konu, "data": tokenstopword})
