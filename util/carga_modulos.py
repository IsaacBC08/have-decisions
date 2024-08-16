import sys
import os

def cargar(modulo):
	sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', modulo)))
