import random
from actores.humanos import cargar_humanos
from core.clima import Clima
from generator.generar_datos import *
import pygame
class Dia:
    ESTACIONES = translations["seasons"]
    
    def __init__(self, eventos):
        self.evento_hoy = False
        self.dia_actual = 1
        pygame.mixer.init()
        pygame.mixer.init()
        self.main_theme = pygame.mixer.Sound("sounds/referencia_1.mp3")
        self.main_theme.play(-1) if current_preferences["music"] == "on" else self.main_theme.stop()
        self.clima = Clima()
        self.humanos_vivos = cargar_humanos()  # Lista de humanos vivos
        self.eventos = eventos
        self.total_vivos = 0
        self.estacion_actual = self.determinar_estacion()
        self.clima_actual = self.clima.generar_clima_aleatorio()

    def eliminar_raza(self):
        if len(self.humanos_vivos) != 0:
            for humano in self.humanos_vivos[:]:
                humano.morir()
            return True
        else:
            return False
        

    def determinar_estacion(self):
        indice_estacion = ((self.dia_actual - 1) // 10) % len(self.ESTACIONES)
        return self.ESTACIONES[indice_estacion]
    
    def agregar_humano(self, humano):
        """Agrega un humano a la lista de vivos si no está muerto"""
        if humano.estado != "Muerto":
            self.humanos_vivos.append(humano)

    def ocasionar_evento(self, evento):
        if not self.evento_hoy:
            self.evento_hoy = True
            pygame.mixer.Sound("sounds/event_ocurred.mp3").play() if current_preferences["sfx"] == "on" else None
            print(f"[LENTO]{translations["event_has_occurred"]}")
            print(f"[LENTO]{translations["event"]} {evento['nombre']}\n{translations["description"]} {evento['descripcion']}")
            for humano in self.humanos_vivos:
                if evento["afectados"](humano):
                    evento["efecto"](humano)
        else:
            print(translations["has_event"])

    def avanzar_dia(self):
        # Incrementa la edad de los humanos vivos
        for humano in self.humanos_vivos:
            if humano.estado != 2:
                humano.edad += 1
                humano.interacciono = False
                humano.envejecer()
        # Elimina a los humanos muertos
        self.humanos_vivos = [humano for humano in self.humanos_vivos if humano.estado != 2]
        self.total_vivos = len(self.humanos_vivos)
        print(f"[LENTO]{translations["current_day"]} {self.dia_actual}, {translations["alive_humans"]} {self.total_vivos}")

        nueva_estacion = self.determinar_estacion()
        
        if nueva_estacion != self.estacion_actual:
            self.estacion_actual = nueva_estacion
            self.clima.cambiar_estacion(self.estacion_actual)
        
        self.clima_actual = self.clima.generar_clima_aleatorio()
        self.evento_hoy = False
        # Verificar si algún evento ocurre y aplicarlo
        for evento in self.eventos:
            if random.random() < evento["probabilidad"]:
                self.ocasionar_evento(evento)
                break  # No ocurren 2 eventos en un solo día
        self.dia_actual += 1