import requests
from bs4 import BeautifulSoup
import os
import telegram
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=3)
def timed_job():
    print('This job is run every three minutes.')

sched.start()

bot = telegram.Bot(token='849308859:AAF7aPnWtSjI8evIQIU4od1tA6vZgpEwjzg')
chat_id = bot.getUpdates()[-1].message.chat.id

# 파일의 위치
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

req = requests.get('https://www.konyang.ac.kr/cop/bbs/BBSMSTR_000000000582/selectBoardList.do')
req.encoding = 'utf-8' # Clien에서 encoding 정보를 보내주지 않아 encoding옵션을 추가해줘야합니다.

html = req.text
soup = BeautifulSoup(html, 'html.parser')
posts = soup.select('table > tbody > tr:nth-child(1) > td.left > div > span.link > a > b')
links = soup.select('table > tbody > tr:nth-child(1) > td.left > div > span.link > a ')
latest=posts[0].text
latestlink=links[0]['href']
print(latest)
print(latestlink)
url = 'https://www.konyang.ac.kr' + latestlink

with open(os.path.join(BASE_DIR, 'latest.txt'), 'r+') as f_read:
    before = f_read.readline()
    if before != latest:
        bot.sendMessage(chat_id=chat_id, text='새 글이 올라왔어요!')
        bot.sendMessage(chat_id=chat_id, text=latest)
        bot.sendMessage(chat_id=chat_id, text=url)
    else: 
        bot.sendMessage(chat_id=chat_id, text='새 글이 없어요 ㅠㅠ')   
    f_read.close()

with open(os.path.join(BASE_DIR, 'latest.txt'), 'w+') as f_write:
    f_write.write(latest)
    f_write.close()

