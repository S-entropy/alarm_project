from flet_coding.project.models.tables import User, Alarm, Alarm_repeat
from flet_coding.project.models.connect import session
import schedule
import time
import datetime
from email_interaction import mail_sender, mail_reader
import streamlit as st

def alarm_deleter(alarm):
    session.delete(alarm)

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
def alarm_check():
    session.commit()
    alarms = (Alarm.query.all())
    now = datetime.datetime.now()
    for alarm in alarms:
        print(alarm.alarm_time)
        if now.strftime('%Y-%m-%d %H:%M') == alarm.alarm_date.strftime('%Y-%m-%d')+alarm.alarm_time.strftime(' %H:%M'):
            if alarm.repeat_now:
                alarm_repeat = alarm.alarm_repeat
                alarm_repeat = alarm_repeat[0]
                v = alarm_repeat.repeat_interval
                v1 = v//60
                v2 = v%60
                dt = datetime.datetime(year=alarm.alarm_date.year, month=alarm.alarm_date.month, day=alarm.alarm_date.day,
                                       hour=alarm.alarm_time.hour, minute=alarm.alarm_time.minute)
                dt = dt + datetime.timedelta(hours=v1, minutes=v2)
                alarm.alarm_date = datetime.date(dt.year, dt.month, dt.day)
                alarm.alarm_time = datetime.time(dt.hour, dt.minute)
            elif alarm.repeat_week:
                dates = []
                v = alarm.repeat_week
                for i in range(7):
                    dates.append(v % 10)
                    v //= 10
                dates.reverse()
                dates = dates + dates
                cur = datetime.datetime.today().weekday() + 1
                while True:
                    if dates[cur]:
                        break
                    else:
                        cur+=1
                delta = cur - datetime.datetime.today().weekday()
                alarm.alarm_date = alarm.alarm_date + datetime.timedelta(days=delta)
            else:
                session.delete(alarm)
            mail_send(alarm.id)
            session.commit()

def mail_send(id):
    alarm = (Alarm.query.filter(Alarm.id == id))
    alarm = alarm[0]
    user = (User.query.filter(User.id == alarm.user_id))[0]
    d = alarm.alarm_date
    t = alarm.alarm_time
    mail_sender(user.email, user.email_key, f'Check For alarm', alarm.data)

alarms = (Alarm.query.all())
schedule.every(10).seconds.do(alarm_check)


users = (User.query.all())
for user in users:
    schedule.every(10).seconds.do(mail_reader, user, user.email, user.email_key)
while True:
    schedule.run_pending()
    time.sleep(1)
