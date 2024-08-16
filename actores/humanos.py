from generator.generar_datos import *
from generator import generar_datos
from pydantic import BaseModel
import random
import json
import os
from time import sleep as wait


class Humano(BaseModel):
	nombre: int
	apellido: int
	edad: int
	estado: int
	enfermedades: list
	pais: str
	atributos: list
	religion: str
	sentimiento: int
	emociones: dict
	profesion: str
	guardado: bool
	relaciones: list
	interacciono: bool = False
	genero: int
	dias_de_vida: int
	aviso: int = random.randint(1,3)

	def __init__(self, **data):
		super().__init__(**data)
		self._hni = generar_datos.hni
		generar_datos.hni += 1


	@property
	def hni(self):
		return self._hni
	
	@hni.setter
	def hni(self, value):
		raise AttributeError("No se pueden modificar atributos de solo lectura")
	
	def __int__(self: object) -> int: return self._hni 
	
	def __str__(self: object) -> str: return self.mapear_nombre()
	
	def mapear_emocion(self, emocion) -> str: return emociones_map[emocion]
	
	def mapear_nombre(self, nombre=None) -> str: 
		lang = get_lang()
		translations = get_text(lang)
		return f"{translations["names"][self.nombre]} {translations["last_names"][self.apellido]}"
 	
	def mapear_estado(self, estado) -> str: return estados[estado]

	def mapear_genero(self) -> str: return translations["gender"][self.genero]

	def conversar(self, tipo, level, otro_humano):
		dialogues = translations["dialogues"][f"{tipo}"][f"level_{level}"]
		
		for i, line in enumerate(dialogues):
			wait(0.1)
			if i % 2 == 0:  
				self.decir(line.replace("[name]", self.mapear_nombre()))
			else: 
				otro_humano.decir(line.replace("[name]", otro_humano.mapear_nombre()))
	
	def subir_nivel_relacion(self, relacion):
		nivel = relacion["nivel"]
		if relacion["tipo_relacion"] == "friendship" and nivel <5:
			relacion["nivel"] += 1
			print("amistad nivel ++")
			
	def evaluar_relaciones(self, otro_humano, tipo):
		"""Busca el HNI de un humano en sus relaciones; si no existe relación, crea una"""
		hni = int(otro_humano)
		existe = False
		# Buscar si ya existe la relación
		for relacion in self.relaciones:
			if str(hni) in relacion:
				# Mejorar la relación
				self.subir_nivel_relacion(relacion[str(hni)])
				self.conversar("friendship",relacion[str(hni)]["nivel"], otro_humano)
				print(f"{translations["up_relation"]} {tipo}, {translations["new_level"]} {relacion[str(hni)]['nivel']}")
				existe = True
				break
		
		if not existe:
			# Crear una nueva relación
			nueva_relación = {
				f"{hni}": {
					"nombre": str(otro_humano),
					"tipo_relacion": f"{tipo}",
					"nivel": 1
				}
			}
			self.relaciones.append(nueva_relación)
			self.conversar("friendship",1, otro_humano)
			print(f"[LENTO]Nueva relación de {tipo} creada")

	def info(self) -> str:
		""" Muestra la información del humano """
		atributos_formateados = "\n".join([f"- {atributo}" for atributo in self.mapear_atributos()])
		enfermedades = self.enfermedades if self.enfermedades else  [translations["fine_human"]]
		info = (
			f"{self.mapear_nombre()}, ID: {self.hni}\n"
			f"{translations["gender_label"]} {self.mapear_genero()}\n"
			f"{translations["age"]} {self.edad} {translations["years"]}\n"
			f"{translations["attributes"]}\n{atributos_formateados}\n"
			f"{translations["feeling"]} {self.mapear_emocion(self.sentimiento)}\n"
			f"{translations["country"]} {self.pais}\n"
			f"{translations["condition"]} {self.mapear_estado(self.estado)}\n"
			f"{translations["religion"]} {self.religion}\n"
			f"{translations["diseases"]} {enfermedades[0]}\n"
			f"{translations["profession"]} {self.profesion if self.profesion else translations["not_assigned"]}\n"	
		)
		return info

	def mapear_atributos(self):
		atributos_mapeados = []
		for atributo in self.atributos:
			if atributo in fortalezas:
				atributos_mapeados.append(fortalezas[atributo].capitalize())
			elif atributo in debilidades:
				atributos_mapeados.append(debilidades[atributo].capitalize())
		return atributos_mapeados

	def decir(self, mensaje: str):
		""" Hace que un humano diga el mensaje"""
		print(f"{self.mapear_nombre()}: {mensaje}")
	


	def envejecer(self):
		"""Resta los días de vida del humano, y en dado caso, lo mata"""
		if self.dias_de_vida > 0:
			self.dias_de_vida -=1
		else: 
			self.morir()
	
	
	def asignar_profesion(self):
		""" Asigna una profesión basada en los atributos del humano """
		for atributo in self.atributos:
			if atributo in atributos_a_profesiones:
				self.profesion = atributos_a_profesiones[atributo]
				break  
		print(f"{self.mapear_nombre()} {translations["is_now"]} {self.profesion}.")
	
	def curar(self, enfermedad):
		self.enfermedades.remove(enfermedad)
		self.estado = 2 if not enfermedades else 1
		print(f"{self.mapear_nombre()} {translations["healthy"]} {enfermedad}")

	def enfermar(self, enfermedad):
		self.enfermedades.append(enfermedad)
		self.estado = 1
		print(f"{self.mapear_nombre()} {translations["sick"]} {enfermedad}")

	def ver_pensamiento(self):
		"""" Permite ver el sentimiento actual del humano"""
		print(f"{self.mapear_nombre()} {translations["feel"]} {self.mapear_emocion(self.sentimiento)}...")

	def interactuar(self, otra_persona, tipo):
		"""Interactua con otro humano"""
		if self.interacciono:
			print(translations["already_interacted"])
			return
		self.interacciono = True
		sentimiento_de_otro = otra_persona.sentimiento
		self.evaluar_relaciones(otra_persona, tipo)

		# mensaje, atributo = self.generar_dialogo(sentimiento_de_otro)
		# print(f"{self.mapear_nombre()}: {mensaje}")
		# otra_persona.modificar_emociones(atributo)
		# otra_persona.actualizar_sentimiento()
		# otra_persona.ver_pensamiento()


	def modificar_emociones(self, emocion):
		""" Modifica las emociones del humano en base a la emoción que le genera un dialogo o accion"""
		aumento_base = 1
		if emocion == "Miedo":
			if "valiente" in self.atributos or "confiado" in self.atributos:
				aumento_base *= 0.6
			elif "cobarde" in self.atributos or "inseguro" in self.atributos:
				aumento_base *= 1.6
		elif emocion == "Enojo":
			if "paciente" in self.atributos:
				aumento_base *= 0.6
			elif "impaciente" in self.atributos:
				aumento_base *= 1.6
		elif emocion == "Felicidad":
			if "optimista" in self.atributos:
				aumento_base *= 1.6
			elif "pesimista" in self.atributos:
				aumento_base *= 0.6
		elif emocion == "Tristeza":
			if "compasivo" in self.atributos:
				aumento_base *= 0.6
			elif "insensible" in self.atributos:
				aumento_base *= 1.6
		# Actualizar la estadística correspondiente
		self.emociones[emocion] += aumento_base

	def actualizar_sentimiento(self, especifico=None):
		""" Cambia el sentimiento actual del humano al que mayor estadistica tiene"""
		self.sentimiento = especifico if especifico else max(self.emociones, key=self.emociones.get)

	def generar_dialogo(self, estado_emocional: str) -> tuple:
		"""Genera un diálogo y la emoción que causa en la otra persona"""
		
		mensaje, atributo = random.choice(dialogos[estado_emocional])
		return mensaje, atributo
	
	def morir(self):
		"""Marca al humano como muerto"""
		self.estado = 2
		print(f"{self.mapear_nombre()} {translations["die"]}")
	
	def trabajar(self):
		"""Pone al humano a chambear"""
		print(f"{self.mapear_nombre()} {translations["working"]} {self.profesion}")

class Crear_Humano:
	def __init__(self ,nombre = None):
		self.name, self.last_name = nombre if nombre != None else random.randint(0, len(nombres) - 1), random.randint(0, len(apellidos) - 1) #! Ya estoy.
		self.edad = random.randint(2, 10)
		self.atributos = []
		self.estado = 1
		self.religion = random.choice(creencias)
		self.pais = random.choice(paises)
		self.asignar_atributos()
		self.emociones = emociones
		self.sentimiento = 1
		self.profesion = ""
		self.relaciones = []
		self.genero = random.randint(0,1)
		self.dias_de_vida = random.randint(10,30)
	
	def asignar_atributos(self):
		""" Asiga atributos aleatorios de la lista de todos los atributos"""
		while len(self.atributos) < 2:
			atributo = random.choice(list(fortalezas.keys()))
			contrario = atributos_contrarios[atributo]
			if not contrario in self.atributos:
				self.atributos.append(atributo)
		while len(self.atributos) < 4:
			atributo = random.choice(list(debilidades.keys()))
			contrario = atributos_contrarios[atributo]
			if not contrario in self.atributos:
				self.atributos.append(atributo)

	def humano_creado(self) -> Humano:
		"""Devuelve la instancia creada del humano con los atributos asignados, nombre, edad, fortalezas, debilidades, estado, pais, creencias y enfermedades"""
		atributos_asignados = list({id_: (fortalezas[id_] if id_ in fortalezas else debilidades[id_]) for id_ in self.atributos})
		return Humano(
				nombre=self.name,
				apellido=self.last_name,
				edad=self.edad,  
				estado=self.estado,  
				enfermedades=[],  
				pais=self.pais,  
				atributos=atributos_asignados,  
				religion=self.religion,  
				sentimiento=self.sentimiento,  
				emociones=self.emociones,  
				profesion=self.profesion,  
				guardado=False, 
				relaciones=self.relaciones, 
				genero=self.genero,
				dias_de_vida=self.dias_de_vida)

def guardar_partida(nuevos_humanos: list, ruta=RUTA):
    # Vaciar el archivo de datos existentes
    if os.path.exists(ruta):
        os.remove(ruta)
    
    # Guardar todos los nuevos humanos
    for humano in nuevos_humanos:
        guardar_humano(humano, ruta)
    print(f"{translations["saved"]}")

def guardar_humano(humano: Humano, ruta=RUTA):
    # Cargar datos existentes o crear un nuevo diccionario
    if os.path.exists(ruta):
        with open(ruta, "r", encoding="utf-8") as f:
            datos = json.load(f)
    else:
        datos = {}
    
    # Encontrar el próximo número de humano
    numeros_existentes = [int(k.split('_')[1]) for k in datos.keys() if k.startswith('Humano_')]
    proximo_numero = max(numeros_existentes + [-1]) + 1
    
    # Añadir el nuevo humano
    clave_humano = f"Humano_{proximo_numero}"
    datos[clave_humano] = humano.model_dump()
    
    # Guardar todos los datos
    with open(ruta, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)


def cargar_humanos(ruta=RUTA):

    try:
        with open(ruta, 'r', encoding="utf-8") as archivo:
            datos = json.load(archivo)
            
        humanos = []

        for clave, valor in datos.items():
            try:
                humano = Humano(**valor)
                humanos.append(humano)
            except Exception as e:
                print(f"Error al cargar {clave}: {str(e)}")
        return humanos
        
    except json.decoder.JSONDecodeError:
        print("No hay humanos guardados o el archivo JSON está malformado.")
        with open(RUTA, "w", encoding="utf-8") as file:
            default = {}
            json.dump(default, file, indent=4)
        return []
    except FileNotFoundError:
        print("El archivo no existe.")
        return []
    except Exception as e:
        print(f"Ocurrió un error inesperado: {str(e)}")
        return []




