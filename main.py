import string

import requests
from bs4 import BeautifulSoup


class WebScrapper:
    def __init__(self, url):
        self.url = url
        self.request = requests.get(url)
        self.list_articles = []

    def __str__(self):
        return f"Saved articles: {self.list_articles}"

    def get_info(self):
        if self.request:
            head_link = "https://www.nature.com"
            soup = BeautifulSoup(self.request.content, "html.parser")
            articles = soup.find_all("article")

            for article in articles:
                article_type = article.find("span", class_="c-meta__type").text

                if article_type == "News":
                    tail_link = article.find("a", {"data-track-action": "view article"}).get("href")

                    hyperlink = requests.get(head_link + tail_link)
                    hyperlink_soup = BeautifulSoup(hyperlink.content, "html.parser")
                    hyperlink_body = hyperlink_soup.find("div", class_="article__body").text.strip()

                    translator = str.maketrans('', '', string.punctuation)
                    title = hyperlink_soup.find("title").text.translate(translator).replace(" ", "_")

                    self.save_to_file(title, hyperlink_body)
            return "Content saved."
        else:
            return f"The URL returned {self.request.status_code}"

    def save_to_file(self, filename, hyperlink_body):
        try:
            with open(f"{filename}.txt", 'w', encoding="UTF-8") as file:
                print(hyperlink_body, file=file)

            self.list_articles.append(f"{filename}.txt")
        except Exception as e:
            return e


if __name__ == '__main__':
    r = WebScrapper("https://www.nature.com/nature/articles")
    print(r.get_info())
    print(r)
