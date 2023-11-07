import flet as ft
from sidebar import Sidebar


def main(page: ft.Page):
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    divide = ft.Row(controls=[ft.TextField(label='a'), ft.TextField(label='b')])
    # app = Sidebar(page)
    # page.update(app)
    page.add(divide)
    page.update()
ft.app(target=main)