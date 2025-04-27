from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlopen, Request
import time
import polars as pl

from bs4 import BeautifulSoup


def load_url(url: str) -> str:
    header = {'User-Agent': 'Mozilla/5.0'}
    r = Request(url, headers = header)
    return urlopen(r).read()

def get_day(news):
    return news.get_text().split()[0]

def get_updated_hour(news):
    return news.get_text().split()[-1]


#news_number = soup.find_all("h2", {"class": "voc-title"})
#print(len(news_number))



#
#news_title_a_href_all = news_title_a_all['href']



def web_scrapping(url, news_number):

    df = pl.DataFrame({})

    html = load_url(url)
    soup = BeautifulSoup(html, "html.parser")

    # news_title_a_all = news_title_all.find("a")

    # news_title_all = soup.find_all("h2", {"class": "voc-title"}, limit = news_number)

    # news_title_all = soup.find_all("h2", {"class": "voc-title"}, limit = news_number)
    # news_author_all = soup.find_all("span", {"class": "voc-onplus__author"}, limit = news_number)

    for a in soup.find_all('a', limit=news_number):
        link = a['href']

        html_href = load_url(link)
        soup_href = BeautifulSoup(html_href, "html.parser")

        news_time = soup_href.find("time")
        day = get_day(news_time)
        updated = get_updated_hour(news_time)

        df_news = pl.DataFrame(
            {
                "title": a.get_text(strip=True),
                "author": news_author.get_text(strip=True),
                "time": day,
                "update_time": updated
            }
        )

        df = pl.concat(
            [
                df,
                df_news,
            ],
            how="vertical",
        )

        time.sleep(10)



    # for news in news_title_all:
    #     news_author = news.find_next("span", {"class": "voc-onplus__author"})
    #     news_title_a = news.find("a")
    #     news_title_a_href = news_title_a['href']

    #     html_href = load_url(news_title_a_href)
    #     soup_href = BeautifulSoup(html_href, "html.parser")

    #     news_time = soup_href.find("time")

    #     day = get_day(news_time)
    #     updated = get_updated_hour(news_time)

    #     df_news = pl.DataFrame(
    #     {
    #         "title": news.get_text(strip=True),
    #         "author": news_author.get_text(strip=True),
    #         "time": day,
    #         "update_time": updated
    #     }
    #     )

    #     df = pl.concat(
    #     [
    #         df,
    #         df_news,
    #     ],
    #     how="vertical",
    #     )

    #     time.sleep(10)

    return df


urls = [
    "https://www.abc.es/",
    "https://elpais.com/",
    "https://www.elmundo.es/"
]

with ThreadPoolExecutor() as executor:
    future_to_url = [executor.submit(load_url, url) for url in urls]
    for future in as_completed(future_to_url):
        data = future.result()
        print(data[:50])
        # TODO: do something with the data