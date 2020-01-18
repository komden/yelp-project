from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary)
from scrapy.utils.project import get_project_settings

MyBase = declarative_base()

def db_connect():
    return create_engine(get_project_settings().get("CONNECTION_STRING"))

def create_table(engine):
    MyBase.metadata.create_all(engine)

class MyDB(MyBase):
    __tablename__ = "yelp_table"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column('name', Text())
    address_all = Column('address_all',Text())
    address_all_span = Column('address_all_span',Text())
    sity = Column('sity', Text())
    country = Column('country', Text())
    index = Column('index', Integer)
    phone = Column('phone', Text())
    countreview = Column('countreview', Integer)
    website = Column('website', Text())
    category = Column('category', Text())
    rannge = Column('rannge', Float)
    path_to_files = Column('path_to_files', Text())
    schedule = Column('schedule', Text())
    array_attib = Column('array_attib', Text())
    datetime = Column('datetime', DateTime())

    def __init__(self, name, address_all, address_all_span, sity, country, index, phone, countreview, website, category, rannge, path_to_files, schedule, array_attib, datetime):
        self.name = name
        self.address_all = address_all
        self.address_all_span = address_all_span
        self.sity = sity
        self.country = country
        self.index = index
        self.phone = phone
        self.countreview = countreview
        self.website = website
        self.category = category
        self.rannge = rannge
        self.path_to_files = path_to_files
        self.schedule = schedule
        self.array_attib = array_attib
        self.datetime = datetime

    def __repr__(self):
        return "<MyDB('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')>" % (self.name, self.address_all, self.address_all_span, self.sity, self.country, self.index, self.phone, self.countreview, self.website, self.category, self.rannge, self.path_to_files, self.schedule, self.array_attib, self.datetime)

    