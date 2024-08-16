import re
import ast
from collections import OrderedDict
import json

class TupleWrapper:
    def __init__(self, tup):
        self.tup = tup
    
    def __getitem__(self, index):
        return self.tup[index]
    
    def __str__(self):
        return f'"{self.tup[0]}"-> {repr(self.tup[1])}'


class VECTOR3D(list):
    """
    Una clase que combina funcionalidades de lista y diccionario, permitiendo
    acceso tanto por índice como por clave.

    Esta clase hereda de list y agrega funcionalidad de diccionario, manteniendo
    el orden de inserción de los elementos. Permite la inicialización a partir de
    una cadena con formato específico.

    Attributes:
        _dict (OrderedDict): Diccionario ordenado interno para almacenar pares clave-valor.
        _original_string (str): Cadena original utilizada para inicializar el SuperArray.
        _original_elements (list): Lista de elementos originales en formato de cadena.
    """

    def __init__(self, string):
        """
        Inicializa un nuevo SuperArray a partir de una cadena.

        Args:
            string (str): Cadena que representa el SuperArray en formato específico.
        """
        super().__init__()
        self._dict = OrderedDict()
        self._original_string = string
        self._original_elements = []
        self._parse(string)

    def _parse(self, string):
        """
        Analiza la cadena de entrada y crea los elementos del SuperArray.

        Args:
            string (str): Cadena que representa el SuperArray sin los corchetes externos.
        """
        string = string.strip()[1:-1]  # Elimina los corchetes externos
        elements = self._split_elements(string)
        
        for element in elements:
            self._add_element(element.strip())

    def _split_elements(self, string):
        """
        Divide la cadena en elementos individuales, respetando los corchetes anidados.

        Args:
            string (str): Cadena que representa el contenido del SuperArray.

        Returns:
            list: Lista de elementos individuales como cadenas.
        """
        elements = []
        current = []
        level = 0
        for char in string:
            if char == ',' and level == 0:
                elements.append(''.join(current).strip())
                current = []
            else:
                if char == '[':
                    level += 1
                elif char == ']':
                    level -= 1
                current.append(char)
        if current:
            elements.append(''.join(current).strip())
        return elements

    def _add_element(self, element):
        """
        Agrega un elemento al SuperArray, procesándolo según su formato.

        Args:
            element (str): Elemento a agregar, puede ser un par clave-valor o un valor simple.
        """
        self._original_elements.append(element)
        if '->' in element:
            key, value = element.split('->', 1)
            key = key.strip().strip('"')
            value = self._safe_eval(value.strip())
            self._dict[key] = value
            super().append((key, value))
        else:
            super().append(self._safe_eval(element))

    def _safe_eval(self, value):
        """
        Evalúa de forma segura una cadena para convertirla en su tipo de dato correspondiente.

        Args:
            value (str): Cadena a evaluar.

        Returns:
            El valor convertido al tipo de dato correspondiente, o la cadena original si no se puede evaluar.
        """
        try:
            return ast.literal_eval(value)
        except:
            return value

    def append(self, item):
        """
        Agrega un nuevo elemento al final del SuperArray.

        Args:
            item: Elemento a agregar. Puede ser una cadena o cualquier otro tipo de dato.
        """
        if isinstance(item, str):
            self._add_element(item)
        else:
            super().append(item)
            self._original_elements.append(repr(item))
        self._update_original_string()

    def _update_original_string(self):
        """
        Actualiza la cadena original basada en los elementos actuales del SuperArray.
        """
        self._original_string = f"[{', '.join(self._original_elements)}]"

    def __getitem__(self, key):
        """
        Obtiene un elemento del SuperArray por índice o clave.

        Args:
            key: Índice (int) o clave (str) del elemento a obtener.

        Returns:
            El elemento correspondiente al índice o clave proporcionada.
        """
        if isinstance(key, int):
            item = super().__getitem__(key)
            if isinstance(item, tuple):
                return TupleWrapper(item)
            return item
        elif isinstance(key, str):
            return self._dict[key]
        return self._dict[key]
    
    def __repr__(self):
        """
        Devuelve una representación en cadena del SuperArray.

        Returns:
            str: Representación en cadena del SuperArray.
        """
        return self._original_string

    def __len__(self):
        """
        Devuelve la cantidad de elementos en el SuperArray.

        Returns:
            int: Número de elementos en el SuperArray.
        """
        return super().__len__()

    def __iter__(self):
        """
        Devuelve un iterador sobre los elementos del SuperArray.

        Returns:
            iterator: Iterador sobre los elementos del SuperArray.
        """
        return super().__iter__()

    def __contains__(self, item):
        """
        Verifica si un elemento está presente en el SuperArray.

        Args:
            item: Elemento a buscar.

        Returns:
            bool: True si el elemento está presente, False en caso contrario.
        """
        return item in self._dict or super().__contains__(item)

    def keys(self):
        """
        Devuelve una vista de las claves del SuperArray.

        Returns:
            dict_keys: Vista de las claves del SuperArray.
        """
        return self._dict.keys()

    def values(self):
        """
        Devuelve una vista de los valores del SuperArray.

        Returns:
            dict_values: Vista de los valores del SuperArray.
        """
        return self._dict.values()

    def items(self):
        """
        Devuelve una vista de los pares clave-valor del SuperArray.

        Returns:
            dict_items: Vista de los pares clave-valor del SuperArray.
        """
        return self._dict.items()

    def get(self, key, default=None):
        """
        Obtiene el valor de una clave, con un valor por defecto si no existe.

        Args:
            key: Clave a buscar.
            default: Valor a devolver si la clave no existe (por defecto None).

        Returns:
            El valor asociado a la clave, o el valor por defecto si la clave no existe.
        """
        return self._dict.get(key, default)

    def pop(self, key):
        """
        Elimina y devuelve el elemento con la clave o índice dado.

        Args:
            key: Clave o índice del elemento a eliminar.

        Returns:
            El valor del elemento eliminado.
        """
        if isinstance(key, int):
            value = super().pop(key)
            self._original_elements.pop(key)
        else:
            value = self._dict.pop(key)
            index = next(i for i, v in enumerate(self) if isinstance(v, tuple) and v[0] == key)
            super().pop(index)
            self._original_elements = [e for e in self._original_elements if not e.startswith(f'"{key}" ->')]
        self._update_original_string()
        return value

    def update(self, other):
        """
        Actualiza el SuperArray con los elementos de otro diccionario o SuperArray.

        Args:
            other: Diccionario o SuperArray con los elementos a agregar.
        """
        if isinstance(other, VECTOR3D):
            other = other.to_dict()
        for key, value in other.items():
            self.append(f'"{key}" -> {repr(value)}')

    def clear(self):
        """
        Elimina todos los elementos del SuperArray.
        """
        super().clear()
        self._dict.clear()
        self._original_elements.clear()
        self._original_string = "[]"

    def copy(self):
        """
        Devuelve una copia superficial del SuperArray.

        Returns:
            SuperArray: Una nueva instancia de SuperArray con los mismos elementos.
        """
        return VECTOR3D(self._original_string)

    def setdefault(self, key, default=None):
        """
        Inserta una clave con un valor si la clave no existe.

        Args:
            key: Clave a insertar.
            default: Valor a asociar con la clave si esta no existe (por defecto None).

        Returns:
            El valor asociado con la clave, ya sea el existente o el recién insertado.
        """
        if key not in self._dict:
            self.append(f'"{key}" -> {repr(default)}')
        return self._dict[key]

    def to_dict(self):
        """
        Convierte el SuperArray a un diccionario ordenado.

        Returns:
            OrderedDict: Un diccionario ordenado con los elementos del SuperArray.
        """
        return OrderedDict(self._dict)

    def to_list(self):
        """
        Convierte el SuperArray a una lista.

        Returns:
            list: Una lista con los elementos del SuperArray.
        """
        return list(self)
    
    def find(self, condition):
        """
        Busca elementos en el SuperArray que cumplan con una condición dada.

        Args:
            condition (callable): Una función que toma un elemento y devuelve True si cumple con la condición.

        Returns:
            list: Lista de elementos que cumplen con la condición.
        """
        return [element for element in self if condition(element)]


# Crear una instancia de SuperArray
v1 = 1
v2 = 2
a = VECTOR3D(f'[{v1}, "v2"->{v2}, "tres" -> 3, [4, 5], "letras" -> ["A", "B", "C"], 10, -1, "cuatro" -> 4 ]')
print(a["v2"])        # 2 
print(a[1])           #'"v2"-> 2' #esta es la cadena que debe devolver el segundo output
print(a[1][1])        # 2
print(a[1][0])        #"v2"
print(a["letras"][0]) #a