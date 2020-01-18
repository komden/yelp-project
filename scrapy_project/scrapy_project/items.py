# -*- coding: utf-8 -*-

import scrapy

class MyItem(scrapy.Item):
    name = scrapy.Field()
    address_all = scrapy.Field()
    address_all_span = scrapy.Field()
    sity = scrapy.Field()
    country = scrapy.Field()
    index = scrapy.Field()
    phone = scrapy.Field()
    countreview = scrapy.Field()
    website = scrapy.Field()
    schedule = scrapy.Field()
    array_attib = scrapy.Field()
    category = scrapy.Field()
    rannge = scrapy.Field()
    #image_names = scrapy.Field()
    image_urls = scrapy.Field()
    image_paths = scrapy.Field()
    count_item = scrapy.Field()
    path_to_files = scrapy.Field()
    name_dir = scrapy.Field()
    #pass
