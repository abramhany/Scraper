import requests
import os
URL = "https://books.toscrape.com/robots.txt"


def scrape(url: str, timeout: float = 5) -> None:
    if not os.path.exists(r"cache\catalogue-page-1.html"):
        res = requests.get(
            url,
            headers={
                "user-agent": "FlyRankInternshipA9/1.0 (https://github.com/abramhany/Scraper)"
            },
            timeout=timeout,
        )
        print('FETCH')

        if res.status_code == 200:
            with open(r"cache\catalogue-page-1.html", "w", encoding="utf-8") as file:
                file.write(res.text)
                file.close()
            
        else:
            print("Bad connection")
    else:
        print('CACHE HIT')
    size = os.path.getsize(r"cache\catalogue-page-1.html")/1024
    print(f"the size is {size} KB")

if __name__ == "__main__":
    res = requests.get(URL, timeout=5)

    if res.status_code == 404:
        print("No robots file found")

    scrape("https://books.toscrape.com/", timeout=5)