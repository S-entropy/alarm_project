import smtplib, imaplib
from email.mime.text import MIMEText
import email
from email.header import decode_header, make_header
import datetime
import time
from flet_coding.project.models.tables import User, Alarm, Alarm_repeat
from flet_coding.project.models.connect import session

def mail_sender(email, key, subject, msg):
    # smtplib.SMTP('사용할 SMTP 서버의 URL', PORT)
    smtp = smtplib.SMTP('smtp.gmail.com', 587)

    # TLS 암호화 (TLS 사용할 때에만 해당코드 입력)
    smtp.starttls()

    # smtp.login('메일 주소', '비밀번호')
    smtp.login(email, key)

    # 메일 내용 입력
    msg = MIMEText(msg)
    # 메일 제목 입력
    msg['Subject'] = subject

    smtp.sendmail(email, email, msg.as_string())

    smtp.quit()

def mail_reader(user, mail, key):
    mail_reader2(user, mail, key)
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(mail, key)
    imap.select("INBOX")

    # 사서함의 모든 메일의 uid 정보 가져오기
    # 만약 특정 발신 메일만 선택하고 싶다면 'ALL' 대신에 '(FROM "xxxxx@naver.com")' 입력
    status, messages = imap.uid('search', None, 'ALL')

    messages = messages[0].split()

    # 0이 가장 마지막 메일, -1이 가장 최신 메일
    recent_email = messages[-1]

    # fetch 명령어로 메일 가져오기
    res, msg = imap.uid('fetch', recent_email, "(RFC822)")

    # 사람이 읽을 수 있는 없는 상태의 이메일
    raw = msg[0][1]

    # 사람이 읽을 수 있는 형태로 변환
    raw_readable = msg[0][1].decode('utf-8')

    # raw_readable에서 원하는 부분만 파싱하기 위해 email 모듈을 이용해 변환
    email_message = email.message_from_string(raw_readable)

    # 보낸사람
    fr = make_header(decode_header(email_message.get('From')))

    # 메일 제목
    subject = make_header(decode_header(email_message.get('Subject')))

    # 메일 내용
    if email_message.is_multipart():
        for part in email_message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
    else:
        body = email_message.get_payload(decode=True)
    try:
        body = body.decode('utf-8')
    except:
        return False
    subject = list(str(subject).split())
    try:
        # 날짜 시간 당일반복 주간반복 순으로 입력
        ret = []
        data = body.strip()
        lis = list(subject[0].split('-'))
        alarm_date = datetime.date(int(lis[0]), int(lis[1]), int(lis[2]))
        lis = list(subject[1].split(':'))
        alarm_time = datetime.time(int(lis[0]), int(lis[1]))
        ret.extend([data, alarm_date, alarm_time])
        if len(subject) > 2:
            repeat_now = int(subject[2])
            ret.append(repeat_now)
        if len(subject) > 3:
            repeat_week = int(subject[3])
            ret.append(repeat_week)
    except Exception as e:
        print(False)
        return False
    if len(subject) <= 2:
        repeat_now = 0
    if len(subject) <= 3:
        repeat_week = 0
    alarm = list((Alarm.query.filter(Alarm.alarm_time == alarm_time).filter(Alarm.alarm_date == alarm_date)))
    if len(alarm) == 0:
        a = Alarm(repeat_now=repeat_now,
            repeat_week=repeat_week,
            alarm_date=alarm_date,
            alarm_time=alarm_time,
            data=data)
        if repeat_now:
            lis = list(subject[1].split(':'))
            rep_time = datetime.datetime(2023, 4, 29, int(lis[0]), int(lis[1]), 0)
            a.alarm_repeat.append(Alarm_repeat(repeat_interval=repeat_now, repeat_time=rep_time))
        user = (User.query.filter(User.id == user.id))[0]
        user.alarms.append(a)
        session.commit()
        print('success')
        mail_sender(mail, key, 'Alarm has succesfully added',
                    f'{alarm_time} {alarm_date} {repeat_now} {repeat_week} {data}')
    else:
        print('not unique')
    #return subject, body
def mail_reader2(user, mail, key):
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(mail, key)
    imap.select("INBOX")

    # 사서함의 모든 메일의 uid 정보 가져오기
    # 만약 특정 발신 메일만 선택하고 싶다면 'ALL' 대신에 '(FROM "xxxxx@naver.com")' 입력
    status, messages = imap.uid('search', None, 'ALL')

    messages = messages[0].split()

    # 0이 가장 마지막 메일, -1이 가장 최신 메일
    recent_email = messages[-1]

    # fetch 명령어로 메일 가져오기
    res, msg = imap.uid('fetch', recent_email, "(RFC822)")

    # 사람이 읽을 수 있는 없는 상태의 이메일
    raw = msg[0][1]

    # 사람이 읽을 수 있는 형태로 변환
    raw_readable = msg[0][1].decode('utf-8')

    # raw_readable에서 원하는 부분만 파싱하기 위해 email 모듈을 이용해 변환
    email_message = email.message_from_string(raw_readable)

    # 보낸사람
    fr = make_header(decode_header(email_message.get('From')))

    # 메일 제목
    subject = make_header(decode_header(email_message.get('Subject')))

    # 메일 내용
    if email_message.is_multipart():
        for part in email_message.walk():
            ctype = part.get_content_type()
            cdispo = str(part.get('Content-Disposition'))
            if ctype == 'text/plain' and 'attachment' not in cdispo:
                body = part.get_payload(decode=True)  # decode
                break
    else:
        body = email_message.get_payload(decode=True)
    try:
        body = body.decode('utf-8')
    except:
        return False
    subject = list(str(subject).split())
    try:
        # 날짜 시간 당일반복 주간반복 순으로 입력
        ret = []
        data = body.strip()
        if subject[0] != 'stop':
            print('delete fail')
            return
        lis = list(subject[1].split(':'))
        alarm_time = datetime.time(int(lis[0]), int(lis[1]))
        time_interval = int(subject[2])
    except Exception as e:
        print('delete fail')
        return False
    alarm_time = datetime.time(int(lis[0]), int(lis[1]))
    dt = datetime.datetime(2023,4,29,alarm_time.hour, alarm_time.minute, 0)
    alarm_repeats = Alarm_repeat.query.all()
    alarm_repeats = (Alarm_repeat.query.filter(Alarm_repeat.repeat_time == dt).filter(Alarm_repeat.repeat_interval == time_interval))
    print(len(list(alarm_repeats)))
    alarm_repeat = alarm_repeats[0]
    alarms = (Alarm.query.filter(Alarm.id == alarm_repeat.alarm_id))
    alarm = alarms[0]
    alarm_repeats = (Alarm_repeat.query.filter(Alarm_repeat.alarm_id == alarm.id))
    for alarm_repeat in alarm_repeats:
        session.delete(alarm_repeat)
    session.delete(alarm)
    print('delete success')
    mail_sender(mail, key, 'Alarm has succesfully deletd', '')
    #return subject, body
