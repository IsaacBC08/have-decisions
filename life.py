# crear Objetos
# dialogos traducidos
# Tutorial
# Traducir eventos
# Sistema de misiones(obtiene objetos)
# Sistema de paises en el mundo
# Añadir más eventos
# Pestaña de mundo
# Estilizar configuración
# Traducir configuracipon
# Creditos
# traducir relaciones

# Una app que cumpla el proposito
# Un script
# Una web
# Un Game Engine

""""
Objetivo: poder tener una app, o un menu interacto, o una web
en esta app, yo puedo arrastrar y soltar componentes de flet,
ponerles las características, reemplazar los colores, y todas las 
opciones de un componente, así como diseñar completamente la ventana
"""

#* BUGS DE LA UI
# Errores con el cambio de idioma

#! Estructura de las relaciones
# las relaciones se van desbloqueando en base a el nivel de otra relación
# atributos facilitan/dificultan la mejora de relaciones
# casamiento --> noviazgo --> amistad --> conocid@
# odio --> enemistad --> Desagrado --> conocid@
# amistad >= 3lvl = !odio(deja de ser posible)
# desagrado >= 3lvl = !amor(deja de ser posible)

# noviazgo -> pedir matrimonio
# enemistad -> agredir/asesinar

from actores.humanos import *

messi = Crear_Humano().humano_creado()
print(messi)