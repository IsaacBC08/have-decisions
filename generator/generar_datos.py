from settings.user import load_preferences
import yaml
from random import choice

def get_lang():
    return load_preferences()["language"]


def get_text(lang):
    translations = []
    RUTA = f"languages/{lang}.yaml"
    with open(RUTA, "r", encoding="utf-8") as f:
        translations = yaml.safe_load(f)
        return translations

language = get_lang()
translations = get_text(language)

# Nombres
nombres = translations["names"]

apellidos = translations["last_names"]
# Enfermedades:
enfermedades = [translations["diseases_list"][0], translations["diseases_list"][1], translations["diseases_list"][2], translations["diseases_list"][3], translations["diseases_list"][4], translations["diseases_list"][5], translations["diseases_list"][6], translations["diseases_list"][7], translations["diseases_list"][8], translations["diseases_list"][9], translations["diseases_list"][10], translations["diseases_list"][11], translations["diseases_list"][12], translations["diseases_list"][13], translations["diseases_list"][14], translations["diseases_list"][15], translations["diseases_list"][16], translations["diseases_list"][17], translations["diseases_list"][18], translations["diseases_list"][19], translations["diseases_list"][20], translations["diseases_list"][21], translations["diseases_list"][22], translations["diseases_list"][23], translations["diseases_list"][24]]

# Fortalezas (atributos positivos) con IDs
fortalezas = {1: translations["strengths"][0], 2: translations["strengths"][1], 3: translations["strengths"][2], 4: translations["strengths"][3], 5: translations["strengths"][4], 6: translations["strengths"][5], 7: translations["strengths"][6], 8: translations["strengths"][7], 9: translations["strengths"][8], 10: translations["strengths"][9], 11: translations["strengths"][10], 12: translations["strengths"][11]}
# Debilidades (atributos negativos) con IDs
debilidades = {13: translations["weaknesses"][0], 14: translations["weaknesses"][1], 15: translations["weaknesses"][2], 16: translations["weaknesses"][3], 17: translations["weaknesses"][4], 18: translations["weaknesses"][5], 19: translations["weaknesses"][6], 20: translations["weaknesses"][7], 21: translations["weaknesses"][8], 22: translations["weaknesses"][9], 23: translations["weaknesses"][10], 24: translations["weaknesses"][11]}

emociones = {1: 1, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0, 7: 0}
emociones_map = {1: translations["emotions"][0], 2: translations["emotions"][1], 3: translations["emotions"][2], 4: translations["emotions"][3], 5: translations["emotions"][4], 6: translations["emotions"][5], 7: translations["emotions"][6],}

#posibilidad de morir
posibilidad_morir_base = 0.02

#HNI (Human Number Identifier)
hni = 0

hni_temp: dict[int, str] = {}

# Mapeo de atributos a profesiones
atributos_a_profesiones = {
    "amable": "Doctor",
    "optimista": "Músico",
    "inteligente": "Científico",
    "valiente": "Bombero",
    "paciente": "Enfermero",
    "honesto": "Abogado",
    "organizado": "Administrador",
    "tolerante": "Profesor",
    "compasivo": "Trabajador Social",
    "persistente": "Ingeniero",
    "egoísta": "Vendedor",
    "cobarde": "Guardia de Seguridad",
    "deshonesto": "Politico",
    "inseguro": "Asistente",
    "pesimista": "Periodista",
    "impaciente": "Operador",
    "grosero": "Conserje",
    "tonto": "Criminal",
    "repugnancia": "Gerente",
    "desordenado": "Artista",
    "insensible": "Investigador",
    "desistido": "Obrero"
    }

# Países
paises = [translations["countries"][0], translations["countries"][1], translations["countries"][2], translations["countries"][3], translations["countries"][4], translations["countries"][5], translations["countries"][6], translations["countries"][7], translations["countries"][8], translations["countries"][9], translations["countries"][10], translations["countries"][11], translations["countries"][12], translations["countries"][13], translations["countries"][14], translations["countries"][15]]

# Estados
estados = {1: translations["states"][0], 2: translations["states"][1]}

# Creencias
creencias = [translations["religions"][0],translations["religions"][1],translations["religions"][2],translations["religions"][3],translations["religions"][4],translations["religions"][5],translations["religions"][6],translations["religions"][7],translations["religions"][8],translations["religions"][9]]

# Hola
dialogos = {
            "Neutralidad": [["Me aburro...", "Neutralidad"], ["¡Eres tonto!", "Enojo"], ["Suicídate", "Tristeza"], ["Ten un día increíble", "Felicidad"], ["Me gustaría hacerte daño...", "Miedo"], ["Soy tu padre", "Miedo"]],
            "Felicidad": [["¿Por qué estás tan sonriente? ¿Acaso eres tonto?", "Enojo"], ["Te odio", "Tristeza"], ["Eres una buena persona", "Felicidad"], ["Espero mueras", "Miedo"], ["Te llaman sequía de neuronas", "Tristeza"], ["Prefiero vivir sin ti", "Tristeza"], ["Si te callas sería lo mismo que si no te callases, porque eres igual de importante que todas las vacas", "Enojo"]],
            "Tristeza": [["Eres fe@", "Enojo"], ["¡Ten un día increíble!", "Enojo"], ["Peinado tan tonto el que te traes...", "Tristeza"], ["Estoy esperando el día en que pueda pegarte", "Miedo"], ["Contrataré a Achío para que te dé unas Ostias", "Miedo"], ["No vivas la vida si no sabes vivir", "Tristeza"], ["La mejor experiencia que puede tener el mundo es vivir sin ti", "Tristeza"]],
            "Enojo": [["Te quiero pegar", "Enojo"], ["Das asco", "Tristeza"], ["Me quiero comer tus órganos...", "Miedo"], ["Te ves bien", "Felicidad"], ["Te cuento un chiste: Había una vez un tú", "Tristeza"]],
            "Miedo": [["Me gustaría irme de la conversación...", "Enojo"], ["¿Puedes no volver a dirigirme la palabra?", "Tristeza"], ["Cambia esas actitudes... ¿Sí?", "Enojo"], ["Te mataré", "Miedo"], ["Me mataré", "Miedo"], ["Los cerdos como tú, saben respirar", "Tristeza"], ["Me caes horriblemente mal", "Enojo"]]
            }

# Mapeo de opuestos:
atributos_contrarios = {
    1: 13, 13: 1, 7:13,   # generoso <-> egoísta: 
    2: 14, 14: 2,   # valiente <-> cobarde: 
    3: 15, 15: 3,   # honesto <-> deshonesto: 
    4: 16, 16: 4,   # confiado <-> inseguro: 
    5: 17, 17: 5,   # optimista <-> pesimista: 
    6: 18, 18: 6,   # paciente <-> impaciente: 
    7: 19, 19: 7,   # amable <-> descortés: 
    8: 20, 20: 8,   # inteligente <-> tonto: 
    9: 21, 21: 9,   # tolerante <-> repugnancia: 
    10: 22, 22: 10, # organizado <-> desordenado: 
    11: 23, 23: 11, # compasivo <-> insensible: 
    12: 24, 24: 12  # persistente <-> desistido: 
}

eventos = [
    {
        "nombre": "Cielo Hermoso",
        "descripcion": "El cielo está despejado y hermoso. Se eliminó pesimismo de todos los humanos!",
		"probabilidad": 0.025, #2.5% de posibilidad de ocurrir cada día
		"afectados": lambda humano: 17 in humano.atributos,
		"efecto": lambda humano: humano.atributos.remove(17) if 17 in humano.atributos else None,
    },
	{
        "nombre": "Lluvia de meteoros",
        "descripcion": "Por la noche se observan miles de hermosos meteoros en el cielo. Todos los humanos están felices",
		"probabilidad": 0.01, #1% de posibilidad de ocurrir cada día
		"afectados": lambda humano: True, #todos
		"efecto": lambda humano: humano.actualizar_sentimiento("Felicidad")
    },
	{
        "nombre": "Luz de la Luna Restauradora",
        "descripcion": "Una noche, un misterioso rayo de luna llena se cierne sobre el mundo, curando a todos los enfermos.",
        "probabilidad": 0.005, # 0.5% de posibilidad de ocurrir cada día
        "afectados": lambda humano: "0" in str(humano.estado),  # solo los humanos enfermos
        "efecto": lambda humano: humano.curar() if humano.estado == 1 else None,
    },
	{
        "nombre": "Eclipse de Niebla Púrpura",
        "descripcion": "Un eclipse mágico cubre el mundo en una niebla púrpura. Todos los humanos se ven afectados por distintas enfermedades.",
        "probabilidad": 0.01, # 1% de posibilidad de ocurrir cada día
        "afectados": lambda humano: True,  # todos los humanos enfermos
        "efecto": lambda humano: humano.enfermar(choice(enfermedades)),
    },
	{
		"nombre": "Apariciones Fantasmales",
		"descripcion": "Espíritus y fantasmas comienzan a aparecer en el mundo, todos los cobardes mueren de miedo...",
		"probabilidad": 0.015, # %1.5 de posibilidad de ocurrir cada día,
		"afectados": lambda humano: "cobarde" in humano.atributos,  # Afecta a una fracción de los humanos
		"efecto": lambda humano: humano.morir()
	}
]


current_preferences = load_preferences()

climas_procedurales = {
    f"{translations["seasons"][0]}": {
        "Despejado": {"Despejado": 0.7, "Nublado": 0.3},
        "Nublado": {"Despejado": 0.4, "Nublado": 0.6}
    },
	f"{translations["seasons"][1]}": {
        "Despejado": {"Despejado": 0.5, "Nublado": 0.3, "Lluvioso": 0.2},
        "Nublado": {"Despejado": 0.3, "Nublado": 0.4, "Lluvioso": 0.3},
        "Lluvioso": {"Nublado": 0.4, "Lluvioso": 0.5, "Despejado": 0.1}
    },
    f"{translations["seasons"][2]}": {
        "Ventoso": {"Ventoso": 0.4, "Lluvioso": 0.3, "Tormenta": 0.2, "Despejado": 0.1},
        "Lluvioso": {"Ventoso": 0.3, "Lluvioso": 0.4, "Tormenta": 0.2, "Despejado": 0.1},
        "Tormenta": {"Ventoso": 0.2, "Lluvioso": 0.3, "Tormenta": 0.4, "Despejado": 0.1},
        "Despejado": {"Ventoso": 0.2, "Lluvioso": 0.2, "Tormenta": 0.2, "Despejado": 0.4}
    },
    f"{translations["seasons"][3]}": {
        "Tormenta": {"Tormenta": 0.4, "Nevado": 0.3, "Granizo": 0.2, "Lluvia": 0.1},
        "Nevado": {"Tormenta": 0.3, "Nevado": 0.4, "Granizo": 0.2, "Lluvia": 0.1},
        "Granizo": {"Tormenta": 0.3, "Nevado": 0.2, "Granizo": 0.4, "Lluvia": 0.1},
        "Lluvia": {"Tormenta": 0.2, "Nevado": 0.2, "Granizo": 0.2, "Lluvia": 0.4}
    }
}

RUTA = "data/humans.json"