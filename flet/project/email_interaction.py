import smtplib
from email.mime.text import MIMEText

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

mail_sender('테스트', 'alarm_project')