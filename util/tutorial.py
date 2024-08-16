import flet as ft
from generator.generar_datos import translations

class Tutorial:
    def __init__(self, app, page):
        self.app = app
        self.page = page
        self.current_step = 0
        self.steps = [
            self.intro_step,
            self.create_human_step,
            self.view_human_info_step,
            self.interact_human_step,
            self.make_human_sick_step,
            self.cure_human_step,
            self.delete_human_step,
            self.next_day_step,
            self.cause_event_step,
            self.configure_colors_step
        ]
        self.current_button = 0
        self.dialog = None
        self.overlay = None
        self.arrow = None

    def start_tutorial(self):
        self.current_step = 0
        self.current_button += 1
        self.show_current_step()

    def show_current_step(self):
        self.steps[self.current_step]()

    def show_final_step(self):
        self.dialog = ft.AlertDialog(
            title=ft.Text("Diviertete!"),
            content=ft.Text("Disfruta de la experiencia en Have Decisions!"),
            actions=[
                ft.ElevatedButton("Anterior", on_click=self.previous_step),
                ft.ElevatedButton("Finalizar", on_click=self.end_tutorial),
            ],
        )
        self.app.page.dialog = self.dialog
        self.dialog.open = True
        self.app.page.update()

    def next_step(self, a):
        if self.current_step < len(self.steps) - 1:
            self.current_step += 1
            self.show_current_step()
        else:
            self.show_final_step()

    def previous_step(self, e):
        if self.current_step > 0:
            self.current_step -= 1
            self.show_current_step()

    def end_tutorial(self, e):
        self.remove_highlight()
        if self.dialog:
            self.dialog.open = False
            self.app.page.update()

    def highlight_button(self, button_name):
        self.remove_highlight()
        
        # Crear un overlay oscuro
        self.overlay = ft.Container(
            expand=True,
            bgcolor=ft.colors.BLACK54,
        )
        
        # Crear una flecha que apunte al botón
        self.arrow = ft.Container(
            content=ft.Text("<--", size=30),
            alignment=ft.alignment.center_right,
        )
        
        elemento = self.page.get_control(self.app.panel_izquierdo.content.controls[0].controls[1])
        print(elemento)
        if elemento:
            print(f"Propiedades del elemento: {elemento.__dict__}")
            if hasattr(elemento, 'top') and hasattr(elemento, 'left'):
                print(f"La posición del elemento es: x={elemento.left}, y={elemento.top}")
            else:
                print("El elemento no tiene propiedades 'top' y 'left'")
        else:
            print("No se pudo obtener el elemento")

        # Obtener el botón correspondiente del panel izquierdo
        # target_button =self.app.panel_izquierdo.content.controls[0].controls[0]
        # if target_button and target_button.left is not None:
        #     # Posicionar la flecha junto al botón
        #     self.arrow.top = target_button.offset.x -30
        #     self.arrow.right = target_button.left.y 
        # else:
        #      print("Warning: Could not position arrow. Target button or its left property is None.")
        
        # Añadir el overlay y la flecha a la página
        self.app.page.overlay.extend([self.overlay, self.arrow])
        self.app.page.update()

    def remove_highlight(self):
        if self.overlay and self.arrow:
            self.app.page.overlay.remove(self.overlay)
            self.app.page.overlay.remove(self.arrow)
            self.app.page.update()

    def show_dialog(self, title, content, button_to_highlight=None):
        self.remove_highlight()
        if button_to_highlight:
            self.highlight_button(button_to_highlight)
        
        self.dialog = ft.AlertDialog(
            title=ft.Text(title),
            content=ft.Container(
                content=ft.Text(content),
                width=600,
                padding=10
            ),
            actions=[
                ft.ElevatedButton("Anterior", on_click=self.previous_step),
                ft.ElevatedButton("Siguiente", on_click=self.next_step),
                ft.ElevatedButton("Finalizar", on_click=self.end_tutorial),
            ],
        )
        self.app.page.dialog = self.dialog
        self.dialog.open = True
        self.app.page.update()

    def intro_step(self):
        self.show_dialog(
            "Have desissions",
            "Esta aplicación te permite crear y gestionar una población de humanos virtuales. "
            "Te guiaremos a través de las principales funciones."
        )

    def create_human_step(self):
        self.show_dialog(
            "Crear un Humano",
            "Con el botón azul que está en el panel izquierdo puedes crear un humano, esté tendrá atributos, y cualidades que lo harán especial",
            button_to_highlight=translations["create_human_btn"]
        )

    def view_human_info_step(self):
        self.show_dialog(
            "Ver Información de un Humano",
            "Al crear al humano, en el panel central aparecerá su nombre, si le das click al icono que sale junto a su nombre, podrás ver su información"
        )

    def interact_human_step(self):
        self.show_dialog(
            "Interactuar con un Humano",
            "Dentro de las opciones del humano encontrarás varios botónes, interactuar sirve para realizar acciones que hacen que el humano interactue con su ambiente, como trabajar o hablar con otro humano"
        )

    def make_human_sick_step(self):
        self.show_dialog(
            "Enfermar a un Humano",
            "También puedes enfermar a un humano, dentro de opciones tocas el botón de enfermar y seleccionas una enfermedad, desde este momento el humano padece dicha enfermedad"
        )

    def cure_human_step(self):
        self.show_dialog(
            "Curar a un Humano",
            "Así como es posible enfermarlo, también puedes sanarlo con el botón sanar, y seleccionar la enfermedad que le quieres curar"
        )

    def delete_human_step(self):
        self.show_dialog(
            "Eliminar un Humano",
            "Volviendo al panel izquierdo, si le das al botón eliminar humano, en el panel derecho saldrán todos los humanos que puedes eliminar",
            button_to_highlight=translations["delete_human_btn"]
        )

    def next_day_step(self):
        self.show_dialog(
            "Avanzar al Siguiente Día",
            "Con el botón de avanzar día podrás hacer que un día pase en tu simulación, cada día puede tener eventos, hacer que los humanos mueran o enfermen, tengan una profesión y cambia el clima, cada 10 días se cambia de estación",
            button_to_highlight=translations["advance_day_btn"]
        )

    def cause_event_step(self):
        self.show_dialog(
            "Ocasionar un Evento",
            "Con el botón de ocasionar evento podrás ocasionar un evento específico que afectará a los humanos de tu simulación.",
            button_to_highlight=translations["event_btn"]
        )

    def configure_colors_step(self):
        self.show_dialog(
            "Configurar Colores",
            "Si no te gustan los colores que vez en pantalla puedes personalizarlo a tu estilo desde el botón de configuración",
            button_to_highlight=translations["config_btn"]
        )