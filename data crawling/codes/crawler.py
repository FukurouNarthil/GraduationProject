import bs4
import requests
import os
from hanziconv import HanziConv

dir = 'D:\Learning\Graduation Project\data crawling\codes\data_per_region'
regional_literatures = ["古希腊文学", "古罗马文学", "古埃及文学", "爱尔兰文学",  "美国文学", "英国文学", 
                        "意大利文学", "西班牙文学", "印度文学", "中国文学", "台湾文学", "香港文学",
                        "朝鲜文学", "韩国文学", "德国文学", "伊朗文学", "日本文学", "法国文学", "拉美文学", 
                        "俄国文学"]


# 爬虫
def wikiCrawler(url):
    response = requests.get(url, proxies={
        'http': 'http://127.0.0.1:1080',
        'https': 'https://127.0.0.1:1080'
    })
    return response


for literature in regional_literatures:
    url = "http://zh.wikipedia.org/wiki/" + literature

    response = wikiCrawler(url)

    if response is not None:
        page = bs4.BeautifulSoup(response.text, 'html.parser')

        # 文字内容
        paragraphs = page.select("p")
        content = '\n'.join([HanziConv.toSimplified(para.text) for para in paragraphs])
        
        # 链接
        hrefs = []
        for link in page.find_all('a'):
            if link.get('href') is not None and '/wiki/' in link.get('href') and link.string is not None:
                text = link.string + link.get('href')
                hrefs.append(link.string + ': http://zh.wikipedia.org' + link.get('href'))
        links = '\n'.join(href for href in hrefs)

        path = os.path.join(dir, literature + '.txt')
        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
            f.write(links)
            f.close()
