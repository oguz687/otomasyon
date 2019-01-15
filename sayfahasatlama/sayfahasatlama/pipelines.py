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
from nltk.tokenize import word_tokenize,sent_tokenize
from nltk.corpus import stopwords
from nltk import wordpunct_tokenize
from nltk.text import Text
from nltk.tokenize import RegexpTokenizer
from string import punctuation,digits
import re
import string
from snowballstemmer import TurkishStemmer,stemmer
class SayfahasatPipeline(object):

    def __init__(self):
        SETTINGS = get_project_settings()
        connection = pymongo.MongoClient(
            SETTINGS['MONGODB_SERVER'],
            SETTINGS['MONGODB_PORT']
        )
        db = connection[SETTINGS['MONGODB_DB']]
        self.collection = db[SETTINGS['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        orn = Veritabani()
        urllist=[]
        coll = orn.db.get_collection("sayfalars")
        sorgu = coll.find({}, {"url": 1, "_id": 0})
        urllist = sorgu.distinct("url")
        with open("dosya.txt","w+") as ds:
            for i in urllist:
                ds.write(str(i))
                ds.write("\n")
        # tokenizer = RegexpTokenizer(r'\w+')
        # tokensayfa=tokenizer.tokenize(tokensayfa2)
        # tokens = wordpunct_tokenize()
        # text = Text(tokens)
        # words = [w.lower() for w in text if w.isalpha()]
        # t = str.maketrans("\r\n\t","   ")
        raw=str(item["sayfa"])
        # s = raw.translate(t)
        # expandraw=s.expandtabs()
        # escapes = ''.join([chr(char) for char in range(1, 32)])
        # rawtext = expandraw.translate(escapes)
        tokensayfa2 = word_tokenize(raw,language="turkish",preserve_line=True)
        stopwordss= stopwords.words("turkish")
        ekleme2=["“","xa0","\n","\t","\r",".",", ","[","]","?"," ",'"',"'",'``',"''","’",","]
        ekleme=list(punctuation)
        stopwordss.extend(ekleme)
        stopwordss.extend(ekleme2)
        tokenstopword=[]
        ps = TurkishStemmer()
        ss = stemmer("turkish")

        for t in tokensayfa2:
            if not t in stopwordss:
                s= re.sub(r"\b\d+\b","", t)
                s1 = re.sub(r"\\r\\n\\t","", s)
                # s=' '.join(t.split())
                # y=t.maketrans("\r\n\t", "   ")
                # s=t.translate(y)
                # s=t.rstrip("\r")
                # s=re.sub(r'\r\n', '', str(t))
                # regex = re.compile(r"['\r']")
                # s = regex.sub(,"", str(t))
                # s1=ps.stemWord(s)
                # s=t.replace("[\r\n\t]","")
                s2 = ss.stemWord(s1)
                if len(s1) != 0 and s1 != ",":
                    tokenstopword.append(s1.lower())


        hashurl="".join(item["url"])
        hashurl2=hash(hashurl)
        self.collection.insert_one({"url": hashurl2, "sayfa": tokenstopword})
        # self.valid1 = True

        # for data in item:
        #     if not data:
        #         self.valid1 = False
        #         raise DropItem("Missing {0}!".format(data))
        # if self.valid1==True:
        #     for url in item["url"]:
        #         if not url in urllist:
        #             try:
        #                 tokensayfa=word_tokenize(item["sayfa"])
        #                 hashurl=hash(str(item["url"]))
        #                 self.collection.insert_one({tokensayfa: hashurl})
        #                 return item
        #             except Exception:
        #                 print(url, "      :bu sayfa var")
        #         else:
        #             print(url, " listede var")

