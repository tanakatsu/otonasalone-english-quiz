import base64
import dataclasses
import re
import requests
from bs4 import BeautifulSoup


@dataclasses.dataclass
class Article:
    title: str
    id: int
    url: str
    date: str


class OtonaSalone:
    URL = "https://otonasalone.jp/tags/ichinichiichieigo/"

    def __init__(self):
        pass

    def get_articles(self) -> list[Article]:
        res = requests.get(self.URL)
        soup = BeautifulSoup(res.content, 'html.parser')

        articles = []
        elms = soup.select("ul.md-articlelist > li")
        for elm in elms:
            e = elm.select_one("div.tag-new")
            if e:
                title = elm.find("span").text
                url = elm.find("a")["href"]
                date = elm.select("li")[0].text
                id = int(re.search(r"\d\d\d\d\d\d", url)[0])
                articles.append(Article(title, id, url, date))
        return articles

    def get_encoded_image(self, article_url: str) -> str:
        res = requests.get(article_url)
        soup = BeautifulSoup(res.content, 'html.parser')
        img_url = soup.select_one("img[fetchpriority]")["data-lazy-src"]

        res_img = requests.get(img_url)
        binary_img = res_img.content
        encoded_img = base64.b64encode(binary_img).decode("utf-8")
        return f"data:image/png;base64,{encoded_img}"
