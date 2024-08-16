# Python
import threading
import time
from screeninfo import get_monitors
# Flet
import flet as ft 
from util.redirect_text import StdoutRedirector
from util.color_field import ColorTextField
from util.tutorial import Tutorial
from util.click_text import ClickText
# Proyecto
from actores.humanos import *
from core.dia import *
from core.objetos import *
from generator.generar_datos import *
from settings.user import *
from util.timer import change_timer

monitor = get_monitors()[0]
screen_width = monitor.width
screen_height = monitor.height

def change_timer():
    wait(1)
    return False
    
class App:
    def __init__(self):
        self.timer = False
        self.humano_seleccionado = None
        self.dia = Dia(eventos)
        self.dia.ESTACIONES = translations["seasons"]
        self.hnis = len(self.dia.humanos_vivos)
        self.pagina_actual = 0
        self.lista_mostrada = "ninguna"
        self.idioma = "es"
    
    def update_size(self, e):
        print("vh:",self.page.window.height,"px")
        print("vw:",self.page.window.width, "px")
        self.build()
        self.page.update

    def start_timer(self,seconds):
        time.sleep(seconds) 
        self.timer = False
        self.page.update()

    def shortcuts(self, e: ft.KeyboardEvent):
        if e.key == "F11":  # se ha presionado F11
            self.page.window.full_screen = not self.page.window.full_screen  # Alterna pantalla completa
            self.page.update()

    def porcentuar_medidas(self, porcentajew, porcentajeh):
        return (self.page.width * (porcentajew / 100), self.page.height * (porcentajeh / 100))

    def start_tutorial(self, e):
        self.tutorial.start_tutorial()

    def otros_humanos(self) -> list: return [h for h in self.dia.humanos_vivos if h != self.humano_seleccionado]
    
    def crear_botones_navegacion(self, lista, tipo):
        return ft.Row([
            ft.IconButton(
                icon=ft.icons.ARROW_BACK,
                on_click=lambda _: self.pagina_anterior(lista, tipo),
                disabled=self.pagina_actual == 0,
                icon_color=COLORS['icon_color']
            ),
            ft.Text(f"{translations["page"]} {self.pagina_actual + 1}", color=COLORS['text_color']),
            ft.IconButton(
                icon=ft.icons.ARROW_FORWARD,
                on_click=lambda _: self.pagina_siguiente(lista, tipo),
                disabled=(self.pagina_actual + 1) * 5 >= len(lista),
                icon_color=COLORS['icon_color']
            )
        ])
    
    def actualizar_lista(self, tipo):
        if tipo == "interaccion":
            self.mostrar_lista_interaccion()
        elif tipo == "enfermedades":
            self.mostrar_lista_enfermedades()
        elif tipo == "kills":
            self.mostrar_lista_eliminables()
        elif tipo == "hablar":
            self.mostrar_lista_hablar()
        elif tipo == "eventos":
            self.mostrar_lista_eventos()
        elif tipo == "enfermedades_humanas":
            self.mostrar_lista_enfermedades_humano(self.humano_seleccionado)
        elif tipo == "hablables":
            self.mostrar_lista_hablar()
        elif tipo == "insultar":
            self.mostrar_lista_insultar()
        elif tipo == "ligar":
            self.mostrar_lista_ligar()

    def pagina_anterior(self, lista, tipo):
        if self.pagina_actual > 0:
            self.pagina_actual -= 1
            self.actualizar_lista(tipo)
    
    def pagina_siguiente(self, lista, tipo):
        if (self.pagina_actual + 1) * 5 < len(lista):
            self.pagina_actual += 1
            self.actualizar_lista(tipo)

    def mostrar_lista_interaccion(self):
        if self.lista_mostrada != "interact":
            self.pagina_actual = 0
        self.lista_mostrada = "interact"
        
        botones = []
        
        # Botón general para todos
        botones.append(ft.ElevatedButton(
            text=translations["talk_someone"],
            icon=ft.icons.CHAT,
            on_click=lambda _: self.mostrar_lista_hablar(),
            bgcolor=COLORS['bgc_btn_talk_someone'],
            color=COLORS['text_color']
        ))
        # Botón general para todos
        botones.append(ft.ElevatedButton(
            text=translations["flirt"],
            icon=ft.icons.FAVORITE,
            icon_color=COLORS["flirt_icon"],
            on_click=lambda _: self.mostrar_lista_ligar(),
            bgcolor=COLORS['bgc_btn_flirt'],
            color=COLORS['text_color']
        ))
        botones.append(ft.ElevatedButton(
            text=translations["hate"],
            icon=ft.icons.SENTIMENT_DISSATISFIED,
            on_click=lambda _: self.mostrar_lista_insultar(),
            bgcolor=COLORS['bgc_btn_insult'],
            color=COLORS['text_color']
        ))
        
        # Botones específicos según la profesión
        if self.humano_seleccionado.profesion:
            botones.append(ft.ElevatedButton(
                text="Trabajar",
                icon=ft.icons.BUILD,
                on_click=lambda _: self.humano_seleccionado.trabajar(),
                bgcolor=COLORS['bgc_btn_work'],
                color=COLORS['text_color']
            ))
        if self.humano_seleccionado.profesion == "Doctor":
            botones.append(ft.ElevatedButton(
                text="Curar",
                icon=ft.icons.HEALING,
                on_click=lambda _: self.curar(),
                bgcolor=COLORS['bgc_btn_work_cure'],
                color=COLORS['text_color']
            ))
        if self.humano_seleccionado.profesion == "Policia":
            botones.append(ft.ElevatedButton(
                text="Arrestar",
                icon=ft.icons.GAVEL,
                on_click=lambda _: self.arrestar(),
                bgcolor=COLORS['bgc_btn_work_arrest'],
                color=COLORS['text_color']
            ))
        if self.humano_seleccionado.profesion == "Criminal":
            botones.append(ft.ElevatedButton(
                text="Matar",
                on_click=lambda _: self.matar(),
                bgcolor=COLORS['bgc_btn_work_kill'],
                color=COLORS['text_color']
            ))
        
        contenido_panel = ft.Column([
            ft.Text(f"{translations["interact_actions_label"]} {self.humano_seleccionado.mapear_nombre()}:", 
                    size=16, weight="bold", color=COLORS['text_color']),
            ft.Column(botones, spacing=10)
        ])

        self.panel_derecho.content = contenido_panel
        self.actualizar_lista(self.lista_mostrada)
        self.page.update()

    def mostrar_lista_enfermedades(self, e=None):
        if self.lista_mostrada != "enfermedades":
            self.pagina_actual = 0
        self.lista_mostrada = "enfermedades"
        inicio = self.pagina_actual * 5
        fin = inicio + 5
        enfermedades_pagina = enfermedades[inicio:fin]
        lista_enfermedades = ft.Column(controls=[
            ft.ElevatedButton(
                text=enfermedad, 
                width=self.porcentuar_medidas(20,0)[0], 
                bgcolor=COLORS["bgc_btn_select_sick"], 
                color=COLORS['fc_btn'], 
                on_click=lambda _, enfermedad=enfermedad: self.seleccionar_enfermedad(enfermedad)
            ) for enfermedad in enfermedades_pagina
        ], spacing=15)
        botones_navegacion = self.crear_botones_navegacion(enfermedades, "enfermedades")
        contenido = ft.Column(controls=[
            ft.Text(translations["choose_illness"], size=16, weight="bold", color=COLORS['text_color']), 
            lista_enfermedades, 
            botones_navegacion
        ])
        self.panel_derecho.content = contenido
        
        self.page.update()

    def mostrar_lista_eventos(self, e=None):
        if self.lista_mostrada != "eventos":
            self.pagina_actual = 0
        self.lista_mostrada = "eventos"
        inicio = self.pagina_actual * 5
        fin = inicio + 5
        eventos_pagina = eventos[inicio:fin]
        lista_eventos = ft.Column(controls=[
            ft.ElevatedButton(
                text=evento["nombre"], 
                width=self.porcentuar_medidas(20,0)[0], 
                bgcolor=COLORS["bgc_btn_select_event"], 
                color=COLORS['fc_btn'], 
                on_click=lambda _, evento=evento: self.seleccionar_evento(evento)
            ) for evento in eventos_pagina
        ], spacing=15)
        botones_navegacion = self.crear_botones_navegacion(eventos, "eventos")
        contenido = ft.Column(controls=[
            ft.Text(translations["select_event_label"], size=16, weight="bold", color=COLORS['text_color']), 
            lista_eventos, 
            botones_navegacion
        ])
        self.panel_derecho.content = contenido
        self.page.update()

    def mostrar_lista_eliminables(self, e=None):
        if self.lista_mostrada != "kills":
            self.pagina_actual = 0
        self.lista_mostrada = "kills"
        todos_humanos = self.dia.humanos_vivos
        inicio = self.pagina_actual * 5
        fin = inicio + 5
        humanos_pagina = todos_humanos[inicio:fin]

        lista_humanos = ft.Column(
            controls=[
                ft.Row([
                    ft.Text(f"{otro_humano.mapear_nombre()}", color=COLORS['text_color']),
                    ft.ElevatedButton(
                        text="Matar",
                        on_click=lambda _, h2=otro_humano: self.matar_humano(h2),
                        bgcolor=COLORS['bgc_btn_select_kill'], color=COLORS['text_color']
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN) for otro_humano in humanos_pagina
            ],
            spacing=10,
            scroll=ft.ScrollMode.AUTO
        )

        botones_navegacion = self.crear_botones_navegacion(todos_humanos, "kills")

        contenido_panel = ft.Column([
            ft.Text("Lista de todos los humanos vivos:", size=16, weight="bold", color=COLORS['text_color']),
            lista_humanos,
            botones_navegacion
        ])

        self.panel_derecho.content = contenido_panel
        self.page.update()
    
    def mostrar_lista_enfermedades_humano(self, humano, e=None):
        if self.lista_mostrada != "enfermedades_humanas":
            self.pagina_actual = 0
        self.lista_mostrada = "enfermedades_humanas"
        inicio = self.pagina_actual * 5
        fin = inicio + 5
        enfermedades_pagina = humano.enfermedades[inicio:fin]
        lista_enfermedades = ft.Column(controls=[
            ft.ElevatedButton(
                text=enfermedad, 
                width=self.porcentuar_medidas(20,0)[0], 
                bgcolor=COLORS["bgc_btn_select_sick_cure"], 
                color=COLORS['fc_btn'], 
                on_click=lambda _, enfermedad=enfermedad: self.seleccionar_curar(enfermedad)
            ) for enfermedad in enfermedades_pagina
        ], spacing=15)
        botones_navegacion = self.crear_botones_navegacion(humano.enfermedades, "enfermedades")
        contenido = ft.Column(controls=[
            ft.Text(f"{translations["choose_cure_illness"]} {humano.mapear_nombre()}", size=16, weight="bold", color=COLORS['text_color']), 
            lista_enfermedades, 
            botones_navegacion
        ])
        self.panel_derecho.content = contenido
        self.page.update()

    def mostrar_lista_hablar(self, e=None):
        if self.lista_mostrada != "hablables":
            self.pagina_actual = 0
        self.lista_mostrada = "hablables"
        otros_humanos = self.otros_humanos()
        inicio = self.pagina_actual * 5
        fin = inicio + 5
        humanos_pagina = otros_humanos[inicio:fin]
        lista_humanos = ft.Column(controls=[
            ft.ElevatedButton(
                text=humano.mapear_nombre(), 
                width=self.porcentuar_medidas(20,0)[0], 
                bgcolor=COLORS["bgc_btn_select_talk"], 
                color=COLORS['fc_btn'], 
                on_click=lambda _: self.humano_seleccionado.interactuar(humano, "amistad")
            ) for humano in humanos_pagina
        ], spacing=15)
        botones_navegacion = self.crear_botones_navegacion(otros_humanos, "hablar")
        contenido = ft.Column(controls=[
            ft.Text(f"{translations["choose_talk"]} {self.humano_seleccionado.mapear_nombre()}", size=16, weight="bold", color=COLORS['text_color']), 
            lista_humanos, 
            botones_navegacion
        ])
        self.panel_derecho.content = contenido
        self.page.update()

    def mostrar_lista_ligar(self, e=None):
        if self.lista_mostrada != "ligar":
            self.pagina_actual = 0
        self.lista_mostrada = "ligar"
        otros_humanos = self.otros_humanos()
        inicio = self.pagina_actual * 5
        fin = inicio + 5
        humanos_pagina = otros_humanos[inicio:fin]
        lista_humanos = ft.Column(controls=[
            ft.ElevatedButton(
                text=humano.mapear_nombre(), 
                width=self.porcentuar_medidas(20,0)[0], 
                bgcolor=COLORS["bgc_btn_select_flirt"], 
                color=COLORS['fc_btn'], 
                on_click=lambda _: self.humano_seleccionado.interactuar(humano, "amor")
            ) for humano in humanos_pagina
        ], spacing=15)
        botones_navegacion = self.crear_botones_navegacion(otros_humanos, "hablar")
        contenido = ft.Column(controls=[
            ft.Text(f"{translations["choose_flirt"]}", size=16, weight="bold", color=COLORS['text_color']), 
            lista_humanos, 
            botones_navegacion
        ])
        self.panel_derecho.content = contenido
        self.page.update()
    
    def mostrar_lista_insultar(self, e=None):
        if self.lista_mostrada != "insultar":
            self.pagina_actual = 0
        self.lista_mostrada = "insultar"
        otros_humanos = self.otros_humanos()
        inicio = self.pagina_actual * 5
        fin = inicio + 5
        humanos_pagina = otros_humanos[inicio:fin]
        lista_humanos = ft.Column(controls=[
            ft.ElevatedButton(
                text=humano.mapear_nombre(), 
                width=self.porcentuar_medidas(20,0)[0], 
                bgcolor=COLORS["bgc_btn_select_insult"], 
                color=COLORS['fc_btn'], 
                on_click=lambda _: self.humano_seleccionado.interactuar(humano, "odio")
            ) for humano in humanos_pagina
        ], spacing=15)
        botones_navegacion = self.crear_botones_navegacion(otros_humanos, "hablar")
        contenido = ft.Column(controls=[
            ft.Text(f"{translations["choose_hate"]}", size=16, weight="bold", color=COLORS['text_color']), 
            lista_humanos, 
            botones_navegacion
        ])
        self.panel_derecho.content = contenido
        self.page.update()

    def crear_humano(self, e):
        if not self.timer:
            self.timer = True
            threading.Thread(target=self.start_timer, args=(1,)).start()
            nuevo_humano = Crear_Humano().humano_creado()
            self.dia.humanos_vivos.append(nuevo_humano)
            self.actualizar_lista_humanos()
            print(f"{translations["create_human"]} {nuevo_humano.mapear_nombre()}")
            self.actualizar_lista(self.lista_mostrada)
            self.panel_izquierdo.content.controls[0].controls[8].value = f"{translations["alive_humans_label"]} {len(self.dia.humanos_vivos)}"
            self.page.update()


    def actualizar_lista_humanos(self):
        self.contenedor_lista_humanos.controls.clear()
        for humano in self.dia.humanos_vivos:
            nombre_text = ClickText(text=humano.mapear_nombre(), width= self.porcentuar_medidas(45,0)[0],color=COLORS["text_color"])
            nombre_text.on_click = lambda _, h=humano: self.ver_info(h)
            self.contenedor_lista_humanos.controls.append(
                ft.Row(controls=[
                    nombre_text,
                    ft.IconButton(
                        icon=ft.icons.INFO_OUTLINED, 
                        on_click=lambda _, h=humano: self.ver_info(h), 
                        bgcolor=COLORS['bgc_btn_opciones'], 
                        icon_color=COLORS['icon_options']
                    )
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
            )                
        self.page.update()

    def ver_info(self, humano):
        self.humano_seleccionado = next((h for h in self.dia.humanos_vivos if int(h) == int(humano)), None)
        info = self.humano_seleccionado.info()
        # Crear los botones como antes
        botones = [
            ft.ElevatedButton(text=translations["options_interact"], icon=ft.icons.CHAT, bgcolor=COLORS["bgc_interactuar"], color=COLORS['text_color'], icon_color=COLORS['icon_interact'], on_click=lambda _: self.mostrar_lista_interaccion()),
            ft.ElevatedButton(text=translations["options_see_tink"], icon= ft.icons.REMOVE_RED_EYE, bgcolor=COLORS['bgc_ver_pensamiento'], color=COLORS['text_color'], icon_color=COLORS['icon_see_think'], on_click=lambda _: self.humano_seleccionado.ver_pensamiento()),
            ft.ElevatedButton(text=translations["options_say"], icon=ft.icons.SPATIAL_AUDIO_OFF_ROUNDED, bgcolor=COLORS['bgc_decir'], color=COLORS['text_color'], icon_color=COLORS['icon_say'], on_click=lambda _: self.decir(humano)),
            ft.ElevatedButton(text=translations["options_sick"], icon=ft.icons.CORONAVIRUS, bgcolor=COLORS['bgc_enfermar'], color=COLORS['text_color'], icon_color=COLORS['icon_get_sick'], on_click=lambda _: self.mostrar_lista_enfermedades()),
            ft.ElevatedButton(text=translations["options_cure"], icon=ft.icons.MEDICAL_SERVICES, bgcolor=COLORS['bgc_curar'], color=COLORS['text_color'], icon_color=COLORS['icon_get_sick'], on_click=lambda _: self.mostrar_lista_enfermedades_humano(humano)),
        ]
        # Crear el contenido del panel
        contenido = [ft.Text(info, color=COLORS['text_color'], size=16)] + botones
        # Añadir el tooltip si la probabilidad de morir es mayor al 30%
        if (humano.dias_de_vida - humano.aviso) <= 0:
            tooltip = ft.Tooltip(
                message="Alta probabilidad de morir pronto",
                content=ft.Icon(ft.icons.WARNING, color="red", size=30),
                wait_duration=0,
            )
            contenido.append(tooltip)
        if Shinigami_eyes.has_it():
            contenido.append(ft.Text(translations["days_remain"].replace("[days]", str(humano.dias_de_vida)), weight="bold", size=16, color="#FF6622"))
        self.panel_derecho.content = ft.Column(contenido)
        self.page.update()

    def matar_humano(self, humano):
        humano.morir()
        self.dia.humanos_vivos.remove(humano)
        self.actualizar_lista_humanos()
        self.panel_izquierdo.content.controls[0].controls[8].value = f"{translations["alive_humans_label"]} {len(self.dia.humanos_vivos)}"
        self.actualizar_lista("kills")
        self.page.update()

    def eliminar_raza_humana(self, e):
        if self.dia.eliminar_raza():
            self.actualizar_lista_humanos()
            self.panel_izquierdo.content.controls[0].controls[8].value = f"{translations["alive_humans_label"]} {len(self.dia.humanos_vivos)}"
            print(translations["delete_all_humans"])
        else:
            print(translations["already_kill"])
        self.page.update()

    def siguiente_dia(self, e): 
        
        if not self.timer:
            self.timer = True
            threading.Thread(target=self.start_timer, args=(1,)).start()
            self.stdout_redirector.limpiar_consola()  
            self.dia.avanzar_dia()
            self.panel_izquierdo.content.controls[0].controls[6].value = f"{translations["seasons_content"]} {self.dia.estacion_actual}"
            #self.panel_izquierdo.content.controls[2].value = f"Clima actual: {self.dia.clima_actual}"
            self.panel_izquierdo.content.controls[0].controls[8].value = f"{translations["alive_humans_label"]} {len(self.dia.humanos_vivos)}"
            self.actualizar_lista_humanos()
            self.panel_derecho.content.clean()   
            self.page.update()



    def seleccionar_enfermedad(self, enfermedad):
        self.humano_seleccionado.enfermar(enfermedad)
        self.panel_derecho.content = ft.Text("Humano enfermado", color=COLORS["text_color"], size=18, weight="bold")
        self.page.update()

    def seleccionar_evento(self, evento):
        self.dia.ocasionar_evento(evento)
        self.panel_derecho.content = ft.Text(f"{evento['nombre']} {translations["event_occurred_msg"]}", color=COLORS['text_color'], size=16)
        self.actualizar_lista_humanos()
        self.panel_izquierdo.content.controls[0].controls[8].value = f"{translations["alive_humans_label"]} {len(self.dia.humanos_vivos)}"
        self.page.update()
    
    def seleccionar_humano_interaccion(self, humano1, humano2):
        humano1.interactuar(otra_persona=humano2)
        self.panel_derecho.content = None
        self.page.update()

    def seleccionar_curar(self, enfermedad):

        self.humano_seleccionado.curar(enfermedad)
        self.panel_derecho.content = ft.Text("Humano Curado", color=COLORS["text_color"], size=18, weight="bold")
        self.page.update()

    def config(self, e):
        def close_dlg(e=None):
            dlg.open = False
            self.page.update()

        def save_colors(e):
            # Actualizar los colores en las preferencias
            color_fields = [main_color, left_panel_color, central_panel_color, right_panel_color, btn_crear_humano_color, btn_eliminar_humano_color, btn_eliminar_vida_color, btn_nuevo_dia_color, btn_lista_eventos_color, btn_tutorial_color, btn_configuracion_color, label_color, indicator_color, divider_color, btn_opciones_color, log_color, border_log_color, interactuar_color, ver_pensamiento_color, decir_color, enfermar_color, curar_color, save_color, delete_color, btn_talk_someone_color, btn_flirt_color, btn_insult_color, btn_work_color, btn_work_cure_color, btn_work_arrest_color, btn_work_kill_color, btn_select_talk_color, btn_select_flirt_color, btn_select_insult_color, btn_select_sick_color, btn_select_sick_cure_color, btn_select_event_color, btn_select_kill_color]
            
            color_keys = ['bgc_main', 'bgc_left_panel', 'bgc_central_panel', 'bgc_rigth_panel', 'bgc_btn_crear_humano', 'bgc_btn_eliminar_humano', 'bgc_btn_eliminar_vida', 'bgc_btn_nuevo_dia', 'bgc_btn_lista_eventos', 'bgc_btn_tutorial', 'bgc_btn_configuracion', 'label_color', 'indicator_color', 'divider_color', 'bgc_btn_opciones', 'bgc_log', 'border_log', 'bgc_interactuar', 'bgc_ver_pensamiento', 'bgc_decir', 'bgc_enfermar', 'bgc_curar', 'bgc_save', 'bgc_delete', 'bgc_btn_talk_someone', 'bgc_btn_flirt', 'bgc_btn_insult', 'bgc_btn_work', 'bgc_btn_work_cure', 'bgc_btn_work_arrest', 'bgc_btn_work_kill', 'bgc_btn_select_talk', 'bgc_btn_select_flirt', 'bgc_btn_select_insult', 'bgc_btn_select_sick', 'bgc_btn_select_sick_cure', 'bgc_btn_select_event', 'bgc_btn_select_kill']
            
            for field, key in zip(color_fields, color_keys):
                current_preferences["colors"][key] = field.value

            # Guardar las preferencias actualizadas
            edit_preferences(current_preferences)

            # Actualizar COLORS con los nuevos valores
            global COLORS
            COLORS = current_preferences["colors"]

            # Actualizar los colores en la interfaz
            self.page.bgcolor = COLORS['bgc_main']
            self.panel_izquierdo.bgcolor = COLORS['bgc_left_panel']
            self.panel_central.bgcolor = COLORS['bgc_central_panel']
            self.panel_derecho.bgcolor = COLORS['bgc_rigth_panel']

            # Cerrar el diálogo
            close_dlg(e)
            
            # Actualizar la página
            self.page.update()

        def change_language(lang):
            close_dlg()
            self.language = lang
            current_preferences["language"] = lang
            edit_preferences(current_preferences)
            self.build()

        def exit_app(e):
            self.page.window_close()

        def toggle_music(e):
            button = e.control
            if button.icon == off:
                button.icon = on
                self.dia.main_theme.play(-1)
                current_preferences["music"] = "on"
            else:
                button.icon = off
                self.dia.main_theme.stop()
                current_preferences["music"] = "off"
            edit_preferences(current_preferences)
            self.page.update()

        def toggle_sfx(e):
            button = e.control
            if button.icon == on:
                button.icon = off
                current_preferences["sfx"] = "off"
            else:
                button.icon = on
                current_preferences["sfx"] = "on"
            edit_preferences(current_preferences)
            self.page.update()

        def toggle_fullscreen(e):
            button = e.control
            self.page.window_full_screen = not self.page.window_full_screen
            if button.icon == on:
                button.icon = off
                current_preferences["full_screen"] = "off"
            else: 
                button.icon = on
                current_preferences["full_screen"] = "on"
            edit_preferences(current_preferences)
            self.page.update()

        # Pestaña de Personalización
        main_color = ColorTextField(label="Color fondo principal", value=COLORS['bgc_main'])
        left_panel_color = ColorTextField(label="Color panel izquierdo", value=COLORS['bgc_left_panel'])
        central_panel_color = ColorTextField(label="Color panel central", value=COLORS['bgc_central_panel'])
        right_panel_color = ColorTextField(label="Color panel derecho", value=COLORS['bgc_rigth_panel'])
        btn_crear_humano_color = ColorTextField(label="Color botón crear humano", value=COLORS['bgc_btn_crear_humano'])
        btn_eliminar_humano_color = ColorTextField(label="Color botón eliminar humano", value=COLORS['bgc_btn_eliminar_humano'])
        btn_eliminar_vida_color = ColorTextField(label="Color botón eliminar vida", value=COLORS['bgc_btn_eliminar_vida'])
        btn_nuevo_dia_color = ColorTextField(label="Color botón nuevo día", value=COLORS['bgc_btn_nuevo_dia'])
        btn_lista_eventos_color = ColorTextField(label="Color botón lista eventos", value=COLORS['bgc_btn_lista_eventos'])
        btn_tutorial_color = ColorTextField(label="Color botón tutorial", value=COLORS['bgc_btn_tutorial'])
        btn_configuracion_color = ColorTextField(label="Color botón configuración", value=COLORS['bgc_btn_configuracion'])
        label_color = ColorTextField(label="Color de etiquetas", value=COLORS['label_color'])
        indicator_color = ColorTextField(label="Color de indicador", value=COLORS['indicator_color'])
        divider_color = ColorTextField(label="Color de divisor", value=COLORS['divider_color'])
        btn_opciones_color = ColorTextField(label="Color botón opciones", value=COLORS['bgc_btn_opciones'])
        log_color = ColorTextField(label="Color de fondo del log", value=COLORS['bgc_log'])
        border_log_color = ColorTextField(label="Color del borde del log", value=COLORS['border_log'])
        interactuar_color = ColorTextField(label="Color botón interactuar", value=COLORS['bgc_interactuar'])
        ver_pensamiento_color = ColorTextField(label="Color botón ver pensamiento", value=COLORS['bgc_ver_pensamiento'])
        decir_color = ColorTextField(label="Color botón decir", value=COLORS['bgc_decir'])
        enfermar_color = ColorTextField(label="Color botón enfermar", value=COLORS['bgc_enfermar'])
        curar_color = ColorTextField(label="Color botón curar", value=COLORS['bgc_curar'])
        save_color = ColorTextField(label="Color botón guardar", value=COLORS['bgc_save'])
        delete_color = ColorTextField(label="Color botón eliminar", value=COLORS['bgc_delete'])
        btn_talk_someone_color = ColorTextField(label="Color botón hablar con alguien", value=COLORS['bgc_btn_talk_someone'])
        btn_flirt_color = ColorTextField(label="Color botón coquetear", value=COLORS['bgc_btn_flirt'])
        btn_insult_color = ColorTextField(label="Color botón insultar", value=COLORS['bgc_btn_insult'])
        btn_work_color = ColorTextField(label="Color botón trabajar", value=COLORS['bgc_btn_work'])
        btn_work_cure_color = ColorTextField(label="Color botón trabajo curar", value=COLORS['bgc_btn_work_cure'])
        btn_work_arrest_color = ColorTextField(label="Color botón trabajo arrestar", value=COLORS['bgc_btn_work_arrest'])
        btn_work_kill_color = ColorTextField(label="Color botón trabajo matar", value=COLORS['bgc_btn_work_kill'])
        btn_select_talk_color = ColorTextField(label="Color selección hablar", value=COLORS['bgc_btn_select_talk'])
        btn_select_flirt_color = ColorTextField(label="Color selección coquetear", value=COLORS['bgc_btn_select_flirt'])
        btn_select_insult_color = ColorTextField(label="Color selección insultar", value=COLORS['bgc_btn_select_insult'])
        btn_select_sick_color = ColorTextField(label="Color selección enfermar", value=COLORS['bgc_btn_select_sick'])
        btn_select_sick_cure_color = ColorTextField(label="Color selección curar enfermedad", value=COLORS['bgc_btn_select_sick_cure'])
        btn_select_event_color = ColorTextField(label="Color selección evento", value=COLORS['bgc_btn_select_event'])
        btn_select_kill_color = ColorTextField(label="Color selección matar", value=COLORS['bgc_btn_select_kill'])
        space = ft.Text("")
        customize_tab = ft.Column([space,
            main_color, left_panel_color, central_panel_color, right_panel_color,
            btn_crear_humano_color, btn_eliminar_humano_color, btn_eliminar_vida_color,
            btn_nuevo_dia_color, btn_lista_eventos_color, btn_tutorial_color,
            btn_configuracion_color, label_color, indicator_color, divider_color,
            btn_opciones_color, log_color, border_log_color, interactuar_color,
            ver_pensamiento_color, decir_color, enfermar_color, curar_color,
            save_color, delete_color, btn_talk_someone_color, btn_flirt_color,
            btn_insult_color, btn_work_color, btn_work_cure_color, btn_work_arrest_color,
            btn_work_kill_color, btn_select_talk_color, btn_select_flirt_color,
            btn_select_insult_color, btn_select_sick_color, btn_select_sick_cure_color,
            btn_select_event_color, btn_select_kill_color,
            ft.ElevatedButton(text="Guardar", on_click=save_colors)
        ], scroll=ft.ScrollMode.AUTO)

        on = ft.icons.CHECK_BOX
        off = ft.icons.CHECK_BOX_OUTLINE_BLANK
        # Pestaña de Opciones
        music_button = ft.Row([
            ft.Icon(ft.icons.MUSIC_NOTE),
            ft.Text("Música"),
            ft.IconButton(
                icon=on if current_preferences["music"] == "on" else off,
                on_click=lambda e: toggle_music(e),
            )
        ], alignment=ft.MainAxisAlignment.START)

        sfx_button = ft.Row([
            ft.Icon(ft.icons.VOLUME_UP),
            ft.Text("Efectos de sonido"),
            ft.IconButton(
                icon=on if current_preferences["sfx"] == "on" else off,
                on_click=lambda e: toggle_sfx(e),
            )
        ], alignment=ft.MainAxisAlignment.START)

        fullscreen_button = ft.Row([
            ft.Icon(ft.icons.FULLSCREEN),
            ft.Text("Pantalla completa"),
            ft.IconButton(
                icon=on if current_preferences["full_screen"] == "on" else off,
                on_click=toggle_fullscreen,
            )
        ], alignment=ft.MainAxisAlignment.START)

        exit_button = ft.ElevatedButton("Salir de la aplicación", on_click=exit_app)

        options_tab = ft.Column([music_button, sfx_button, fullscreen_button], 
                                alignment=ft.MainAxisAlignment.START, spacing=20)

        # Pestaña de Idioma
        english_button = ft.ElevatedButton(text="English", on_click=lambda e: change_language("en"))
        spanish_button = ft.ElevatedButton(text="Español", on_click=lambda e: change_language("es"))
        japanese_button = ft.ElevatedButton(text="日本語", on_click=lambda e: change_language("ja"))

        language_tab = ft.Row([english_button, spanish_button, japanese_button], 
                            alignment=ft.MainAxisAlignment.CENTER)

        # Crear las pestañas
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(text="Opciones", content=options_tab),
                ft.Tab(text="Personalizar", content=customize_tab),
                ft.Tab(text="Idioma", content=language_tab),
            ],
            expand=1,
        )

        dlg = ft.AlertDialog(
            title=ft.Text("Configuración"),
            content=ft.Container(
                content=tabs,
                width=self.page.window.width / 2,  
                height=500,  
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=close_dlg),
                exit_button
            ],
            actions_alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            
        )

        self.page.overlay.append(dlg)
        dlg.open = True
        self.page.update()
    
    def build(self):
        self.page.clean()
        language = generar_datos.get_lang()
        translations = generar_datos.get_text(language)
        botones = [
            ft.Text(""),
            ft.ElevatedButton(
                text=translations["create_human_btn"],
                width=self.porcentuar_medidas(20,0)[0],
                
                icon=ft.icons.PERSON_ADD,
                on_click=self.crear_humano,
                bgcolor=COLORS['bgc_btn_crear_humano'],
                color=COLORS['fc_btn']
            ),
            ft.ElevatedButton(
                text=translations["delete_human_btn"],
                width=self.porcentuar_medidas(20,0)[0],
                icon=ft.icons.DELETE,
                on_click=self.mostrar_lista_eliminables,
                bgcolor=COLORS['bgc_btn_eliminar_humano'],
                color=COLORS['fc_btn']
            ),
            ft.ElevatedButton(
                text=translations["delete_race_btn"],
                width=self.porcentuar_medidas(20,0)[0],
                icon=ft.icons.DELETE_FOREVER,
                on_click=self.eliminar_raza_humana,
                bgcolor=COLORS['bgc_btn_eliminar_vida'],
                color=COLORS['fc_btn']
            ),
            ft.ElevatedButton(
                text=translations["advance_day_btn"],
                width=self.porcentuar_medidas(20,0)[0],
                bgcolor=COLORS['bgc_btn_nuevo_dia'],
                color=COLORS['fc_btn'],
                icon=ft.icons.TRANSFER_WITHIN_A_STATION,
                on_click=self.siguiente_dia
            ),
            ft.ElevatedButton(
                text=translations["event_btn"],
                width=self.porcentuar_medidas(20,0)[0],
                bgcolor=COLORS['bgc_btn_lista_eventos'],
                color=COLORS['fc_btn'],
                icon=ft.icons.FLASH_ON,
                on_click=self.mostrar_lista_eventos,
                icon_color=COLORS['icon_events']
            ),
            ft.Text(
                translations["current_season_label"].format(self.dia.estacion_actual),
                size=20,
                weight="bold",
                color=COLORS['text_color']
            ),
            ft.Text(
                translations["current_weather_label"].format(self.dia.clima_actual),
                size=20,
                weight="bold",
                color=COLORS['text_color']
            ),
            ft.Text(
                translations["alive_humans_label"].format(len(self.dia.humanos_vivos)),
                size=20,
                weight="bold",
                color=COLORS['text_color']
            ),
            ft.ElevatedButton(
            text=translations["tutorial_btn"],
            width=self.porcentuar_medidas(20,0)[0],
            icon=ft.icons.HELP_OUTLINE,
            on_click=self.start_tutorial,
            bgcolor=COLORS['bgc_btn_tutorial'],
            color=COLORS['fc_btn']
            ),
            ft.ElevatedButton(
                text=translations["config_btn"],
                width=self.porcentuar_medidas(20,0)[0],
                icon=ft.icons.SETTINGS_APPLICATIONS,
                on_click=self.config,
                bgcolor=COLORS['bgc_btn_configuracion'],
                color=COLORS['fc_btn']
            ),
            ft.ElevatedButton(text=translations["saved"], 
                              icon=ft.icons.SAVE, 
                              width=self.porcentuar_medidas(20,0)[0],
                              bgcolor=COLORS['bgc_save'], 
                              color=COLORS['text_color'], 
                              icon_color=COLORS['icon_get_sick'], 
                              on_click=lambda _: guardar_partida(self.dia.humanos_vivos))
        ]
        self.panel_izquierdo = ft.Container(
            content=ft.Column(
                controls=[ft.Column(controls=botones, spacing=20)],
                spacing=20
            ),
            width=(self.page.window.width / 4) -(self.porcentuar_medidas(2,0)[0]),
            height=self.page.window.height,
            bgcolor=COLORS['bgc_left_panel']
        )
        
        # Contenedor lista humanos
        self.contenedor_lista_humanos = ft.Column(
            controls=[],
            scroll=ft.ScrollMode.HIDDEN,
            height=(self.page.window.height / 2) - (self.porcentuar_medidas(2,0)[0]),  # Ajustado para dejar espacio para las pestañas
            width=self.page.window.width / 2,
            alignment=ft.MainAxisAlignment.START,
        )
        self.actualizar_lista_humanos()

        # Contenedor salida de texto
        self.texto_salida = ft.Text(
            value="",
            size=16,
            weight="bold",
            color=COLORS['text_color'],
            selectable=True
        )
        self.scroll_column = ft.Column(
            [self.texto_salida],
            scroll=ft.ScrollMode.ALWAYS,
            expand=True
        )
        self.salida_texto = ft.Container(
            content=self.scroll_column,
            width=self.page.window.width / 2,
            height=(self.page.window.height / 2) - (self.porcentuar_medidas(2,0)[0]),  # Ajustado para que coincida con la altura de los tabs
            bgcolor=COLORS['bgc_log'],
            border=ft.border.all(4, COLORS['border_log']),
            border_radius=ft.border_radius.all(5),
        )

        # Tabs
        tabs = ft.Tabs(
            selected_index=0,
            tabs=[
                ft.Tab(text=translations["human_tab_label"], content=self.contenedor_lista_humanos),
                ft.Tab(text=translations["world_tab_label"], content=ft.Text("")),
            ],
            height=(self.page.window.height / 2) - 25,
            animation_duration=1,
            divider_color=COLORS["divider_color"],
            divider_height=2.5,
            indicator_color=COLORS["indicator_color"],
            label_color=COLORS["label_color"],
            tab_alignment=ft.TabAlignment.CENTER
        )

        # Panel central
        self.panel_central = ft.Container(
            margin=ft.margin.only(bottom=40),
            content=ft.Column(
                controls=[tabs, self.salida_texto],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=15
            ),
            width=self.page.window.width / 2,
            height=self.page.window.height,
            bgcolor=COLORS['bgc_central_panel'])
        
        # Panel derecho        
        self.panel_derecho = ft.Container(
            content=ft.Text(translations["select_action_label"], 
                            color=COLORS['text_color'], size=16), 
                            width=self.page.window.width / 4 - (self.porcentuar_medidas(2,0)[0]), 
                            height=self.page.window.height, 
                            bgcolor=COLORS['bgc_rigth_panel'])
        self.tutorial = Tutorial(self, self.page)
        self.stdout_redirector = StdoutRedirector(self.texto_salida, self.scroll_column)
        self.page.add(ft.Row(controls=[self.panel_izquierdo, self.panel_central, self.panel_derecho],alignment=ft.MainAxisAlignment.START,vertical_alignment=ft.CrossAxisAlignment.START,))


    def main(self, page: ft.Page):
        self.page = page
        self.page.on_keyboard_event = self.shortcuts 
        self.page.title = translations["app_title"]
        self.page.vertical_alignment = ft.MainAxisAlignment.START
        self.page.bgcolor = COLORS['bgc_main']
        self.page.window.height = screen_height
        self.page.window.width = screen_width
        self.page.window.full_screen = True if current_preferences["full_screen"] == "on" else False
        self.page.on_resized = self.update_size
        # panel_central
        self.build()
 



ft.app(target=App().main)