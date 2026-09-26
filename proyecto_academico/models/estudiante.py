# TUPLA de campos: el orden y los nombres son fijos, por eso no es una lista.
# La usan el Controlador y la Vista para no repetir textos sueltos.
CAMPOS_ESTUDIANTE = ("cedula", "nombres", "apellidos", "email", "carrera")


class Estudiante:
    """MODELO (COMPLETO): representa a un estudiante del sistema académico."""

    def __init__(self, id_estudiante, cedula, nombres, apellidos, email, carrera):
        self.id = id_estudiante
        self.cedula = cedula
        self.nombres = nombres
        self.apellidos = apellidos
        self.email = email
        self.carrera = carrera

    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    def a_diccionario(self):
        # Objeto -> diccionario (listo para guardar en JSON)
        return {
            "id": self.id,
            "cedula": self.cedula,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "email": self.email,
            "carrera": self.carrera,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        # Diccionario -> objeto. Método de CLASE: Estudiante.desde_diccionario({...})
        return cls(
            datos["id"],
            datos["cedula"],
            datos["nombres"],
            datos["apellidos"],
            datos["email"],
            datos.get("carrera", ""),
        )

    def __str__(self):
        return f"[{self.cedula}] {self.nombre_completo()} - {self.carrera}"
