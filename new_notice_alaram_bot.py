import requests
from bs4 import BeautifulSoup
import telegram
import codecs
from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()

# @sched.scheduled_job('interval', minutes=3)
@sched.scheduled_job('cron', day_of_week='mon-fri', hour=16)
def timed_job():
    notice()

def notice():
    bot = telegram.Bot(token='849308859:AAF7aPnWtSjI8evIQIU4od1tA6vZgpEwjzg')
    # chat_id = bot.getUpdates()[-1].message.chat.id
    chat_id = '-1001437224598'

    req = requests.get('https://www.konyang.ac.kr/cop/bbs/BBSMSTR_000000000582/selectBoardList.do')
    req.encoding = 'utf-8'

    html = req.text
    soup = BeautifulSoup(html, 'html.parser')
    posts = soup.select('table > tbody > tr:nth-child(1) > td.left > div > span.link > a > b')
    # links = soup.select('table > tbody > tr:nth-child(1) > td.left > div > span.link > a ')
    latest=posts[0].text
    # latestlink=links[0]['href']
    print(latest)
    # print(latestlink)
    url = 'https://www.konyang.ac.kr/cop/bbs/BBSMSTR_000000000582/selectBoardList.do'

    with open('./latest.txt', 'r', encoding='utf-8') as f_read:
        before = f_read.readline()
        if before != latest:
            bot.sendMessage(chat_id=chat_id, text='새 글이 올라왔어요!')
            bot.sendMessage(chat_id=chat_id, text=latest)
            bot.sendMessage(chat_id=chat_id, text=url)
        else: 
            bot.sendMessage(chat_id=chat_id, text='새 글이 없어요 ㅠㅠ')   
        f_read.close()

    with open('./latest.txt', 'w+', encoding='utf-8') as f_write:
        f_write.write(latest)
        f_write.close()

sched.start()
# notice()
#heroku ps:scale clock=1
# heroku git:clone -a limitless-cove-32728 파일체크