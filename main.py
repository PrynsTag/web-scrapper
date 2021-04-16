import os
import string

import requests
from bs4 import BeautifulSoup


class WebScrapper:
    def __init__(self, url):
        self.url = url
        self.request = requests.get(url)
        self.list_articles = []
        self.num_pages = 0
        self.category = ""
        self.page_dir = ""

    def __str__(self):
        return f"Articles Saved\nSaved articles: {self.list_articles}"

    def get_user_input(self):
        self.num_pages = int(input())
        self.category = input()

    def create_directory(self, page_num):
        self.page_dir = os.path.join(os.getcwd(), f"Page_{page_num}")
        os.mkdir(self.page_dir)

    def scrape_page(self):
        self.get_user_input()

        if self.request:
            head_link = "https://www.nature.com"

            for page_num in range(1, self.num_pages + 1):
                self.create_directory(page_num)

                page = f"https://www.nature.com/nature/articles?searchType=journalSearch&sort=PubDate&page={page_num}"
                page_request = requests.get(page)
                soup = BeautifulSoup(page_request.content, "html.parser")
                articles = soup.find_all("article")

                for article in articles:
                    article_type = article.find("span", class_="c-meta__type").text

                    if article_type == self.category:
                        tail_link = article.find("a", {"data-track-action": "view article"}).get("href")

                        hyperlink = requests.get(head_link + tail_link)
                        hyperlink_soup = BeautifulSoup(hyperlink.content, "html.parser")

                        # Take into account article-item__body and article__body class
                        if hyperlink_soup.find("div", {"class": "article-item__body"}):
                            hyperlink_body = hyperlink_soup.find("div", {"class": "article-item__body"}).text.strip()
                        else:
                            hyperlink_body = hyperlink_soup.find("div", {"class": "article__body"}).text.strip()

                        translator = str.maketrans('', '', string.punctuation)
                        title = hyperlink_soup \
                            .find("h1", {"itemprop": "headline"}) \
                            .text.translate(translator) \
                            .replace(" ", "_")

                        self.save_to_file(self.page_dir, title, hyperlink_body)

            return self
        else:
            return f"The URL returned {self.request.status_code}"

    def save_to_file(self, page_dir, filename, hyperlink_body):
        try:
            with open(f"{os.path.join(page_dir, filename)}.txt", 'w', encoding="UTF-8") as file:
                print(hyperlink_body, file=file)

            self.list_articles.append(f"{filename}.txt")
        except Exception as e:
            return e


if __name__ == '__main__':
    r = WebScrapper("https://www.nature.com/nature/articles")
    print(r.scrape_page())