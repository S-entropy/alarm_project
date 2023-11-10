import flet as ft

temporary: list[ft.Control] = []
login_pages: list[ft.Control] = []
def login_signup(page):
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    is_login = True

    def login(e):
        # 이름/메일 주소와 비밀번호가 일치하는지 확인, 일치하면 이하 실행
        page.remove(*login_pages, *temporary)
        ft.app(target=datas)
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

            t1 = ft.Container(content= ft.TextField(label='이름/메일 주소'), alignment= ft.alignment.center, width=500)
            t2 = ft.Container(content= ft.TextField(label='비밀번호'), alignment=ft.alignment.center, width=500)
            col = ft.Column(controls=[t1, t2])
            sb = ft.ElevatedButton(text='Submit', on_click=login)

            temporary = [col, sb]
            page.add(col, sb)
        else:
            page.remove(*temporary)

            t1 = ft.Container(content=ft.TextField(label='이름'), alignment=ft.alignment.center, width=500)
            t2 = ft.Container(content=ft.TextField(label='메일 주소'), alignment=ft.alignment.center, width=500)
            t3 = ft.Container(content=ft.TextField(label='비밀번호'), alignment=ft.alignment.center, width=500)
            col = ft.Column(controls=[t1, t2, t3])
            sb = ft.ElevatedButton(text='Submit', on_click=sign_up)

            temporary = [col, sb]
            page.add(col, sb)
        page.update()

    cg = ft.RadioGroup(content=ft.Column([
        ft.Radio(value=True, label='로그인'),
        ft.Radio(value=False, label="회원가입")]), on_change=radiogroup_changed)
    page.add(cg)
    login_pages.append(cg)

def datas(page):
    pass

ft.app(target=login_signup)