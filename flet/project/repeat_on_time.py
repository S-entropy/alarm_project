import schedule
import time
import datetime
from email_interaction import mail_sender

# 스케쥴 모듈이 동작시킬 코드 : 현재 시간 출력
def get_added_time(time, interval):
    hour, minute = map(int, time.split(':'))
    minute += interval
    if minute >= 60:
        hour += minute // 60
        minute %= 60
    hour %= 24
    if len(str(hour)) == 1:
        hour = '0' + str(hour)
    if len(str(minute)) == 1:
        minute = '0' + str(minute)
    return str(hour) + ':' + str(minute)
def test_fuction():
    now = datetime.datetime.now()
    print("test code- 현재 시간 출력하기")
    print(now)
    mail_sender('반복되는 메일은', '개발자를 불안하게 해요')

def repeat_alarm(repeat_time, repeat_interval):
    times = []
    curtime = repeat_time
    for i in range(100):
        times.append(curtime)
        curtime = get_added_time(times[-1], repeat_interval)
    return times



for alarm_time in repeat_alarm('13:35', 1):
    schedule.every().day.at(alarm_time).do(test_fuction)
schedule.every().day.at("13:37").do(test_fuction)
while True:
    schedule.run_pending()
    time.sleep(1)
