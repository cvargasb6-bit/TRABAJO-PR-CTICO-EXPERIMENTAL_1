from models.curso import Curso, CAMPOS_CURSO
from shared.archivo_json import ArchivoJSON
from shared.validaciones import texto_no_vacio

archivo = ArchivoJSON("data/cursos.json")

CAMPOS_OBLIGATORIOS = ("nombre", "paralelo", "asignatura_id", "docente_id")


def _asignatura_existe(asignatura_id):
    from controllers.controlador_asignatura import obtener_por_id
    return obtener_por_id(asignatura_id) is not None


def _docente_existe(docente_id):
    from controllers.controlador_docente import obtener_por_id
    return obtener_por_id(docente_id) is not None


def _estudiante_existe(estudiante_id):
    from controllers.controlador_estudiante import obtener_por_id
    return obtener_por_id(estudiante_id) is not None


# ===================== C · CREATE =====================

def crear_curso(datos):
    try:
        nombre = str(datos.get("nombre", "")).strip()
        paralelo = str(datos.get("paralelo", "")).strip()
        asignatura_id = datos.get("asignatura_id")
        docente_id = datos.get("docente_id")

        if not texto_no_vacio(nombre) or not texto_no_vacio(paralelo):
            return False, "Faltan campos obligatorios: nombre, paralelo"

        try:
            asignatura_id = int(asignatura_id)
            docente_id = int(docente_id)
        except (TypeError, ValueError):
            return False, "asignatura_id y docente_id deben ser números"

        if not _asignatura_existe(asignatura_id):
            return False, f"No existe una asignatura con id {asignatura_id}"

        if not _docente_existe(docente_id):
            return False, f"No existe un docente con id {docente_id}"

        curso = Curso(archivo.siguiente_id(), nombre, paralelo, asignatura_id, docente_id)

        registros = archivo.leer()
        registros.append(curso.a_diccionario())
        if not archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, f"Curso {curso.nombre} creado con id {curso.id}"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    return [Curso.desde_diccionario(registro) for registro in archivo.leer()]


def obtener_por_id(id_curso):
    for curso in obtener_todos():
        if curso.id == id_curso:
            return curso
    return None


# ===================== S · SEARCH =====================

def buscar_cursos(termino):
    termino = termino.strip().lower()
    if not termino:
        return []
    return [curso for curso in obtener_todos()
            if termino in curso.nombre.lower() or termino in curso.paralelo.lower()]


# ===================== U · UPDATE =====================

def actualizar_curso(id_curso, cambios):
    try:
        desconocidos = set(cambios) - set(CAMPOS_CURSO)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se indicó ningún cambio"

        if "asignatura_id" in cambios:
            cambios["asignatura_id"] = int(cambios["asignatura_id"])
            if not _asignatura_existe(cambios["asignatura_id"]):
                return False, f"No existe una asignatura con id {cambios['asignatura_id']}"

        if "docente_id" in cambios:
            cambios["docente_id"] = int(cambios["docente_id"])
            if not _docente_existe(cambios["docente_id"]):
                return False, f"No existe un docente con id {cambios['docente_id']}"

        registros = archivo.leer()
        posicion = None
        for indice, registro in enumerate(registros):
            if registro["id"] == id_curso:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un curso con id {id_curso}"

        registros[posicion].update(cambios)
        archivo.guardar(registros)
        return True, f"Curso {id_curso} actualizado ({len(cambios)} campo/s)"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_curso(id_curso):
    registros = archivo.leer()
    quedan = [registro for registro in registros if registro["id"] != id_curso]

    if len(quedan) == len(registros):
        return False, f"No existe un curso con id {id_curso}"

    archivo.guardar(quedan)
    return True, f"Curso {id_curso} eliminado"


# ===================== EXTRA: matrícula con CONJUNTOS =====================

def matricular_estudiante(id_curso, id_estudiante):
    """Agrega un estudiante al CONJUNTO de matriculados del curso."""
    if not _estudiante_existe(id_estudiante):
        return False, f"No existe un estudiante con id {id_estudiante}"

    registros = archivo.leer()
    posicion = next((i for i, r in enumerate(registros) if r["id"] == id_curso), None)
    if posicion is None:
        return False, f"No existe un curso con id {id_curso}"

    curso = Curso.desde_diccionario(registros[posicion])
    if id_estudiante in curso.estudiantes_ids:
        return False, "Ese estudiante ya está matriculado en este curso"

    curso.matricular_estudiante(id_estudiante)
    registros[posicion] = curso.a_diccionario()
    archivo.guardar(registros)
    return True, f"Estudiante {id_estudiante} matriculado en {curso.nombre}"


def retirar_estudiante(id_curso, id_estudiante):
    """Quita un estudiante del CONJUNTO de matriculados del curso."""
    registros = archivo.leer()
    posicion = next((i for i, r in enumerate(registros) if r["id"] == id_curso), None)
    if posicion is None:
        return False, f"No existe un curso con id {id_curso}"

    curso = Curso.desde_diccionario(registros[posicion])
    if id_estudiante not in curso.estudiantes_ids:
        return False, "Ese estudiante no está matriculado en este curso"

    curso.retirar_estudiante(id_estudiante)
    registros[posicion] = curso.a_diccionario()
    archivo.guardar(registros)
    return True, f"Estudiante {id_estudiante} retirado de {curso.nombre}"


def companeros_en_comun(id_curso_a, id_curso_b):
    """INTERSECCIÓN de conjuntos: estudiantes matriculados en ambos cursos a la vez."""
    curso_a = obtener_por_id(id_curso_a)
    curso_b = obtener_por_id(id_curso_b)

    if not curso_a:
        return False, f"No existe un curso con id {id_curso_a}"
    if not curso_b:
        return False, f"No existe un curso con id {id_curso_b}"

    return True, curso_a.estudiantes_ids & curso_b.estudiantes_ids
