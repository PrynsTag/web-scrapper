import requests


class WebScrapper:
    def __init__(self, url):
        self.url = url

    def search(self):
        return self.get_quote(requests.get(self.url))

    def get_quote(self, request):
        query = self.url.split("/")
        if "quotes" in query and request:
            return request.json()["content"]
        else:
            return "Invalid quote resource!"


if __name__ == '__main__':
    r = WebScrapper(input("Input the url:\n"))
    print(r.search())
