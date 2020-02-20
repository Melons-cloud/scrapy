import requests
from bs4 import BeautifulSoup
import csv
import datetime

url ='https://www.bilibili.com/ranking'
# 发起网络请求
response = requests.get(url)
html_text=response.text
soup = BeautifulSoup(html_text,'html.parser')

# 保存视频信息的对象
class Video:
    def __init__(self,rank,title,score,visit,up,up_id,url):
        self.rank=rank
        self.title=title
        self.score=score
        self.visit = visit
        self.up = up
        self.up_id =up_id
        self.url =url
    def to_csv(self):
        return [self.rank,self.title,self.score,self.visit,self.up,self.up_id,self.url]
    @staticmethod
    def csv_title():
        return ['排名','标题','分数','播放量','Up主','Up Id','url']

#提取列表
items=soup.findAll('li',{'class':'rank-item'})
# 保存提取出来的Video列表
videos = []
for itm in items:
    title=itm.find('a',{'class':'title'}).text
    score = itm.find('div',{'class':'pts'}).find('div').text
    rank  = itm.find('div',{'class':'num'}).text
    visit = itm.find('span',{'class':'data-box'}).text
    up = itm.find_all('a')[2].text
    up_id = itm.find_all('a')[2].get('href')[len('//space.bilibili.com/'):]
    url = itm.find('a',{'class':'title'}).get( 'href' )
    v =Video(rank,title,score,visit,up,up_id,url)
    videos.append(v)
now_str =datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
file_name=f'top100_{now_str}.csv'
with open(file_name,'w',newline='',encoding='gb18030') as f:
    pen=csv.writer(f)
    pen.writerow(Video.csv_title())
    for v in videos:
        pen.writerow(v.to_csv())