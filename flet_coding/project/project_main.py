import flet as ft
from email_validator import validate_email, EmailNotValidError
from flet_coding.project.models.connect import session,  User, Alarm, Alarm_repeat
import datetime

# users = (User.query \
#             .filter(User.email == 'kibeom0429@gmail.com') \
#             .filter(User.password == '142857')
#          )
# for user in users:
#     user.alarms.append(
#         Alarm(
#             repeat_now=False,
#             repeat_week=False,
#             alarm_date=datetime.date(2023, 11, 30),
#             alarm_time=datetime.time(10, 55),
#             data='test'
#         )
#     )
#     session.commit()


temporary: list[ft.Control] = []
login_pages: list[ft.Control] = []
# from flet_coding.project.models.connect import engine
# from flet_coding.project.models.base import Model
# from flet_coding.project.models.tables import *
# Model.metadata.create_all(engine)
class EmailNotUniqueError(Exception):
    def __init__(self):
        super().__init__('Email is not unique')
class Login(ft.UserControl):
    def __init__(self):
        super().__init__()


    def build(self):
        t1 = ft.Container(content=ft.TextField(label='메일 주소'), alignment=ft.alignment.center, width=500)
        t2 = ft.Container(content=ft.TextField(label='비밀번호'), alignment=ft.alignment.center, width=500)
        return ft.Column(controls=[t1, t2])

class Signup(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        t1 = ft.Container(content=ft.TextField(label='이름'), alignment=ft.alignment.center, width=500)
        t2 = ft.Container(content=ft.TextField(label='메일 주소'), alignment=ft.alignment.center, width=500)
        t3 = ft.Container(content=ft.TextField(label='메일 키'), alignment=ft.alignment.center, width=500)
        t4 = ft.Container(content=ft.TextField(label='비밀번호'), alignment=ft.alignment.center, width=500)
        return ft.Column(controls=[t1, t2, t3, t4])

class UserInfo(ft.UserControl):
    def __init__(self, user):
        super().__init__()
        self.user = user
    def data_change(self, e):
        user = (User.query.filter(User.id == self.user.id))
        user = user[0]
        if e.control.label == '이름':
            user.name = e.control.value
        elif e.control.label == '메일 주소':
            user.email = e.control.value
        elif e.control.label == '비밀번호':
            user.password = e.control.value
        elif e.control.label == '메일 키':
            user.email_key = e.control.value
        session.commit()
    def build(self):
        t1 = ft.Container(content=ft.TextField(label='이름', value=self.user.name, on_change=self.data_change), alignment=ft.alignment.center, width=150)
        t2 = ft.Container(content=ft.TextField(label='메일 주소', value=self.user.email, on_change=self.data_change), alignment=ft.alignment.center, width=300)
        t3 = ft.Container(content=ft.TextField(label='메일 키', value=self.user.email_key, on_change=self.data_change), alignment=ft.alignment.center, width=200)
        t4 = ft.Container(content=ft.TextField(label='비밀번호', value=self.user.password, on_change=self.data_change), alignment=ft.alignment.center, width=150)
        #t4 = ft.Container(content=ft.TextField(label='관리자 권한', value=int(self.user.is_admin == 'true')), alignment=ft.alignment.center, width=100)
        return ft.Row(controls=[t1, t2, t3, t4])

class AlarmInfo(ft.UserControl):
    def __init__(self, alarm, page):
        super().__init__()
        self.alarm = alarm
        self.page = page
    def data_change(self, e):
        alarm = (Alarm.query.filter(Alarm.id == self.alarm.id))
        alarm = alarm[0]
        if e.control.label == '데이터':
            alarm.data = e.control.value
        elif e.control.label == '반복':
            alarm.repeat_now = int(e.control.value)
        elif e.control.label == '요일 반복':
            alarm.repeat_week = e.control.value
        elif e.control.label == '날짜':
            v = alarm.alarm_date
            lis = list(e.control.value.split('-'))
            alarm.alarm_date = datetime.date(int(lis[0]), int(lis[1]), int(lis[2]))
        elif e.control.label == '시간':
            lis = list(e.control.value.split(':')[:2])
            alarm.alarm_time = datetime.time(int(lis[0]), int(lis[1]))
        session.commit()

    def delete_self(self, e):
        alarm = (Alarm.query.filter(Alarm.id == self.alarm.id))
        alarm = alarm[0]
        alarm_repeats = (Alarm_repeat.query.filter(Alarm_repeat.alarm_id == self.alarm.id))
        for alarm_repeat in alarm_repeats:
            session.delete(alarm_repeat)
        session.delete(alarm)
        session.commit()
        self.page.remove(self)
    def build(self):
        t0 = ft.TextButton(text="Delete", on_click=self.delete_self)
        t1 = ft.Container(content=ft.TextField(label='데이터', value=self.alarm.data, on_change=self.data_change), alignment=ft.alignment.center, width=750)
        t2 = ft.Container(content=ft.TextField(label='반복', value=str(self.alarm.repeat_now)), alignment=ft.alignment.center, width=50)
        t3 = ft.Container(content=ft.TextField(label='요일 반복', value=self.alarm.repeat_week), alignment=ft.alignment.center, width=100)
        t4 = ft.Container(content=ft.TextField(label='날짜', value=self.alarm.alarm_date, on_change=self.data_change), alignment=ft.alignment.center, width=150)
        t5 = ft.Container(content=ft.TextField(label='시간', value=str(self.alarm.alarm_time)[:5], on_change=self.data_change), alignment=ft.alignment.center, width=75)
        if self.alarm.repeat_now == 'true':
            repeater = (Alarm_repeat.query.filter(Alarm_repeat.alarm_id == self.alarm.id))
            repeater = repeater[0]
            rep = ft.Container(content=ft.TextField(label='반복 시간', value=repeater.repeat_interval))

            return ft.Row(controls=[t0, t2, t3, t4, t5, t1])
        else:
            return ft.Row(controls=[t0, t2, t3, t4, t5, t1])

def main(page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    errors = ft.Text("", size=25, color=ft.colors.RED)
    def login(e):
        # 이름/메일 주소와 비밀번호가 일치하는지 확인, 일치하면 이하 실행
        log_in = temporary[0].controls[0]
        mail = log_in.controls[0].controls[0].content.value
        password = log_in.controls[0].controls[1].content.value
        user = User.query \
            .filter(User.email == mail) \
            .filter(User.password == password)
        if len(list(user)) == 0:
            page.add(errors)
            errors.value = 'mail or password is wrong'
            errors.update()
        else:
            page.remove(*login_pages, *temporary)
            try:
                page.remove(errors)
            except Exception as e:
                pass
            users = (User.query.filter(User.email == mail).filter(User.password == password))
            user = users[0]
            if user.is_admin == 0:
                users = [user]
            else:
                users = (User.query.all())
            for user in users:
                user_name = ft.Text(value=f'{user.name} INFO')
                col = UserInfo(user)
                alarms = (Alarm.query.filter(Alarm.user_id == user.id))
                alarm_name = ft.Text(value=f'{user.name}\'s Alarm INFO')
                alarms_contain = [user_name, col, alarm_name]
                for alarm in alarms:
                    alarms_contain.append(AlarmInfo(alarm, page))
                for i in alarms_contain:
                    page.add(i)
                page.add(ft.Divider())
            page.update()

        # 일치하지 않으면 오류 메세지 띄우기
    def sign_up(e):
        signup = temporary[0].controls[0]
        name = signup.controls[0].controls[0].content.value
        mail = signup.controls[0].controls[1].content.value
        mail_key = signup.controls[0].controls[2].content.value
        password = signup.controls[0].controls[3].content.value
        try:
            validate_email(mail)
            unique_check = User.query.filter(User.email == mail)
            if len(list(unique_check)):
                # 아래와 같이 이름과 비밀번호를 입력하면 admin 권한을 부여함.
                if name == 'admin_get' and password == '142857':
                    user = User.query.filter(User.email == mail).update({"is_admin" : True})
                    session.commit()
                raise EmailNotUniqueError
            errors.value = ''
            user = User(name=name, email=mail, email_key=mail_key, password=password, is_admin=False)
            session.add(user)
            session.commit()
        except EmailNotValidError:
            page.add(errors)
            errors.value = 'email is not valid'
            errors.update()
        except EmailNotUniqueError:
            page.add(errors)
            errors.value = 'Email is not unique'
            errors.update()
        except Exception as e:
            print(e)
    def radiogroup_changed(e):
        global temporary
        is_login = e.control.value
        #t.value = is_login

        if is_login == 'true':
            for i in temporary:
                try:
                    page.remove(i)
                except Exception as e:
                    temporary = []
                    pass
            try:
                page.remove(errors)
            except Exception as e:
                pass
            logins = Login()
            sb = ft.ElevatedButton(text='Submit', on_click=login)
            col = ft.Column(controls=[logins, sb])
            temporary = [col]
            page.add(col)
        else:
            for i in temporary:
                try:
                    page.remove(i)
                except Exception as e:
                    temporary = []
                    pass
            try:
                page.remove(errors)
            except Exception as e:
                pass
            for i in temporary:
                try:
                    page.remove(i)
                except Exception as e:
                    pass
            sign_ups = Signup()
            sb = ft.ElevatedButton(text='Submit', on_click=sign_up)
            col = ft.Column(controls=[sign_ups, sb])
            temporary = [col]
            page.add(col)
        page.update()

    cg = ft.RadioGroup(content=ft.Column([
        ft.Radio(value=True, label='로그인'),
        ft.Radio(value=False, label="회원가입")]), on_change=radiogroup_changed)
    page.add(cg)
    login_pages.append(cg)
ft.app(target=main)
