# TUPLA de campos: mismo patrón que CAMPOS_ESTUDIANTE.
CAMPOS_DOCENTE = ("cedula", "nombres", "apellidos", "email", "titulo", "especialidad")


class Docente:
    """MODELO (TAREA 1): representa a un docente del sistema académico.

    Construida por analogía con Estudiante (COMPLETO): mismos dos métodos
    bisagra (a_diccionario / desde_diccionario) y el mismo estilo de __str__.
    """

    def __init__(self, id_docente, cedula, nombres, apellidos, email, titulo, especialidad):
        self.id = id_docente
        self.cedula = cedula
        self.nombres = nombres
        self.apellidos = apellidos
        self.email = email
        self.titulo = titulo            # ej: "Ingeniero", "Magíster"
        self.especialidad = especialidad  # ej: "Estructuras de datos"

    def nombre_completo(self):
        return f"{self.nombres} {self.apellidos}"

    def a_diccionario(self):
        return {
            "id": self.id,
            "cedula": self.cedula,
            "nombres": self.nombres,
            "apellidos": self.apellidos,
            "email": self.email,
            "titulo": self.titulo,
            "especialidad": self.especialidad,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["cedula"],
            datos["nombres"],
            datos["apellidos"],
            datos["email"],
            datos.get("titulo", ""),
            datos.get("especialidad", ""),
        )

    def __str__(self):
        return f"[{self.cedula}] {self.titulo} {self.nombre_completo()} - {self.especialidad}"
