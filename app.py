from flask import Flask, request, redirect
from api import get_zhilian, folderSelector
from webbrowser import open as webopen
import requests
from os import environ, system, path, remove
import py7zr

app = Flask(__name__)

# 跨域支持

def after_request(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    return resp


app.after_request(after_request)


@app.route('/')
def index():
    return redirect('/static/index.html')


@app.route('/select')
def select():
    return folderSelector()


@app.route('/isVscode')
def isVscode():
    return ('vs code' in environ['path'].lower() or 'vscode' in environ['path'].lower()) and 'true' or 'false'


@app.route('/isMinGW')
def isMinGW():
    return 'mingw' in environ['path'].lower() and 'true' or 'false'


@app.route('/vscode')
def vscode():
    r = requests.get(get_zhilian("https://wwe.lanzous.com/imCQzjig9yb"))
    with open("install.exe", "wb") as code:
        code.write(r.content)
    system('install.exe')
    if path.exists("install.exe"):
        remove("install.exe")
    return 'true'


@app.route('/mingw')
def mingw():
    try:
        pathStr = request.args.get('path')
    except:
        pathStr = 'D:\\Program\\MinGW'
    r = requests.get(get_zhilian('https://wwe.lanzous.com/iqjyBjih6qb'))
    with open("MinGW.7z", "wb") as code:
        code.write(r.content)
    archive = py7zr.SevenZipFile('MinGW.7z', mode='r')
    archive.extractall(path=pathStr.strip())
    archive.close()
    aftPath = environ['path'] + ';' + path.join(pathStr.strip(), 'MinGw\\bin') + ';'
    command = r"setx path %s /m" % aftPath
    environ['path'] = aftPath
    system(command)
    # print(command)
    if path.exists("MinGW.7z"):
        remove("MinGW.7z")
    return 'true'


@app.route('/codespace')
def codespace():
    try:
        pathStr = request.args.get("path")
    except:
        pathStr = 'D:\\CodeSpace'
    r = requests.get(get_zhilian('https://wwe.lanzous.com/ixnHGjihzwb'))
    with open("CodeSpace.7z", "wb") as code:
        code.write(r.content)
    archive = py7zr.SevenZipFile('CodeSpace.7z', mode='r')
    print(pathStr)
    archive.extractall(path=pathStr.strip())
    archive.close()
    if path.exists('CodeSpace.7z'):
        remove('CodeSpace.7z')
    system('explorer.exe ' + path.join(pathStr.strip(), 'CodeSpace'))
    return 'true'


if __name__ == '__main__':
    webopen('http://127.0.0.1:5200')
    app.run(host='127.0.0.1', port=5200)
