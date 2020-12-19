from flask import Flask, request, redirect
from api import get_zhilian, folderSelector
from webbrowser import open as webopen
import requests
from os import environ

app = Flask(__name__)


@app.route('/')
def index():
    return redirect('/static/index.html')


@app.route('/geturl')
def test():
    try:
        url = request.args.get("url")
    except:
        url = ''
    r = requests.get(get_zhilian(url))
    # http://127.0.0.1:5000/geturl?url=https://www.lanzous.com/i6aa3hg
    with open("demo3.zip", "wb") as code:
        code.write(r.content)


@app.route('/select')
def select():
    return folderSelector()


if __name__ == '__main__':
    # print(environ['path'])
    webopen('http://127.0.0.1:5200')
    app.run(host='127.0.0.1', port=5200)
