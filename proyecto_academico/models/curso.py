# TUPLA de campos básicos del curso (sin contar los estudiantes matriculados,
# que se manejan aparte porque son una colección, no un campo simple).
CAMPOS_CURSO = ("nombre", "paralelo", "asignatura_id", "docente_id")


class Curso:
    """MODELO (TAREA 3): una sección/paralelo concreto de una Asignatura,
    dictado por un Docente, con un grupo de Estudiantes matriculados.

    Es la entidad que más colecciones usa: un CONJUNTO para los estudiantes
    (nadie puede estar matriculado dos veces) y una TUPLA para los campos fijos.
    """

    def __init__(self, id_curso, nombre, paralelo, asignatura_id, docente_id,
                 estudiantes_ids=None):
        self.id = id_curso
        self.nombre = nombre                  # ej: "Estructura de Datos - Paralelo A"
        self.paralelo = paralelo              # ej: "A", "B"
        self.asignatura_id = asignatura_id    # referencia a Asignatura.id
        self.docente_id = docente_id          # referencia a Docente.id
        # CONJUNTO: ids de estudiantes matriculados, sin repetidos
        self.estudiantes_ids = set(estudiantes_ids) if estudiantes_ids else set()

    def matricular_estudiante(self, id_estudiante):
        # add() no duplica: si ya estaba matriculado, no pasa nada
        self.estudiantes_ids.add(id_estudiante)

    def retirar_estudiante(self, id_estudiante):
        # discard() no lanza error si el id no estaba (a diferencia de remove())
        self.estudiantes_ids.discard(id_estudiante)

    def total_matriculados(self):
        return len(self.estudiantes_ids)

    def a_diccionario(self):
        return {
            "id": self.id,
            "nombre": self.nombre,
            "paralelo": self.paralelo,
            "asignatura_id": self.asignatura_id,
            "docente_id": self.docente_id,
            # JSON no sabe guardar un set: lo convertimos a lista ordenada
            "estudiantes_ids": sorted(self.estudiantes_ids),
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["nombre"],
            datos.get("paralelo", ""),
            datos.get("asignatura_id"),
            datos.get("docente_id"),
            estudiantes_ids=set(datos.get("estudiantes_ids", [])),
        )

    def __str__(self):
        return f"{self.nombre} (Paralelo {self.paralelo}) - {self.total_matriculados()} matriculado(s)"
