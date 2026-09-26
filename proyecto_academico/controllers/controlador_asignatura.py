from models.asignatura import Asignatura, CAMPOS_ASIGNATURA
from shared.archivo_json import ArchivoJSON
from shared.validaciones import es_numero_en_rango, texto_no_vacio

archivo = ArchivoJSON("data/asignaturas.json")

CAMPOS_OBLIGATORIOS = ("codigo", "nombre", "creditos")
CAMPOS_BUSCABLES = ("codigo", "nombre")


def _codigos_registrados(excepto_id=None):
    """CONJUNTO con los códigos ya usados: ninguna asignatura se repite."""
    return {
        registro["codigo"].lower()
        for registro in archivo.leer()
        if registro["id"] != excepto_id
    }


def _docente_existe(docente_id):
    # Importa aquí (no arriba) para evitar import circular con controlador_docente
    from controllers.controlador_docente import obtener_por_id
    return obtener_por_id(docente_id) is not None


# ===================== C · CREATE =====================

def crear_asignatura(datos):
    try:
        codigo = str(datos.get("codigo", "")).strip()
        nombre = str(datos.get("nombre", "")).strip()
        creditos = datos.get("creditos", "")
        docente_id = datos.get("docente_id") or None

        if not texto_no_vacio(codigo) or not texto_no_vacio(nombre):
            return False, "Faltan campos obligatorios: codigo, nombre"

        if not es_numero_en_rango(creditos, 1, 10):
            return False, "Los créditos deben ser un número entre 1 y 10"

        if codigo.lower() in _codigos_registrados():
            return False, "Ese código de asignatura ya está registrado"

        if docente_id is not None:
            docente_id = int(docente_id)
            if not _docente_existe(docente_id):
                return False, f"No existe un docente con id {docente_id}"

        asignatura = Asignatura(archivo.siguiente_id(), codigo, nombre, int(float(creditos)), docente_id)

        registros = archivo.leer()
        registros.append(asignatura.a_diccionario())
        if not archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, f"Asignatura {asignatura.nombre} creada con id {asignatura.id}"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    return [Asignatura.desde_diccionario(registro) for registro in archivo.leer()]


def obtener_por_id(id_asignatura):
    for asignatura in obtener_todos():
        if asignatura.id == id_asignatura:
            return asignatura
    return None


# ===================== S · SEARCH =====================

def buscar_asignaturas(termino):
    termino = termino.strip().lower()
    if not termino:
        return []
    encontradas = []
    for registro in archivo.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                encontradas.append(Asignatura.desde_diccionario(registro))
                break
    return encontradas


# ===================== U · UPDATE =====================

def actualizar_asignatura(id_asignatura, cambios):
    try:
        desconocidos = set(cambios) - set(CAMPOS_ASIGNATURA)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se indicó ningún cambio"

        if "codigo" in cambios:
            if cambios["codigo"].lower() in _codigos_registrados(excepto_id=id_asignatura):
                return False, "Ese código ya lo usa otra asignatura"

        if "creditos" in cambios:
            if not es_numero_en_rango(cambios["creditos"], 1, 10):
                return False, "Los créditos deben ser un número entre 1 y 10"
            cambios["creditos"] = int(float(cambios["creditos"]))

        if "docente_id" in cambios and cambios["docente_id"]:
            docente_id = int(cambios["docente_id"])
            if not _docente_existe(docente_id):
                return False, f"No existe un docente con id {docente_id}"
            cambios["docente_id"] = docente_id

        registros = archivo.leer()
        posicion = None
        for indice, registro in enumerate(registros):
            if registro["id"] == id_asignatura:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe una asignatura con id {id_asignatura}"

        registros[posicion].update(cambios)
        archivo.guardar(registros)
        return True, f"Asignatura {id_asignatura} actualizada ({len(cambios)} campo/s)"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_asignatura(id_asignatura):
    # Regla de integridad: no se elimina si algún curso ya la está usando.
    from controllers.controlador_curso import obtener_todos as cursos_todos
    en_uso = [c for c in cursos_todos() if c.asignatura_id == id_asignatura]
    if en_uso:
        return False, f"No se puede eliminar: hay {len(en_uso)} curso(s) que la usan"

    registros = archivo.leer()
    quedan = [registro for registro in registros if registro["id"] != id_asignatura]

    if len(quedan) == len(registros):
        return False, f"No existe una asignatura con id {id_asignatura}"

    archivo.guardar(quedan)
    return True, f"Asignatura {id_asignatura} eliminada"
