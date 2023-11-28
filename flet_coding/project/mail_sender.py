from flet_coding.project.models.tables import User, Alarm, Alarm_repeat
from flet_coding.project.models.connect import session
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
    delta_date = hour // 24
    hour %= 24
    if len(str(hour)) == 1:
        hour = '0' + str(hour)
    if len(str(minute)) == 1:
        minute = '0' + str(minute)
    return str(hour) + ':' + str(minute), delta_date
def test_fuction():
    now = datetime.datetime.now()
    print("test code- 현재 시간 출력하기")
    print(now)
    mail_sender('반복되는 메일은', '개발자를 불안하게 해요')

def repeat_times(repeat_time, repeat_interval, repeat_cnt):
    times = []
    curtime = repeat_time
    delta_date = 0
    for i in range(repeat_cnt):
        times.append(curtime)
        curtime, adds = get_added_time(times[-1], repeat_interval)
        delta_date += adds
    return times, delta_date

def check_date_type(date):
    return datetime.datetime.today().weekday() == date

def check_date(date):

    return date == datetime.datetime.now().date()

def mail_send(id):
    alarm = (Alarm.query.filter(Alarm.id == id))
    alarm = alarm[0]
    print(alarm.data)
    mail_sender('test', alarm.data)

alarms = (Alarm.query.all())
for alarm in alarms:
    now = datetime.datetime.now()
    #schedule.every().second.do(mail_send, alarm.id)
    if now.strftime('%Y-%m-%d') == alarm.alarm_date.strftime('%Y-%m-%d'):
        print(alarm.alarm_time.strftime('%H:%M:%S'))
        schedule.every().day.at(alarm.alarm_time.strftime('%H:%M:%S')).do(mail_send, alarm.id)

while True:
    schedule.run_pending()
    time.sleep(1)