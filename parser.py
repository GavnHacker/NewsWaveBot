import requests
from bs4 import BeautifulSoup
import json


def get_news():
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/108.0.0.0 Safari/537.36"
    }
    url = "https://www.rbc.ua/rus/news"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    article_news_list = soup.find("div", class_="newsline").find_all('div')

    news_dict = {}
    for article in article_news_list:
        try:
            title = article.find('a').text.strip()
            link = article.find('a').get('href')
            news_id = link.split("-")[-1]
            news_id = news_id[:-5]
            news_dict[news_id] = {
                "title": title,
                "link": link
            }

        except:
            pass

    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)


fresh_news = {}


def check_update():
    with open("news_dict.json") as file:
        news_dict = json.load(file)
    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/108.0.0.0 Safari/537.36"
    }
    url = "https://www.rbc.ua/rus/news"
    r = requests.get(url=url, headers=headers)

    soup = BeautifulSoup(r.text, "lxml")
    article_news_list = soup.find("div", class_="newsline").find_all('div')

    for article in article_news_list:
        try:
            link = article.find('a').get('href')
            news_id = link.split("-")[-1]
            news_id = news_id[:-5]
            if news_id in news_dict:
                continue
            else:
                title = article.find('a').text.strip()
                link = article.find('a').get('href')
                news_id = link.split("-")[-1]
                news_id = news_id[:-5]
                news_dict[news_id] = {
                    "title": title,
                    "link": link
                }
                fresh_news[news_id] = {
                    "title": title,
                    "link": link
                }
        except:
            pass
    with open("news_dict.json", "w") as file:
        json.dump(news_dict, file, indent=4, ensure_ascii=False)

    return fresh_news


if __name__ == "__main__":
    check_update()
