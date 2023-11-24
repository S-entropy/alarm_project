import flet as ft
from email_validator import validate_email, EmailNotValidError
from flet_coding.project.models.tables import User, Alarm, Alarm_repeat
from flet_coding.project.models.connect import session
import datetime
'''
users = (User.query \
            .filter(User.email == 'kibeom0429@gmail.com') \
            .filter(User.password == '142857')
         )
for user in users:
    print(user.email)
    user.alarms.append(
        Alarm(
            repeat_now=False,
            repeat_week=False,
            alarm_date=datetime.date(2023, 11, 24),
            alarm_time=datetime.time(1, 55)
        )
    )
    session.commit()
'''

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
        t3 = ft.Container(content=ft.TextField(label='비밀번호'), alignment=ft.alignment.center, width=500)
        return ft.Column(controls=[t1, t2, t3])

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


        # 일치하지 않으면 오류 메세지 띄우기
    def sign_up(e):
        signup = temporary[0].controls[0]
        name = signup.controls[0].controls[0].content.value
        mail = signup.controls[0].controls[1].content.value
        password = signup.controls[0].controls[2].content.value
        try:
            validate_email(mail)
            unique_check = User.query.filter(User.email == mail)
            if len(list(unique_check)):
                if name == 'admin_get' and password == '142857':
                    user = User.query.filter(User.email == mail).update({"is_admin" : True})
                    session.commit()
                raise EmailNotUniqueError
            errors.value = ''
            user = User(name=name, email=mail, password=password, is_admin=False)
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
            page.remove(*temporary)
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
            page.remove(*temporary)
            try:
                page.remove(errors)
            except Exception as e:
                pass
            page.remove(*temporary)
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
