import requests
import os
from bs4 import BeautifulSoup
import  time
from urllib.parse import urljoin

def page_parser(url: str,page_number:str, timeout: float = 10):

    location = f"cache\\catalogue-page-{page_number}.html"
    if not os.path.exists(location):
        time.sleep(3)
        res = requests.get(

            url,
            headers={
                "user-agent": "FlyRankInternshipA9/1.0 (https://github.com/abramhany/Scraper)"
            },
            timeout=timeout,

        )

        print('FETCH')

        if res.status_code == 200:

            with open(location, "w", encoding="utf-8") as file:
                file.write(res.text)
                file.close()
            size = os.path.getsize(location)/1024
            print(f"the size is {size} KB")
        else:

            print("Bad connection")

    else:

        print('CACHE HIT')

    
    
    return location

def url_joiner(original_url,links):

    abs_urls = []

    for link in links:
        if link.startswith("catalogue/"):
                        absolute_url = urljoin(original_url, link)
        else :
                        link = "catalogue/" + link 
                        absolute_url = urljoin(original_url, link)
        abs_urls.append(absolute_url)

    return abs_urls

def link_parser(loctaion):
    try:
        with open(loctaion)as file:
        
            soup = BeautifulSoup(file,'html.parser')
    except FileNotFoundError as e:
        return e
    
    #rows = soup.find('ol',class_='row')
    rows = soup.find_all('div',class_='image_container')
    print(rows)
    next_url = soup.find('li',class_='next').find('a').get('href')
    urls = [row.find('a').get('href') for row in rows]
    
    urls.append(next_url)
    return urls


    
if __name__ == "__main__":

    book_url = "https://books.toscrape.com/robots.txt"
    abs_url = "https://books.toscrape.com/"
    site_url = abs_url
    res = requests.get(book_url, timeout=5)
    
    if res.status_code == 404:
    
        print("No robots file found")

    all_urls = []
    for i in range(1,4,1):
        
        location = page_parser(site_url, str(i),timeout=5,)

        urls = link_parser(location)
        abs_urls = url_joiner(abs_url,urls)

        site_url = abs_urls.pop(-1)
        all_urls.extend(abs_urls)

cache_lenght = len(os.listdir("cache\\"))

print(f"pages= {cache_lenght}")
print(f"discovered urls= {len(all_urls)}")
print(f"unique urls= {len(set(all_urls))}")