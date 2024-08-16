from pydantic import BaseModel
from generator.generar_datos import translations

translations = translations["objects"]

class Objeto(BaseModel):
	name: int
	type: int
	description: int
	obtained: bool = False
	
	def __str__(self) -> str:
		return f"{translations["names"][self.name]}: {translations["descriptions"][self.description]}: {translations["types"][self.type]}"
	def has_it(self): return self.obtained

Shinigami_eyes = Objeto(name=0, type=0, description=0)
