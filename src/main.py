import requests


URL = "https://books.toscrape.com/robots.txt"

res =requests.get(URL)

if res.status_code == 404:
    print("No robots file found")