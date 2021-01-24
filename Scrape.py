#importing the dependencies
import requests  # performs web requests
import time      # contains time counter & helper functions
import json      # useful to manipulate json objects
import pandas as pd    #useful for making dataframes 

# A crawler class with helpful member functions 
class Crawler():

    # constructor function which gets executed on object creation
    def __init__(self):
        self.token_url = "https://public-apis-api.herokuapp.com/api/v1/auth/token"
        self.categories_url="https://public-apis-api.herokuapp.com/api/v1/apis/categories?page={}"
        self.category_base_url = "https://public-apis-api.herokuapp.com/api/v1/apis/entry?page={}&category="
        self.token_start = time.perf_counter()
        self.token = ""
        self.empty_categories = []

    # check if a un-expired token exists
    def token_exists(self):
        #condition1: initial token is empty string -> invalid
        #condition2: previous token is expired or not ? -> valid/invalid
        return self.token!="" and ((time.perf_counter()-self.token_start)<280)

    # returns a valid token
    def get_token(self):
        #if valid token exists? return it
        if  self.token_exists():
            return self.token
        # otherwise, request for a new token
        response = requests.get(self.token_url) 
        # the token requst is made, it should expire in 300 seconds from now
        # so, we record the time at which the token is initiated
        self.token_start = time.perf_counter()
        # extract the json version of the response
        json_data = response.json()
        # store the token as a member of the class
        self.token = json_data["token"]
        #returns the new token
        return self.token

    # return a valid response from server
    # functionalities: 
    #   1) authorization 
    #   2) work around rate limited server 
    def make_auth_request(self,url):
        token = self.get_token()
        response = requests.get(url,headers={
            'Authorization': f'Bearer {token}'
            })
        if response.status_code==200: # response is valid: OK 
            return response
        time.sleep(60) # wait for 60 seconds
        #recursive call until we make a valid request
        return self.make_auth_request(url)

    # returns a list of names of categories from the input page
    def get_categories(self,page:int):
        # format the url
        url = self.categories_url.format(page)
        # get the response
        response = self.make_auth_request(url)
        # convert response into a json object
        json_data = response.json()
        # The list of values correspond to the key:categories 
        categories = json_data['categories']
        #returns the list of strings i.e categories 
        return categories

    # finds the items that belong to a given category 
    def get_category_details(self,category:str,page:int)->dict:
        # embed the base url with given page number and append category name 
        url = self.category_base_url.format(page) + category  
        # obtain a valid response for a request
        response = self.make_auth_request(url)
        # return the json version of the response
        json_data = response.json()
        return json_data

    
    def get_data(self):
        all_data = []
        all_categories = []
        for page in range(1,6): # total pages is 5 => range = [1,6)
            #for a page,
            #   1) get the list of category names
            #   2) get all objects belonging to each category  
            #   3) return all of them
            categories = self.get_categories(page)
            print("page",page)
            print(categories)
            all_categories.extend(categories)
            for category in categories:
                details = self.get_category_details(category,page)
                rows = details["categories"]
                if not rows:
                    # storing the empty size categories for later analysis
                    self.empty_categories.append(details)

                df = pd.DataFrame(rows) # construct a dataframe from the rows 
                print(category)   
                print(df) # printing a dataframe for the entire category
                print()   # formatting output
                all_data.extend(rows) #Add new rows to the total set 
        return all_categories,all_data
