from concurrent.futures import ThreadPoolExecutor, as_completed
from urllib.request import urlopen, Request
import time
from dateutil import parser
from datetime import date, datetime
import polars as pl

from bs4 import BeautifulSoup


def load_url(url: str) -> str:
    header = {'User-Agent': 'Mozilla/5.0'}
    r = Request(url, headers = header)
    return urlopen(r).read()


urls = {
    "https://www.abc.es/": ["time", "datetime", "ABC"],
    "https://elpais.com/": ["a", "data-date", "El Mundo"],
    "https://www.elmundo.es/": ["time", "datetime", "El País"]
}


def web_scrapping(url, news_number):

    df = pl.DataFrame({})

    html = load_url(url)
    soup = BeautifulSoup(html, "html.parser")

    date_news = urls[url]

    h2_with_a = soup.select('h2:has(a)', limit=news_number)
    for h in h2_with_a:

        a = h.find("a")
        link = a['href']

        html_href = load_url(link)
        soup_href = BeautifulSoup(html_href, "html.parser")

        news_time = soup_href.find(date_news[0], attrs={date_news[1]: True})
        final_news_time = news_time[date_news[1]]
        fecha_obj = parser.parse(final_news_time)
        normal_date = fecha_obj.strftime("%d/%m/%Y %H:%M:%S")

        df_news = pl.DataFrame(
            {
                "newspaper": date_news[2],
                "title": a.get_text(strip=True),
                #"author": news_author.get_text(strip=True),
                "date": normal_date
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

    return df


with ThreadPoolExecutor() as executor:
    future_to_url = {executor.submit(load_url, url): url for url in list(urls.keys())}
    df = pl.DataFrame({})
    for future in as_completed(future_to_url):
        url = future_to_url[future]
        try:
            df = pl.concat(
                [
                    df,
                    web_scrapping(url, 1),
                ],
                how="vertical",
            )
          # Llama a la función de scraping con la URL
            print(df)
        except Exception as e:
            print(f"Error al procesar {url}: {e}")
    print(df)