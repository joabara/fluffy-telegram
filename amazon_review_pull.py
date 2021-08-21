import pandas as pd
import numpy as np
laptops = pd.read_csv('laptops.csv', encoding='latin1')

companies = laptops['Company'].unique()

# by PRODUCT KEYWORD
import requests
import json
import time

def searchAmazonByProductID(product_ID):
    # by PRODUCT_ID
    import requests
    reviews = []
    url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/reviews"

    querystring = {"asin":product_ID,"country":"US","variants":"1","top":"0"}

    headers = {
        'x-rapidapi-key': "e35047a6a7msh08480cb929f5e1ap1bec83jsncbb5a9cdade0",
        'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        print("Success! Pulling data...")
        x = json.loads(response.text)
        product_reviews = x['reviews']
        for x in product_reviews:
            y = str(x['title']) + " " + str(x['review'])
            z = x['rating']
            w = [y, z]
            reviews.append(w)

    return reviews



AmazonReviews = dict({})

url = "https://amazon-product-reviews-keywords.p.rapidapi.com/product/search"

for company in companies:
    time.sleep(2)
    ASINs = []
    keyword = str(company + " laptop")
    print(keyword)
    querystring = {"keyword":keyword, "page":"1", "country":"US","category":"aps"}
    headers = {
        'x-rapidapi-key': "e35047a6a7msh08480cb929f5e1ap1bec83jsncbb5a9cdade0",
        'x-rapidapi-host': "amazon-product-reviews-keywords.p.rapidapi.com"
        }

    print("Querying " + keyword)
    response = requests.request("GET", url, headers=headers, params=querystring)

    if response.status_code == 200:
        print("Success! Pulling data...")
        x = json.loads(response.text)
        product_listings = x['products']
        for x in product_listings:
            ASINs.append(x['asin'])

    products = []
    for x in ASINs:
        time.sleep(2)
        y = searchAmazonByProductID(x)
        products.append(y)
    AmazonReviews[company] = products
    products = []

df = pd.DataFrame(columns=['Company', 'Review', 'Rating'])
for k, v in AmazonReviews.items():
    for reviews in v:
        for item in reviews:
            review = ""
            rating = ""
            try:
                review = item[0]
                rating = item[1]
            except IndexError: pass
            df = df.append({'Company': str(k), 'Review': review, 'Rating': rating}, ignore_index=True)

df.to_csv('reviews.csv')
