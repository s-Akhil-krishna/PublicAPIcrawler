#importing dependencies
import json
import time
import requests
import sqlalchemy
from Scrape import Crawler
from sqlalchemy import create_engine, Column, String, Integer
from sqlalchemy.orm import  sessionmaker
from sqlalchemy.ext.declarative import declarative_base

#create db, session, base
engine=create_engine("sqlite:///data.db")
session = sessionmaker(bind=engine)
my_session = session()
base = declarative_base()

#inherit base class, define table schema
class Model(base):
    __tablename__ = "model"
    id = Column(Integer,primary_key=True)
    api = Column(String) 
    description = Column(String)
    auth = Column(String)
    https = Column(String)
    cors = Column(String)
    link = Column(String)
    category = Column(String)

    def __repr__(self):
        return self.api 

#Add all the tables to the database
base.metadata.create_all(engine)

#helper class: crawl,format,write to db
class processData():
    def __init__(self,session):
        self.categories = []
        self.data = []
        self.crawler = Crawler()
        self.session = session

    def pretty_json(self,json_object):
        #json_object: dict 
        return json.dumps(json_object, indent = 1)

    def get_data(self):
        if self.data:
            return self.data
        self.categories,self.data = self.crawler.get_data()
        return self.categories,self.data

    def prepare(self,json_obj):
        #json_obj:dict
        json_data = {}
        for key,value in json_obj.items():
            json_data[key.lower()]=str(value)
        return json_data

    def write_to_db(self): 
        for json_obj in self.data:
            json_obj = self.prepare(json_obj)
            instance = Model(**json_obj)
            self.session.add(instance)
        self.session.commit()
        print("Successfully pushed to SQLite database")

    def query_db(self):
        print("db query")
        qs1 = self.session.query(Model).all()
        print(qs1)


    def print_data(self):
        categories,data = self.get_data()
        print(categories)
        print(data)        

processor = processData(my_session)
processor.write_to_db()
processor.query_db()
