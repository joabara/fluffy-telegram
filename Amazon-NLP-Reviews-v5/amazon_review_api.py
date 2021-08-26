# by PRODUCT KEYWORD
import requests
import json
import pandas as pd

ASINs = []

url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/search"

querystring = {"keyword":"Apple laptops", "page":"1", "country":"US","category":"aps"}

headers = {
    'x-rapidapi-key': "e35047a6a7msh08480cb929f5e1ap1bec83jsncbb5a9cdade0",
    'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
    }

response = requests.request("GET", url, headers=headers, params=querystring)
x = json.loads(response.text)
product_listings = x['products'][0:5]


for x in product_listings:
    ASINs.append(x['asin'])


def searchAmazonByProductID(product_ID):
    # by PRODUCT_ID
    import requests

    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/reviews"

    querystring = {"asin":"B07XQXZXJC","country":"US","variants":"1","top":"0"}

    headers = {
        'x-rapidapi-key': "e35047a6a7msh08480cb929f5e1ap1bec83jsncbb5a9cdade0",
        'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)
    print(response.text)