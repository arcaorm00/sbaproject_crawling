import os, shutil
import sys
sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
basedir = os.path.abspath(os.path.dirname(__file__))
from urllib.request import urlopen
from bs4 import BeautifulSoup
import re
from pandas import DataFrame

class CrawlerArticles:

    naver_notice_list = []

    def __init__(self):
        self.parser = 'html.parser'

    def process(self):
        for page in range(1, 40):
            print(f'{page}페이지 시작')
            notice_soup = self.get_articles(f'https://ui.nboard2.naver.com/nboard2/list.nhn?n2_page={page}&n2_boardId=1100001004')
            self.crawling_naver_notices(notice_soup)
        print(len(self.naver_notice_list))
        self.makeCsv()
        

    def get_articles(self, url):
        response = urlopen(url)
        soup = BeautifulSoup(response, self.parser)
        return soup
        
    def crawling_naver_notices(self, soup):
        target = soup.find_all('div', attrs={'class': 'subject'})

        for t in target:

            try:
                a = str(t.find('a'))
                a_temp = a.split(',')
                a_temp = a_temp[-1]
                a_temp = a_temp.replace('&amp;', '&')
                a_temp = a_temp[a_temp.find("/"):a_temp.find("');")]
                # print(a_temp)
                
                link = 'https://ui.nboard2.naver.com' + a_temp
                if link == 'https://ui.nboard2.naver.com':
                    continue
                print(link)
                notice_detail = self.get_articles(link)

                # title
                title = notice_detail.find('h3', attrs={'class': 'title'}).text
                # print(title)

                # content
                content = str(notice_detail.find('div', attrs={'class': 'conts'}))
                
                # content = re.sub("<(/)?([a-zA-Z]*)(\\s[a-zA-Z]*=[^>]*)?(\\s)*(/)?>", '', content)
                # content = re.sub("<!--(.+?)-->", '', content)
                # content = re.sub("<(.+?)>", '', content)
                # print(content)

                # regdate
                regdate = notice_detail.find('div', attrs={'class': 'clipboard'})
                time = regdate.find('span', attrs={'class': 'time'}).text
                regdate = str(regdate)
                day = regdate[regdate.find('<div class="clipboard">'):regdate.find('<span class="time">')]
                day = day.replace('<div class="clipboard">', '')
                day = day.lstrip()
                regdate = day+time
                # print(regdate)

                subList = []

                subList.append(title)
                subList.append(content)
                subList.append(regdate)
                subList.append(link)
                self.naver_notice_list.append(subList)
            except:
                continue


    # csv 파일 저장    
    def makeCsv(self):
        mycolumns = ['제목', '내용', '작성일자', 'url']
        frame = DataFrame(self.naver_notice_list, columns=mycolumns)

        filename = './crawlingCsv/naver_notice.csv'

        frame.to_csv(filename, index=False)

        print(filename + ' 파일 저장됨')

if __name__ == '__main__':
    c = CrawlerArticles()
    c.process()

    