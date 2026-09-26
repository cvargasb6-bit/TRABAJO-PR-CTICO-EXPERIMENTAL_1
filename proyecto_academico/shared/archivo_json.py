import json
import os


class ArchivoJSON:
    """Lee y guarda una LISTA de diccionarios en un archivo JSON.

    Es la única parte del sistema que toca el disco; no sabe qué es un
    Estudiante, un Docente, etc. — solo mueve listas de diccionarios.
    """

    def __init__(self, ruta):
        self.ruta = ruta
        carpeta = os.path.dirname(ruta)
        if carpeta and not os.path.exists(carpeta):
            os.makedirs(carpeta)

    def leer(self):
        # Devuelve SIEMPRE una LISTA: vacía si el archivo no existe o está dañado
        if not os.path.exists(self.ruta):
            return []
        try:
            with open(self.ruta, "r", encoding="utf-8") as archivo:
                datos = json.load(archivo)
            return datos if isinstance(datos, list) else []
        except (json.JSONDecodeError, OSError):
            # Nunca un "except:" pelado: solo capturamos los errores esperados
            return []

    def guardar(self, datos):
        try:
            with open(self.ruta, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, ensure_ascii=False, indent=2)
            return True
        except (TypeError, OSError):
            # TypeError aparece si se intenta guardar un set sin convertirlo antes
            return False

    def siguiente_id(self):
        # Calcula el próximo id disponible a partir de lo que ya hay guardado
        ids = [registro["id"] for registro in self.leer()]
        return max(ids) + 1 if ids else 1
