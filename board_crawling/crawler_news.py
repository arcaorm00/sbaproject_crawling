import os, shutil
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
basedir = os.path.abspath(os.path.dirname(__file__))
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from pandas import DataFrame

class CrawlerNews:

    nasdaq = []
    korea_news_List = []

    def __init__(self):
        self.parser = 'html.parser'

    def process(self):
        # us_news_soup = self.get_articles('https://www.usnews.com/topics/subjects/stock-market')
        # self.crawling_us_news(us_news_soup)
        for page in range(1, 201):
            print(f'{page}회 시작')
            kr_news_soup = self.get_articles(f'https://vip.mk.co.kr/newSt/news/news_list.php?p_page={page}&sCode=21&termDatef=&search=&topGubun=')
            self.crawling_korea_news(kr_news_soup)
        # print(self.korea_news_links[0])
        # print(self.korea_news_titles[0])
        # print(self.korea_news_contents[0])
        # print(self.korea_news_regdates[0])
        self.makeCsv()
        

    def get_articles(self, url):
        response = urlopen(url)
        soup = BeautifulSoup(response, self.parser)
        return soup

    def crawling_us_news(self, soup):
        target = soup.find_all('h3', attrs={'class': 'story-headline'})
        print(f'us: {len(target)}')
        
    def crawling_korea_news(self, soup):
        target = soup.find_all('td', attrs={'class': 'title'})

        for t in target:
            tr = t.parent
            # url
            link = 'https:' + t.find('a').attrs['href']
            # self.korea_news_links.append(link)

            # title
            # title = t.find('a').text
            # self.korea_news_titles.append(title)

            # content
            news_detail = self.get_articles(link)
            content = str(news_detail.find('div', attrs={'id': 'Conts'}))
            content = re.sub("<(/)?([a-zA-Z]*)(\\s[a-zA-Z]*=[^>]*)?(\\s)*(/)?>", '', content)
            content = re.sub("googletag(.+?);", '', content)
            content = content[:content.find('[')]
            # self.korea_news_contents.append(content)

            # regdate
            regdate = tr.find('td', attrs={'class': 't_11_brown'}).text
            # self.korea_news_regdates.append(regdate)

            title = news_detail.find('div', attrs={'id': 'Titless'}).text

            subList = []

            subList.append(title)
            subList.append(content)
            subList.append(regdate)
            subList.append(link)
            self.korea_news_List.append(subList)

        
    def makeCsv(self):
        mycolumns = ['제목', '내용', '작성일자', 'url']
        frame = DataFrame(self.korea_news_List, columns=mycolumns)

        filename = './crawlingCsv/korea_news_list.csv'

        frame.to_csv(filename, index=False)

        print(filename + ' 파일 저장됨')

if __name__ == '__main__':
    c = CrawlerNews()
    c.process()

    