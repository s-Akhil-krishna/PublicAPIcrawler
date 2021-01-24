#importing dependencies

#dealing with json 
import json

# time functions
import time

# dataframe functionality
import pandas as pd

# perform web requests
import requests

# Python support for relational database 
import sqlalchemy

#Crawler class imported from Scrape.py module
from Scrape import Crawler

# Schema related functions 
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
    #intialize the table name
    __tablename__ = "model"

    # declaring the columns/attributes of the table
    # name: datatype

    # id is the primary key, whose values are automatically assigned on creating rows
    id = Column(Integer,primary_key=True)

    # 7  attributes as mentioned in the public api github repo
    api = Column(String) 
    description = Column(String)
    auth = Column(String)
    https = Column(String)
    cors = Column(String)
    link = Column(String)
    category = Column(String)

    def __repr__(self):
        #This represents a row in the db
        return self.api 

#Add all the tables to the database
base.metadata.create_all(engine)

#helper class: crawl,format,write to db
class processData():
    def __init__(self,session): # takes the live db session as input
        self.categories = []  # all category names
        self.data = []        # data that belongs to of all categories 
        self.crawler = Crawler()  # instantiating Crawler class
        self.session = session      

    # formatted version of json objects
    def pretty_json(self,json_object):
        #json_object: dict 
        return json.dumps(json_object, indent = 1)

    def get_data(self):
        if self.data: # if already exists, we need not re-perform crawling
            return self.categories,self.data
        # invoke the get_data() member function of the crawler instance
        self.categories,self.data = self.crawler.get_data()
        #returns categories and data 
        return self.categories,self.data

    def prepare(self,json_obj):
        # json_obj:dict
        json_data = {}
        for key,value in json_obj.items():
            json_data[key.lower()]=str(value)
        # returns a json_obj with all keys in lower case.
        return json_data

    def write_to_db(self):
        #get data first
        self.categories,self.data = self.get_data()    
        # each row is in the form of a dictionary/json
        for json_obj in self.data:
            # obtain a processed object with lower case
            json_obj = self.prepare(json_obj)
            # now, send dictionary as kwargs to the schema class -> instantiate it 
            instance = Model(**json_obj)
            # A row is crated, add it to the table 
            self.session.add(instance)
            # now commit/confirm the modifications of the db table
            self.session.commit()
        # flush enables the db to settle if any changes are not enforced
        self.session.flush()
        print("Successfully pushed to SQLite database")


    def query_db(self):
        # queries on the database that we created
        print("db query results") # starting line for user 
        # pulling a QuerySet from the database -> All items/rows
        qs = self.session.query(Model).all()
        # put the rows into a dataframe
        df = pd.DataFrame(qs)
        # print it out
        print(df)


    def print_data(self):
        # just a display function
        categories,data = self.get_data()
        print(categories)
        print(data)        

# instantiate the ProcessData class
processor = processData(my_session)
#now, write the data to the db table
processor.write_to_db()
# test the success of the above operations by printing out the rows of the db table
processor.query_db()