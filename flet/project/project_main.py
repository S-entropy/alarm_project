import flet as ft

temporary: list[ft.Control] = []
login_pages: list[ft.Control] = []

class Login(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        t1 = ft.Container(content=ft.TextField(label='이름/메일 주소'), alignment=ft.alignment.center, width=500)
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
    def login(e):
        # 이름/메일 주소와 비밀번호가 일치하는지 확인, 일치하면 이하 실행
        page.remove(*login_pages, *temporary)

        # 일치하지 않으면 오류 메세지 띄우기
    def sign_up(e):
        # 데이터베이스에 이름, 메일 주소, 비밀번호 추가
        pass
    def radiogroup_changed(e):
        global temporary
        is_login = e.control.value
        #t.value = is_login
        if is_login == 'true':
            page.remove(*temporary)

            logins = Login()
            sb = ft.ElevatedButton(text='Submit', on_click=login)
            col = ft.Column(controls=[logins, sb])

            temporary = [col]
            page.add(col)
        else:
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