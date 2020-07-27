from bs4 import BeautifulSoup
import requests


def is_valid_url(url):
    if url.find("https://medium.com/") == -1:
        print("Invalid URL")
        return False

    url = url.replace("https://medium.com/", "")
    url_parts = url.split("/")
    if len(url_parts) < 2:
        return False

    return True


if is_valid_url('https://medium.com/data-hackers/como-fazer-web-scraping-em-python-23c9d465a37f'):
    req = requests.get('https://medium.com/data-hackers/como-fazer-web-scraping-em-python-23c9d465a37f')
    if req.status_code == 200:
        content = req.content
        soup = BeautifulSoup(content, 'html.parser')
        article = soup.findAll(name="article")
        soup = BeautifulSoup(str(article), 'html.parser')
        title = soup.find(name="h1")
        subtitle = soup.find(name="h2")
        post = soup.findAll(name=["p", "ul"])
        for tag in post:
            for content in tag.contents:
                print(content.string)
