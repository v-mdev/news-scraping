from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlopen, Request
import time

from bs4 import BeautifulSoup

url = "https://www.abc.es/"

def load_url(url: str) -> str:
    r = Request(url)
    return urlopen(r).read()

html = load_url(url)
soup = BeautifulSoup(html, "html.parser")

#news_number = soup.find_all("h2", {"class": "voc-title"})
#print(len(news_number))

news_number = 10

news_title_all = soup.find_all("h2", {"class": "voc-title"}, limit = news_number)
news_author_all = soup.find_all("span", {"class": "voc-onplus__author"}, limit = news_number)
#news_title_a_all = news_title_all.find("a")
#news_title_a_href_all = news_title_a_all['href']

news_title_author = zip(news_title_all,news_author_all)
print(news_title_author)


for news in news_title_all:
    print(news)
    news_author = news.find_next("span", {"class": "voc-onplus__author"})
    news_title_a = news.find("a")
    print(news_title_a)
    news_title_a_href = news_title_a['href']

    html_href = load_url(news_title_a_href)
    soup_href = BeautifulSoup(html_href, "html.parser")

    news_time = soup_href.find("time")


    print("News Title: \n", news.get_text())
    print("Author: \n", news_author.get_text())
    print("Time: \n", news_time.get_text())
    print("\n")

    time.sleep(10)


urls = [
    "https://stackoverflow.com/questions/415511/how-to-get-the-current-time-in-python",
    "https://stackoverflow.com/questions/38137771/printing-the-time-between-2-points-in-a-program-in-python",
    "https://stackoverflow.com/questions/64341047/how-to-get-the-current-time-with-python",
]

with ThreadPoolExecutor() as executor:
    future_to_url = [executor.submit(load_url, url) for url in urls]
    for future in as_completed(future_to_url):
        data = future.result()
        print(data[:50])
        # TODO: do something with the data