from flask import Flask, redirect, request
from api import get_zhilian
from webbrowser import open

app = Flask(__name__)

@app.route('/')
def index():
    return "hello"


@app.route('/geturl')
def test():
    try:
        url = request.args.get("url")
    except:
        url = ''
    return redirect(get_zhilian(url))


if __name__ == '__main__':
    open('http://127.0.0.1:5000')
    app.run()
    
