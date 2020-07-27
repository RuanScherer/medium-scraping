from flask import Flask, request, render_template, redirect, url_for
from bs4 import BeautifulSoup
import requests

app = Flask(__name__)


@app.route('/')
def serve_page():
    url = request.args.get('url')
    if url is not None:
        if is_valid_url(url):
            return redirect(url_for('show_post', url=url))
        else:
            return render_template('index.html', error="Invalid post URL.")
    else:
        return render_template('index.html')


@app.route('/post')
def show_post():
    url = request.args['url']
    if url is not None:
        if is_valid_url(url):
            req = requests.get(url)
            if req.status_code == 200:
                content = req.content
                soup = BeautifulSoup(content, 'html.parser')
                article = soup.findAll(name="article")
                soup = BeautifulSoup(str(article), 'html.parser')
                title = soup.find(name="h1")
                post = soup.findAll(name=["p", "li"])
                post_content = ""
                for tag in post:
                    for content in tag.contents:
                        post_content += " " + content.string
                post = {"title": title.string, "content": post_content}
                return render_template('post.html', post=post)
            else:
                return render_template('post.html', error="Failed to get post.")
        else:
            return render_template('post.html', error="Invalid post URL.")
    else:
        return render_template('post.html', error="Invalid post URL.")


def is_valid_url(url):
    if url.find("https://medium.com/") == -1:
        return False
    else:
        url = url.replace("https://medium.com/", "")
        url_parts = url.split("/")
        if len(url_parts) < 2:
            return False
        else:
            return True
