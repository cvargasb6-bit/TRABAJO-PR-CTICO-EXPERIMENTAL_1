from models.docente import Docente, CAMPOS_DOCENTE
from shared.archivo_json import ArchivoJSON
from shared.validaciones import es_email_valido, es_cedula_valida, texto_no_vacio

archivo = ArchivoJSON("data/docentes.json")

CAMPOS_OBLIGATORIOS = ("cedula", "nombres", "apellidos", "email")
CAMPOS_BUSCABLES = ("cedula", "nombres", "apellidos", "email", "especialidad")


# ===================== AYUDAS INTERNAS =====================

def _cedulas_registradas(excepto_id=None):
    """CONJUNTO con las cédulas ya usadas (mismo patrón que en ControladorEstudiante)."""
    return {
        registro["cedula"]
        for registro in archivo.leer()
        if registro["id"] != excepto_id
    }


def _emails_registrados(excepto_id=None):
    return {
        registro["email"].lower()
        for registro in archivo.leer()
        if registro["id"] != excepto_id
    }


# ===================== C · CREATE =====================

def crear_docente(datos):
    try:
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_DOCENTE}

        faltantes = [campo for campo in CAMPOS_OBLIGATORIOS if not valores[campo]]
        if faltantes:
            return False, f"Faltan campos obligatorios: {', '.join(faltantes)}"

        if not es_cedula_valida(valores["cedula"]):
            return False, "La cédula debe tener 10 dígitos numéricos"

        if not es_email_valido(valores["email"]):
            return False, f"El email '{valores['email']}' no tiene un formato válido"

        if valores["cedula"] in _cedulas_registradas():
            return False, "Esa cédula ya está registrada"

        if valores["email"].lower() in _emails_registrados():
            return False, "Ese email ya está registrado"

        docente = Docente(archivo.siguiente_id(), **valores)

        registros = archivo.leer()
        registros.append(docente.a_diccionario())
        if not archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, f"Docente {docente.nombre_completo()} creado con id {docente.id}"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    return [Docente.desde_diccionario(registro) for registro in archivo.leer()]


def obtener_por_id(id_docente):
    for docente in obtener_todos():
        if docente.id == id_docente:
            return docente
    return None


# ===================== S · SEARCH =====================

def buscar_docentes(termino):
    termino = termino.strip().lower()
    if not termino:
        return []
    encontrados = []
    for registro in archivo.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Docente.desde_diccionario(registro))
                break
    return encontrados


# ===================== U · UPDATE =====================

def actualizar_docente(id_docente, cambios):
    try:
        desconocidos = set(cambios) - set(CAMPOS_DOCENTE)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se indicó ningún cambio"

        if "cedula" in cambios:
            if not es_cedula_valida(cambios["cedula"]):
                return False, "La cédula debe tener 10 dígitos numéricos"
            if cambios["cedula"] in _cedulas_registradas(excepto_id=id_docente):
                return False, "Esa cédula ya la usa otro docente"

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            if cambios["email"].lower() in _emails_registrados(excepto_id=id_docente):
                return False, "Ese email ya lo usa otro docente"

        registros = archivo.leer()
        posicion = None
        for indice, registro in enumerate(registros):
            if registro["id"] == id_docente:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un docente con id {id_docente}"

        registros[posicion].update(cambios)
        archivo.guardar(registros)
        return True, f"Docente {id_docente} actualizado ({len(cambios)} campo/s)"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_docente(id_docente):
    # Regla de integridad: no se elimina un docente que ya dicta una asignatura.
    from controllers.controlador_asignatura import obtener_todos as asignaturas_todas
    en_uso = [a for a in asignaturas_todas() if a.docente_id == id_docente]
    if en_uso:
        nombres = ", ".join(a.nombre for a in en_uso)
        return False, f"No se puede eliminar: el docente dicta {len(en_uso)} asignatura(s): {nombres}"

    registros = archivo.leer()
    quedan = [registro for registro in registros if registro["id"] != id_docente]

    if len(quedan) == len(registros):
        return False, f"No existe un docente con id {id_docente}"

    archivo.guardar(quedan)
    return True, f"Docente {id_docente} eliminado"
