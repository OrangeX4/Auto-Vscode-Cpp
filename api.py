import requests
import bs4
import re
from time import sleep

session = requests.session()

def remove_notes(html: str) -> str:
    """删除网页的注释"""
    # 去掉 html 里面的 // 和 <!-- --> 注释，防止干扰正则匹配提取数据
    # 蓝奏云的前端程序员喜欢改完代码就把原来的代码注释掉,就直接推到生产环境了 =_=
    html = re.sub(r'<!--.+?-->|\s+//\s*.+', '', html)  # html 注释
    html = re.sub(r'(.+?[,;])\s*//.+', r'\1', html)  # js 注释
    return html

def get_zhilian(share_url):
    index_url = 'https://www.lanzous.com'
    headers = {
        'Upgrade-Insecure-Requests': '1',
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3672.400 QQBrowser/10.4.3448.400"
    }
    share_html_text = session.get(url=share_url, headers=headers).text
    share_html_bs4 = bs4.BeautifulSoup(share_html_text, "lxml")
    src_url = share_html_bs4.find('iframe', attrs={'class': 'ifr2'})['src']
    downloads_url = index_url + src_url
    headers_d = {
        "x-requested-with": "XMLHttpRequest",
        "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
        "origin": "https://www.lanzous.com",
        "referer": downloads_url,
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
        "accept-encoding": "gzip, deflate, br",
        "accept-language": "zh-CN,zh;q=0.9",
        "cache-control": "max-age=0",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3672.400 QQBrowser/10.4.3448.400"
    }
    downloads_page = session.get(url=downloads_url, headers=headers).text
    try:
        # sign = re.search('sign.{89}', downloads_page).group()[7:89]
        sign = re.search('var ajaxdata = \'.{0,100}\';', downloads_page).group()[16:-2]
    except:
        sign = re.search('var ajaxup = \'.{0,100}\';', downloads_page).group()[13:-2]

    ajaxm_url = 'https://www.lanzous.com/ajaxm.php'

    data = {
        'action': 'downprocess',
        'sign': sign,
        'ves': 1
    }
    file_data = session.post(url=ajaxm_url, data=data, headers=headers_d).json()
    zhilian = str(file_data['dom']) + '/file/' + str(file_data['url']) + '='
    fake_url = zhilian  # 假直连，存在流量异常检测
    # download_page = self._get(fake_url, allow_redirects=False)
    download_page = session.get(url=fake_url, headers=headers, allow_redirects=False)
    if not download_page:
        return ''
    download_page_html = remove_notes(download_page.text)
    if '网络异常' not in download_page_html:  # 没有遇到验证码
        return(download_page.headers['Location'])
    else:  # 遇到验证码，验证后才能获取下载直链
        file_token = re.findall("'file':'(.+?)'", download_page_html)[0]
        file_sign = re.findall("'sign':'(.+?)'", download_page_html)[0]
        check_api = 'https://vip.d0.baidupan.com/file/ajax.php'
        post_data = {'file': file_token, 'el': 2, 'sign': file_sign}
        sleep(2)  # 这里必需等待2s, 否则直链返回 ?SignError
        # resp = self._post(check_api, post_data)
        resp = session.post(url=check_api, data=post_data, headers=headers)
        direct_url = resp.json()['url']
        if not direct_url:
            return ''
        return direct_url


if __name__ == '__main__':
    i = 0
    while True:
        i = i + 1
        print(i)
        print(get_zhilian('https://www.lanzous.com/i6aa3hg'))
    # print(get_zhilian('https://www.lanzous.com/i6aa3hg'))
