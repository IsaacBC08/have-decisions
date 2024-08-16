import flet as ft

class ColorTextField(ft.TextField):
    def __init__(self, label, value, **kwargs):
        super().__init__(
            label=label,
            value=value,
            on_change=self.validate_input,
            max_length=7,
            **kwargs
        )

    def validate_input(self, e):
        if not self.value.startswith('#'):
            self.value = '#' + self.value
        if len(self.value) > 7:
            self.value = self.value[:7]
        self.update()