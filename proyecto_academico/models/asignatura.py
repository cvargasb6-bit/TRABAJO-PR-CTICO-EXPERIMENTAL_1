# TUPLA de campos de la asignatura.
CAMPOS_ASIGNATURA = ("codigo", "nombre", "creditos", "docente_id")


class Asignatura:
    """MODELO (TAREA 2): representa una materia del pénsum.

    'docente_id' es una referencia al id de un Docente (relación entre
    entidades): el Controlador es quien valida que ese id exista.
    """

    def __init__(self, id_asignatura, codigo, nombre, creditos, docente_id=None):
        self.id = id_asignatura
        self.codigo = codigo          # ej: "EST-DAT-101"
        self.nombre = nombre
        self.creditos = int(creditos)
        self.docente_id = docente_id  # None si todavía no tiene docente asignado

    def a_diccionario(self):
        return {
            "id": self.id,
            "codigo": self.codigo,
            "nombre": self.nombre,
            "creditos": self.creditos,
            "docente_id": self.docente_id,
        }

    @classmethod
    def desde_diccionario(cls, datos):
        return cls(
            datos["id"],
            datos["codigo"],
            datos["nombre"],
            datos.get("creditos", 0),
            datos.get("docente_id"),
        )

    def __str__(self):
        docente_txt = f"docente_id={self.docente_id}" if self.docente_id else "sin docente"
        return f"[{self.codigo}] {self.nombre} ({self.creditos} créditos) - {docente_txt}"
