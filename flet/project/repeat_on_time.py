import schedule
import time
import datetime
from email_interaction import mail_sender

# 스케쥴 모듈이 동작시킬 코드 : 현재 시간 출력
def test_fuction():
    now = datetime.datetime.now()
    print("test code- 현재 시간 출력하기")
    print(now)
    mail_sender('반복되는 메일은', '개발자를 불안하게 해요')


#schedule.every(1).second.do(test_fuction)
schedule.every().day.at("10:10").do(test_fuction)

while True:
    schedule.run_pending()
    time.sleep(1)
