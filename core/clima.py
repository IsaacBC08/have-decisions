import random
from generator.generar_datos import climas_procedurales, translations




class Clima:
    def __init__(self, clima_actual="Despejado", estacion_actual=translations["seasons"][0]):
        self.clima_actual = clima_actual
        self.estacion_actual = estacion_actual

    def generar_clima_aleatorio(self):
        opciones = climas_procedurales[self.estacion_actual][self.clima_actual]
        self.clima_actual = random.choices(list(opciones.keys()), list(opciones.values()))[0]
        return self.clima_actual

    def cambiar_estacion(self, nueva_estacion):
        self.estacion_actual = nueva_estacion
        # Ajustar el clima inicial para la nueva estación
        climas_estacion = climas_procedurales[nueva_estacion]
        if self.clima_actual not in climas_estacion:
            self.clima_actual = random.choice(list(climas_estacion.keys()))
        else:
            opciones = climas_estacion[self.clima_actual]
            self.clima_actual = random.choices(list(opciones.keys()), list(opciones.values()))[0]
        return self.clima_actual