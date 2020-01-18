# -*- coding: utf-8 -*-

import scrapy
from scrapy.pipelines.images import ImagesPipeline
from scrapy.utils.project import get_project_settings
import hashlib
from scrapy.utils.python import to_bytes
from sqlalchemy.orm import sessionmaker
from scrapy_project.models import MyDB, db_connect, create_table
import datetime

class MyMysqlPipeline(object):

    def __init__(self):
        engine = db_connect()
        create_table(engine)
        self.Session = sessionmaker(bind=engine)

    def process_item(self, item, spider):
        session = self.Session()

        s_name = session.query(MyDB).filter(MyDB.name==item["name"]).filter(MyDB.address_all==item["address_all"]).first()
        if s_name is not None:
            try:
                s_name.phone = item["phone"]
                s_name.countreview = item["countreview"]
                s_name.website = item["website"]
                s_name.category = item["category"]
                s_name.rannge = item["rannge"]
                s_name.path_to_files = item["path_to_files"]
                s_name.schedule = item["schedule"]
                s_name.array_attib = item["array_attib"]
                s_name.datetime = datetime.datetime.now()
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()
        else :
            mydb = MyDB(name='', address_all='', address_all_span='', sity='', country='', index=0, phone='', countreview=0, website='', category='', rannge=0, path_to_files='', schedule='', array_attib='', datetime='')
            mydb.name = item["name"]
            mydb.address_all = item["address_all"]
            mydb.address_all_span = item["address_all_span"]
            mydb.sity = item["sity"]
            mydb.country = item["country"]
            mydb.index = int(item["index"])
            mydb.phone = item["phone"]
            mydb.countreview = int(item["countreview"])
            mydb.website = item["website"]
            mydb.category = item["category"]
            mydb.rannge = float(item["rannge"])
            mydb.path_to_files = item["path_to_files"]
            mydb.schedule = item["schedule"]
            mydb.array_attib = item["array_attib"]
            mydb.datetime = datetime.datetime.now()
            try:
                session.add(mydb)
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

        return item

class MyImagesPipeline(ImagesPipeline):

    IMAGES_STORE = get_project_settings().get("IMAGES_STORE")

    def get_media_requests(self, item, info):
        return [scrapy.Request(x, meta={'item': item}) for x in item.get(self.images_urls_field, [])]

    def file_path(self, request, response=None, info=None):
        item = request.meta.get('item')
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        rr = item['name_dir'] + '/' + image_guid + '.jpg'
        item['path_to_files'] = self.IMAGES_STORE + '/' + item['name_dir'] + '/'
        return rr

