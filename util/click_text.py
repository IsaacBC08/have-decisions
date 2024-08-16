import flet as ft


class ClickText(ft.UserControl):
    def __init__(self, text: str, width: float, color: str = ft.colors.BLACK, on_click=None):
        super().__init__()
        self.text = text
        self.width = width
        self.color = color
        self.on_click = on_click

    def build(self):
        return ft.TextButton(
            text=self.text,
            width=self.width,
            style=ft.ButtonStyle(
                color={ft.MaterialState.DEFAULT: self.color},
                bgcolor={ft.MaterialState.DEFAULT: ft.colors.TRANSPARENT},
                overlay_color={ft.MaterialState.HOVERED: ft.colors.TRANSPARENT},
                padding={ft.MaterialState.DEFAULT: 0},
            ),
            content=ft.Container(
                content=ft.Text(self.text, text_align=ft.TextAlign.LEFT),
                alignment=ft.alignment.center_left
            ),
            on_click=self.on_click
        )