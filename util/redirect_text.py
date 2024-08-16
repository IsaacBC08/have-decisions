import sys
import flet as ft
import time
from threading import Thread

class StdoutRedirector:
    def __init__(self, text_component: ft.Text, scroll_container: ft.Column):
        self.text_component = text_component
        self.scroll_container = scroll_container
        self.old_stdout = sys.stdout
        sys.stdout = self
        self.buffer = ""
        self.writing = False
        self.stop_writing = False 
        self.slow_text_markers = ["[LENTO]"]
        self.normal_speed = 0.00012
        self.slow_speed = 0.02

    def write(self, text: str):
        self.buffer += text
        if not self.writing:
            self.writing = True
            Thread(target=self._animate_typing).start()
    
    def flush(self):
        pass

    def _animate_typing(self):
        current_line = ""
        is_slow = False
        
        while (self.buffer or current_line) and not self.stop_writing:
            if not current_line and self.buffer:
                if '\n' in self.buffer:
                    current_line, self.buffer = self.buffer.split('\n', 1)
                    current_line += '\n'
                else:
                    current_line = self.buffer
                    self.buffer = ""
                
                is_slow = any(marker in current_line for marker in self.slow_text_markers)
                current_line = self._remove_markers(current_line)
            
            if current_line:
                char = current_line[0]
                current_line = current_line[1:]
                
                self.text_component.value += char
                self.text_component.update()
                self.scroll_container.scroll_to(offset=-1, duration=100)
                
                speed = self.slow_speed if is_slow else self.normal_speed
                time.sleep(speed)

        self.writing = False

    def limpiar_consola(self):
        # Detener la escritura en curso
        self.stop_writing = True
        # Esperar a que cualquier hilo de escritura termine
        while self.writing:
            time.sleep(0.1)
        # Limpiar el contenido del Text component
        self.text_component.value = ""
        self.text_component.update()
        # Vaciar el buffer
        self.buffer = ""
        # Resetear el indicador de escritura y stop_writing
        self.writing = False
        self.stop_writing = False

    def _remove_markers(self, text):
        for marker in self.slow_text_markers:
            text = text.replace(marker, '')
        return text

    def __del__(self):
        sys.stdout = self.old_stdout
