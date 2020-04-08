# -*- coding: utf-8 -*-
#
# Author: Thamme Gowda [tg (at) isi (dot) edu]
# Created: 4/7/20

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class MTDataItem(scrapy.Item):

    # define the fields for your item here like:
    # name = scrapy.Field()
    id = Field()
    name = Field()
    url = Field()
    langs = Field()
    title = Field()
    info = Field()

class MTCorpusItem(scrapy.Item):
    url = Field()
    name = Field()
    langs = Field()

