import requests

from bs4 import BeautifulSoup


class WebScrapper:
    def __init__(self, url):
        self.url = url
        self.request = requests.get(url)

    def get_info(self):
        soup = BeautifulSoup(self.request.content, "html.parser")
        is_movie = "title" in self.url
        is_imdb = soup.find("meta", {"content": "IMDb"})

        if is_imdb and is_movie:
            return dict(title=soup.find("meta", {"name": "title"}).get("content"),
                        description=soup.find("meta", {"name": "description"}).get("content"))
        else:
            return "Invalid movie page!"


if __name__ == '__main__':
    r = WebScrapper(input("Input the url:\n"))
    print(r.get_info())
