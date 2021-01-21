import requests
import time 
import json
import pandas as pd

class Crawler():
    def __init__(self):
        self.token_url = "https://public-apis-api.herokuapp.com/api/v1/auth/token"
        self.categories_url="https://public-apis-api.herokuapp.com/api/v1/apis/categories?page={}"
        self.category_base_url = "https://public-apis-api.herokuapp.com/api/v1/apis/entry?page={}&category="
        self.token_start = time.perf_counter()
        self.token = ""
        self.empty_categories = []

    def token_exists(self):
        return self.token!="" and ((time.perf_counter()-self.token_start)<280)

    def get_token(self):
        if  self.token_exists():
            return self.token
        r = requests.get(self.token_url) 
        self.token_start = time.perf_counter()
        json_data = r.json()
        self.token = json_data["token"]
        return self.token

   
    def make_auth_request(self,url):
        token = self.get_token()
        response = requests.get(url,headers={
            'Authorization': f'Bearer {token}'
            })
        if response.status_code==200:
            return response
        time.sleep(60)
        return self.make_auth_request(url)

    def get_categories(self,page):
        url = self.categories_url.format(page)
        response = self.make_auth_request(url)
        json_data = response.json()
        categories = json_data['categories']
        return categories

    def get_category_details(self,category,page):
        url = self.category_base_url.format(page)+category
        response = self.make_auth_request(url)
        json_data = response.json()
        return json_data

    def get_data(self):
        data = []
        all_categories = []
        for page in range(1,6):
            categories = self.get_categories(page)
            print("page",page)
            print(categories)
            all_categories.extend(categories)
            for category in categories:
                details = self.get_category_details(category,page)
                rows = details["categories"]
                if not rows:
                    self.empty_categories.append(details)
                df = pd.DataFrame(rows)
                print(category)
                print(df)
                print()
                data.extend(rows)
        return all_categories,data
