# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.item import Item, Field


class SayfahasatItem(Item):
    # _id = Field()
    title = Field()
    url = Field()
    summary = Field()
    sayfa = Field()

