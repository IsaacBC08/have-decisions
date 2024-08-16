# Sistema economico
# Nivel de riqueza
# Peligroso
# Descripcion
# condicion geografica
# que tiene
# definir atributos_positivos, atributos_negros
import random
from itertools import combinations, product

data = {
	"human_names": ("Abril", "Adela", "Adelina", "Adolfo", "Adriana", "Adrián", "Adán", "Agustín", "Aitana", "Alan", "Alba", "Alberto", "Alejandro", "Alejo", "Alexis", "Alfonso", "Alfredo", "Alicia", "Alma", "Alonso", "Amado", "Amelia", "Anastasia", "Andrés", "Angélica", "Anselmo", "Antonia", "Antonio", "Ariadna", "Arnaldo", "Artemio", "Arturo", "Asunción", "Augusto", "Aurora", "Aída", "Baltasar", "Bartolomé", "Basilio", "Beatriz", "Belén", "Benigno", "Benito", "Benjamín", "Berenice", "Bernarda", "Bernardo", "Berta", "Bianca", "Blanca", "Bob", "Bonifacio", "Borja", "Braulio", "Brenda", "Brigida", "Bruno", "Bryan", "Bárbara", "Camila", "Carina", "Carla", "Carlos", "Carmelo", "Carmen", "Carolina", "Catalina", "Cecilia", "Celia", "Celso", "Ciro", "Clara", "Claudia", "Claudio", "Clemente", "Concepción", "Consuelo", "Cornelio", "Cristina", "Cristóbal", "Cándido", "César", "Dagoberto", "Dalia", "Damián", "Dania", "Daniel", "Dante", "Darío", "David", "Delfina", "Demetrio", "Dereck", "Diana", "Diego", "Dionisio", "Dolores", "Domingo", "Dora", "Dámaso", "Edilberto", "Edmundo", "Eduardo", "Efraín", "Eladio", "Elena", "Elias", "Elisa", "Eliseo", "Elsa", "Elvira", "Elías", "Emiliano", "Emilio", "Enrique", "Enzo", "Erasmo", "Ernesto", "Esperanza", "Esteban", "Esteban", "Estefanía", "Estela", "Ester", "Eugenio", "Eulalia", "Eva", "Ezequiel", "Fabio", "Fabiola", "Fabiola", "Fabricio", "Facundo", "Fausto", "Federico", "Feliciano", "Felipe", "Felix", "Fermín", "Fernanda", "Fernando", "Fidel", "Flavia", "Flor", "Florencia", "Francisco", "Franco", "Gabriel", "Gabriela", "Gaspar", "Genaro", "Genoveva", "Georgina", "Gerardo", "Germán", "Gilberto", "Gina", "Gisela", "Gloria", "Gonzalo", "Graciela", "Gregorio", "Guadalupe", "Guido", "Guillermina", "Guillermo", "Gustavo", "Haydée", "Helena", "Heriberto", "Herminia", "Hilda", "Hipólito", "Homero", "Honorio", "Horacio", "Hortensia", "Hugo", "Humberto", "Héctor", "Ibai", "Ignacia", "Ignacio", "Iker", "Ildefonso", "Indiana", "Ingrid", "Inés", "Irene", "Iris", "Irma", "Isaac", "Isabel", "Isaías", "Isidoro", "Isidro", "Ismael", "Ivanna", "Iván", "Jacinto", "Jacobo", "Jafeth", "Jaime", "Jairo", "Javier", "Jeremías", "Jimena", "Joaquín", "Joel", "Jonás", "Jordi", "Jorge", "Josefina", "Josué", "José", "Juan", "Juana", "Judas", "Julia", "Julieta", "Julio", "Julián", "Justino", "Juvenal", "Karina", "Karina", "Karla", "Kevin", "Lara", "Laura", "Laureano", "Leandro", "Leocadio", "Leonardo", "Leonor", "Leslie", "Leticia", "León", "Lidia", "Lilia", "Liliana", "Lisandro", "Lorena", "Lorenzo", "Lourdes", "Lucas", "Luciano", "Lucrecia", "Lucía", "Ludmila", "Luis", "Macario", "Magdalena", "Malena", "Manuel", "Manuela", "Marcelino", "Marcelo", "Marcos", "Margarita", "Mariano", "Mariela", "Mario", "Marta", "Martín", "María", "Mateo", "Matilde", "Matías", "Mauricio", "Mauro", "Mauro", "Maximiliano", "Melisa", "Micaela", "Miguel", "Miriam", "Mirta", "Moisés", "Mónica", "Nadia", "Nadie", "Nahuel", "Nancy", "Narciso", "Natalia", "Nataly", "Natividad", "Nazario", "Nerea", "Nicanor", "Nicolás", "Nieves", "Noe", "Noelia", "Noemí", "Nora", "Norberto", "Norma", "Néstor", "Octavio", "Olegario", "Olga", "Olga", "Oliver", "Olivia", "Omar", "Oneida", "Oralia", "Orestes", "Orlando", "Oscar", "Oseas", "Osvaldo", "Otilia", "Ovidio", "Pablo", "Paloma", "Paloma", "Paola", "Paolo", "Pascual", "Patricia", "Patricio", "Paula", "Paulina", "Paz", "Pedro", "Petrona", "Pilar", "Porfirio", "Priscila", "Prudencio", "Rafael", "Ramiro", "Ramón", "Raquel", "Raúl", "Rebeca", "Reinaldo", "Renata", "Renzo", "René", "Ricardo", "Rigoberto", "Rita", "Roberto", "Rocío", "Rodrigo", "Rogelio", "Rolando", "Romeo", "Romina", "Román", "Rosaura", "Rubén", "Rufino", "Sabrina", "Salomé", "Salvador", "Samuel", "Santiago", "Sara", "Saúl", "Sebastián", "Selena", "Serafín", "Sergio", "Silvestre", "Silvia", "Simón", "Sofía", "Soledad", "Susana", "Tadeo", "Tamara", "Tania", "Tatiana", "Telma", "Teodoro", "Teresa", "Thiago", "Timoteo", "Tobías", "Tomasa", "Tomás", "Tony", "Trinidad", "Ubaldo", "Ulises", "Ulma", "Uriel", "Valentina", "Valentín", "Valeria", "Valerio", "Vanesa", "Verónica", "Vicenta", "Vicente", "Victoria", "Violeta", "Virgilio", "Virginia", "Viviana", "Viviana", "Víctor", "Wally", "Walter", "Wenceslao", "Wenceslao", "Wendy", "Wilfredo", "Xavier", "Ximena", "Xiomara", "Yago", "Yahir", "Yamilet", "Yanet", "Yaretzi", "Yesenia", "Yessica", "Yolanda", "Yolanda", "Yovanna", "Yulia", "Zacarías", "Zoe", "Zulma", "Álvaro", "Ángel", "Ángela", "Úrsula"),
	"human_surnames": ("Abarca", "Abreu", "Acevedo", "Acosta", "Adame", "Adams", "Aguado", "Aguayo", "Aguilar", "Aguilera", "Aguirre", "Agüero", "Alarcón", "Alarcón", "Albornoz", "Alcalá", "Alcaraz", "Alcocer", "Alcántara", "Alcázar", "Alderete", "Alfaro", "Almagro", "Almaraz", "Almonte", "Alonso", "Altamirano", "Altamirano", "Alvarado", "Amador", "Andrade", "Angulo", "Aparicio", "Aponte", "Aragón", "Aranda", "Araujo", "Araya", "Arce", "Arce", "Archuleta", "Arellano", "Arenas", "Arguello", "Arias", "Arismendi", "Arjona", "Armendáriz", "Armenta", "Arnau", "Arredondo", "Arreola", "Arriaga", "Arriola", "Arroyo", "Arteaga", "Asensio", "Atencio", "Avilés", "Ayala", "Baena", "Balderas", "Ballesteros", "Barajas", "Barba", "Barbosa", "Barquero", "Barrera", "Barreto", "Barrientos", "Barrios", "Barros", "Batista", "Bautista", "Bautista", "Becerra", "Bello", "Beltrán", "Benavides", "Benítes", "Benítez", "Bermúdez", "Betancourt", "Blanco", "Blanco", "Bonilla", "Borrego", "Botello", "Bravo", "Briones", "Briseño", "Brito", "Bueno", "Burgos", "Bustamante", "Bustillo", "Báez", "Caballero", "Cabello", "Cabrera", "Cadena", "Calderón", "Calvo", "Camacho", "Camacho", "Campos", "Cano", "Canto", "Cardozo", "Carmona", "Caro", "Carranza", "Carrasco", "Carrera", "Carrero", "Carrillo", "Carvajal", "Casas", "Castañeda", "Castañón", "Castellanos", "Castillo", "Castro", "Ceballos", "Cedillo", "Cepeda", "Cerda", "Cervantes", "Chacón", "Chávez", "Cienfuegos", "Cisneros", "Collado", "Colón", "Contreras", "Cordero", "Cordero", "Corona", "Corral", "Corrales", "Correa", "Correa", "Cortez", "Cortés", "Crespo", "Cruz", "Cuevas", "Cuevas", "Cárdenas", "Delarosa", "Deleon", "Delgadillo", "Delgado", "Domínguez", "Donoso", "Duarte", "Dueñas", "Duran", "Durán", "Dávila", "Díaz", "Echevarría", "Echeverría", "Elizondo", "Enríquez", "Escalante", "Escamilla", "Escobar", "Escobar", "Escobedo", "Esparza", "Espinal", "Espino", "Espinosa", "Espinoza", "Esquivel", "Estrada", "Estrada", "Estévez", "Fajardo", "Farias", "Farías", "Feliciano", "Fernández", "Ferrer", "Fierro", "Figueres", "Figueroa", "Flores", "Fonseca", "Franco", "Frías", "Fuentes", "Fuentes", "Gaitán", "Galarza", "Galindo", "Galindo", "Gallardo", "Gallegos", "Gallo", "Galván", "Gamboa", "Gaona", "Garay", "García", "Garrido", "Garza", "Gastelum", "Godoy", "Gomez", "González", "Gracia", "Granados", "Guardado", "Guardiola", "Guerra", "Guerrero", "Guerrero", "Guevara", "Guillen", "Gurule", "Gutiérrez", "Gutiérrez", "Guzman", "Guzmán", "Gómez", "Haro", "Henríquez", "Heredia", "Hermosillo", "Hernandez", "Hernando", "Hernández", "Herrada", "Herrera", "Herrera", "Hidalgo", "Hidalgo", "Hinojosa", "Holguín", "Huerta", "Hurtado", "Ibarra", "Ibarra", "Ibáñez", "Iglesias", "Iturbe", "Jacobo", "Jaramillo", "Jasso", "Jimenez", "Jiménez", "Jurado", "Juárez", "Lara", "Lara", "Laureano", "Leal", "Ledesma", "Ledesma", "Leiva", "Lewis", "Leyva", "León", "Limón", "Linares", "Lira", "Llamas", "Loera", "Lomeli", "Longoria", "Lozada", "Lozano", "Lugo", "Luján", "Luna", "Luna", "López", "Macías", "Macías", "Madrigal", "Malave", "Maldonado", "Manrique", "Manzanares", "Marin", "Marrero", "Marroquín", "Martí", "Martínez", "Marín", "Mascareñas", "Mateo", "Matos", "Matías", "Medina", "Meireles", "Mejía", "Meléndez", "Mena", "Mendoza", "Mendoza", "Menéndez", "Meyer", "Miramontes", "Miranda", "Mitchell", "Molina", "Montes", "Montiel", "Montoya", "Mora", "Morales", "Moreno", "Moya", "Muñoz", "Márquez", "Navarrete", "Navarro", "Newton", "Núñez", "Ochoa", "Ojeda", "Olson", "Ordoñez", "Ortega", "Ortiz", "Pacheco", "Padilla", "Palacios", "Palma", "Paredes", "Perales", "Peralta", "Peña", "Pineda", "Pinedo", "Pizarro", "Pérez", "Quezada", "Quijano", "Quintana", "Quiroga", "Quirós", "Ramos", "Ramírez", "Rangel", "Rebolledo", "Reina", "Rentería", "Reyes", "Reynoso", "Rico", "Rivera", "Rodarte", "Rodríguez", "Rojas", "Roldán", "Romero", "Rosales", "Ruiz", "Ríos", "Saavedra", "Salazar", "Salinas", "Salvatierra", "Sandí", "Santos", "Sepúlveda", "Serna", "Serrano", "Silva", "Solano", "Soler", "Soto", "Stewart", "Suárez", "Sánchez", "Tapia", "Torres", "Tovar", "Trejos", "Ugarte", "Uribe", "Valdez", "Valencia", "Valenzuela", "Valle", "Varela", "Vargas", "Vega", "Velasco", "Velásquez", "Vera", "Villanueva", "Villegas", "Vásquez", "Vázquez", "Yanez", "Yáñez", "Zamora", "Zaragoza", "Zavala", "Zúñiga", "del Río", "del Valle", "Álvarez"),
	"diseases_list": ("pneumonia", "tuberculosis", "common_cold", "influenza", "diabetes", "hypertension", "asthma", "bronchitis", "covid_19", "arthritis", "migraine", "osteoporosis", "gastroenteritis", "malaria"),
	"positive_traits": ("generous", "brave", "honest", "confident", "optimistic", "patient", "gentle", "intelligent", "tolerant", "organized", "compassionate", "persistent", "ambitious"),
	"negative_traits": ("selfish", "coward", "dishonest", "insecure", "pessimistic", "impatient", "rude", "silly", "repugnance", "messy", "insensitive", "desisted", "sensual_hot"),
	"incompatibilities": {
        ("generous", "selfish"),
        ("generous", "insensitive"),
        ("generous", "rude"),
        ("generous", "repugnance"),
        ("brave", "selfish"),
        ("brave", "insensitive"),
        ("brave", "coward"),
        ("brave", "insecure"),
        ("honest", "dishonest"),
        ("confident", "desisted"),
        ("confident", "coward"),
        ("optimistic", "insensitive"),
        ("optimistic", "insecure"),
        ("optimistic", "impatient"),
        ("optimistic", "pessimistic"),
        ("patient", "selfish"),
        ("patient", "impatient"),
        ("gentle", "selfish"),
        ("gentle", "rude"),
        ("gentle", "insensitive"),
        ("gentle", "repugnance"),
        ("intelligent", "silly"),
        ("tolerant", "selfish"),
        ("tolerant", "insensitive"),
        ("tolerant", "impatient"),
        ("tolerant", "rude"),
        ("tolerant", "repugnance"),
        ("organized", "messy"),
        ("compassionate", "selfish"),
        ("compassionate", "insensitive"),
        ("compassionate", "impatient"),
        ("compassionate", "rude"),
        ("compassionate", "repugnance"),
        ("persistent", "desisted"),
        ("persistent", "insecure"),
        ("persistent", "pessimistic"),
        ("ambitious", "insecure"),
        ("ambitious", "messy"),
        ("ambitious", "desisted")
    },
	"countries": {
		"maxico": {
			"economic_status": "medium",
			"weather": "hot"
		},
		"napama": {
			"economic_status": "high",
			"weather": "hot"
		},
		"tangamandapio": {
			"economic_status": "low",
			"weather": "hot"
		},
		"aftagisnan": {
			"economic_status": "hot",
			"weather": "cold"
		},
		"peur": {
			"economic_status": "medium",
			"weather": "cold"
		}
	},
	"valid_traits": [],
	"humans_list": []
}

positive_combinations = list(combinations(data["positive_traits"], 2))
negative_combinations = list(combinations(data["negative_traits"], 2))

for pos_comb, neg_comb in product(positive_combinations, negative_combinations):
	if all(((pos1, neg1) not in data["incompatibilities"] and (neg1, pos1) not in data["incompatibilities"]) for pos1, neg1 in product(pos_comb, neg_comb)):
		data["valid_traits"].append((pos_comb, neg_comb))

data["valid_names"] = list(product(data["human_names"], data["human_surnames"]))

random.shuffle(data["valid_names"])
random.shuffle(data["valid_traits"])

#! HUMANO
#? MÉTODOS:
# interactuar(Otro_Humano)

class Human:
	def __init__(self, name: str = None, /, lifetime: int = None, country: str = None, *, relations: dict[int, dict[str, int]] = None, personality: tuple[tuple[str], tuple[str]] = None, diseases: dict[str, int] = None) -> None:
		if not name:
			first_name, surname = data["valid_names"].pop()
			name = f"{first_name} {surname}"
		if not lifetime: lifetime = random.randint(15, 30)
		if not country: country = random.choice(tuple(data["countries"].keys()))
		if not personality: personality = random.choice(data["valid_traits"])
		if not diseases: diseases = {}

		self.name = name
		self.lifetime = lifetime
		self.country = country
		self.relations = relations
		self.personality = personality
		self.diseases = diseases
		self.edad = 0

		data["humans_list"].append(self)

		self._hni = self.hni

	@property
	def hni(self) -> int:
		return data["humans_list"].index(self)

	@hni.setter
	def hni(self, _) -> None:
		raise AttributeError("Attempt to modify a read-only property")

	def __str__(self) -> str: return self.name
	def __int__(self) -> int: return self.hni

	def has_trait(self, trait_name: str) -> bool:
		return trait_name in self.personality[0] or trait_name in self.personality[1]
	
	def has_disease(self, disease_name: str) -> bool:
		return disease_name in self.diseases

	def alterate_disease(self, disease_name: str, intensity: int = None, *, increment: int = 0) -> None:
		disease_in_entity: bool = disease_name in self.diseases
		valid_intensity: bool = intensity == -1 or 0 < intensity <= 100 if intensity else False
		is_ailment: bool = self.diseases[disease_name] == -1 if disease_in_entity else False

		if not valid_intensity and disease_in_entity: intensity = self.diseases[disease_name]

		if disease_name in data["diseases_list"] and not is_ailment:
			if 0 < intensity + increment <= 100 or intensity + increment == -1:
				self.diseases[disease_name] = intensity + increment
			else:
				del self.diseases[disease_name]

test = Human(diseases={"pneumonia": 40, "tuberculosis": 60})
print(test.personality)