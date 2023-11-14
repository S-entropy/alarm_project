import smtplib, imaplib
from email.mime.text import MIMEText
import email
from email.header import decode_header, make_header

def mail_sender(subject, msg):
    # smtplib.SMTP('사용할 SMTP 서버의 URL', PORT)
    smtp = smtplib.SMTP('smtp.gmail.com', 587)

    # TLS 암호화 (TLS 사용할 때에만 해당코드 입력)
    smtp.starttls()

    # smtp.login('메일 주소', '비밀번호')
    smtp.login('kibeom0429@gmail.com', 'bolulxcmhbhmxunf')

    # 메일 내용 입력
    msg = MIMEText(msg)
    # 메일 제목 입력
    msg['Subject'] = subject

    smtp.sendmail('kibeom0429@gmail.com', 'kibeom0429@gmail.com', msg.as_string())

    smtp.quit()

def mail_reader(mail):
    imap = imaplib.IMAP4_SSL('imap.gmail.com')
    imap.login(mail, 'bolulxcmhbhmxunf')
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

    body = body.decode('utf-8')
    return subject, body
if __name__ == '__main__':
    mail_sender('테스트', 'alarm_project')
    subject, body = mail_reader('kibeom0429@gmail.com')
    print(subject)
    print(body)