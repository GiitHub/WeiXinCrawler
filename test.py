import requests

url = 'https://weixin.sogou.com/weixin?query=%E5%B9%B4%E5%90%8E&type=2&page=1'

proxies = {
    'http': '54.193.249.144:8080'
}
try:
    response = requests.get(url, proxies=proxies)
    if response.status_code == 200:
        print('1')
    else:
        print('2')
except ConnectionError:
    print('error')