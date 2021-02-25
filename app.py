from flask import Flask, request, redirect
from api import folderSelector
from webbrowser import open as webopen
import requests
from os import environ, system, path, remove
import py7zr
from writeCpp import writeCpp, getMinGW

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
    return getMinGW(environ['path']) != '' and 'true' or 'false'


@app.route('/vscode')
def vscode():
    r = requests.get('https://box.nju.edu.cn/f/1ccf7406b7a94b278b84/?dl=1')
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
        pathStr = 'D:\\Program'
    r = requests.get('https://box.nju.edu.cn/f/720aab0f6e3644a4b29c/?dl=1')
    with open("MinGW.7z", "wb") as code:
        code.write(r.content)
    archive = py7zr.SevenZipFile('MinGW.7z', mode='r')
    archive.extractall(path=pathStr.strip())
    archive.close()
    aftPath = environ['path'] + ';' + path.join(pathStr.strip(), 'MinGw\\bin') + ';'
    command = r'setx PATH "' + aftPath + r'"'
    environ['path'] = aftPath
    system(command)
    if path.exists("MinGW.7z"):
        remove("MinGW.7z")
    return 'true'


@app.route('/codespace')
def codespace():
    try:
        pathStr = request.args.get("path")
        mingwPath = request.args.get('mingw')
    except:
        pathStr = 'D:\\'
        mingwPath = 'D:\\Program'
    r = requests.get('https://box.nju.edu.cn/f/d7a6506c07c6423ab816/?dl=1')
    with open("CodeSpace.7z", "wb") as code:
        code.write(r.content)
    archive = py7zr.SevenZipFile('CodeSpace.7z', mode='r')
    archive.extractall(path=pathStr.strip())
    archive.close()
    if path.exists('CodeSpace.7z'):
        remove('CodeSpace.7z')
    writeCpp(path.join(mingwPath, 'MinGW'), path.join(pathStr.strip(), 'CodeSpace'))
    system('explorer.exe ' + path.join(pathStr.strip(), 'CodeSpace'))
    return 'true'


if __name__ == '__main__':
    webopen('http://127.0.0.1:5200')
    app.run(host='127.0.0.1', port=5200)

