from urllib.parse import urlencode
from pyquery import PyQuery as pq
import requests

base_url = 'https://weixin.sogou.com/weixin?'
proxy_pool_url = 'http://localhost:5555/random'

headers = {
    'Cookie': 'SUID=A1B78E244322910A0000000062789872; ld=EZllllllll2AWnq@YX0OkuJcigdAWnQjJwfToyllll9llllxjylll5@@@@@@@@@@; cd=1652090242&193f2e2be6a880441618bfb0733fdd64; rd=EZllllllll2AWnq@YX0OkuJcigdAWnQjJwfToyllll9llllxjylll5@@@@@@@@@@; SUV=00E44DF9248EB12862826165387C0336; ssuid=7505174292; ABTEST=4|1654089007|v1; weixinIndexVisited=1; ppinf=5|1654089626|1655299226|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozNjolRTklQUElQjglRTklQUElQjglRTklQUElQjglRTklQUElQjh8Y3J0OjEwOjE2NTQwODk2MjZ8cmVmbmljazozNjolRTklQUElQjglRTklQUElQjglRTklQUElQjglRTklQUElQjh8dXNlcmlkOjQ0Om85dDJsdUg3RnJMWHVPQy1rUmFuOGU3U2Z6cVVAd2VpeGluLnNvaHUuY29tfA; pprdig=nOvcWSrfOWOgNKZs62t1K-gyXOWwdMh4qVnNP4qjfMiryTUp8-0Kv75kzXE_4qLnuSmsjW3Ot2Tr39HVUjhUiWY0XIf5oP9efwXLVbBAizy9k7EIZ7OcMP_N80W-4Z1D6uLwc7FEDsdcUYrk2owMM5ANvENjJwyFnOutDSzPc5A; ppinfo=f247238b58; passport=5|1654089626|1655299226|dHJ1c3Q6MToxfGNsaWVudGlkOjQ6MjAxN3x1bmlxbmFtZTozNjolRTklQUElQjglRTklQUElQjglRTklQUElQjglRTklQUElQjh8Y3J0OjEwOjE2NTQwODk2MjZ8cmVmbmljazozNjolRTklQUElQjglRTklQUElQjglRTklQUElQjglRTklQUElQjh8dXNlcmlkOjQ0Om85dDJsdUg3RnJMWHVPQy1rUmFuOGU3U2Z6cVVAd2VpeGluLnNvaHUuY29tfA|953d9aae85|nOvcWSrfOWOgNKZs62t1K-gyXOWwdMh4qVnNP4qjfMiryTUp8-0Kv75kzXE_4qLnuSmsjW3Ot2Tr39HVUjhUiWY0XIf5oP9efwXLVbBAizy9k7EIZ7OcMP_N80W-4Z1D6uLwc7FEDsdcUYrk2owMM5ANvENjJwyFnOutDSzPc5A; sgid=08-55623211-AWKXZ5qHIGQTHhsw790FqAs; ppmdig=1654101627000000f3dfa6e7d43fa4cc2d8b46c3512541dc; IPLOC=CN6200; PHPSESSID=vd1hqou3ml6ers7t1fcb6h77i4; SNUID=8CCA9C2CF3F113967F0F6B01F42724FA; JSESSIONID=aaabLsFxCwbow-Jj1m6dy; ariaDefaultTheme=null',
    'Host': 'weixin.sogou.com',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.60 Safari/537.36'
}
keyword = '2'

proxy = None
max_count = 5


def get_proxy():
    try:
        response = requests.get(proxy_pool_url)
        if response.status_code == 200:
            return response.text
        return None
    except ConnectionError:
        return None


def get_html(url, count=1):
    print('Crawling', url)
    print('Trying Count', count)
    global proxy
    if count >= max_count:
        print('Tried too many counts')
        return None
    try:
        if proxy:
            proxies = {
                'http': proxy
            }
            print(proxies)
            response = requests.get(url, allow_redirects=False, headers=headers, proxies=proxies)
        else:
            response = requests.get(url, allow_redirects=False, headers=headers)

        if response.status_code == 200:
            print(response.text)
            return response.text
        if response.status_code == 302:
            # ip被封
            print('302')
            proxy = get_proxy()
            if proxy:
                print('Using Proxy: ', proxy)
                count += 1
                return get_html(url)
            else:
                print('Get Proxy Failed')
                return None
    except ConnectionError as e:
        print('Error', e.args)
        proxy = get_proxy()
        count = count + 1
        return get_html(url, count)


def get_index(keyword, page):
    data = {
        'query': keyword,
        'type': 2,
        'page': page
    }
    queries = urlencode(data)
    url = base_url + queries
    html = get_html(url)
    return html


def main():
    for page in range(1, 101):
        html = get_index(keyword, page)
        print(html)


if __name__ == '__main__':
    main()

    # proxies = {
    #     'http': 'http://27.72.88.64:8080'
    # }
    # response = requests.get(base_url + 'query=1&type=2&page=1', headers=headers, proxies=proxies)
    # if response.status_code == 200:
    #     print(response.text)
    # if response.status_code == 302:
    #     print('302')
