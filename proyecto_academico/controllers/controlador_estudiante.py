from models.estudiante import Estudiante, CAMPOS_ESTUDIANTE
from shared.archivo_json import ArchivoJSON
from shared.validaciones import es_email_valido, es_cedula_valida

archivo = ArchivoJSON("data/estudiantes.json")

CAMPOS_OBLIGATORIOS = ("cedula", "nombres", "apellidos", "email")
CAMPOS_BUSCABLES = ("cedula", "nombres", "apellidos", "email", "carrera")


# ===================== AYUDAS INTERNAS =====================

def _cedulas_registradas(excepto_id=None):
    """CONJUNTO con las cédulas ya usadas: detecta duplicados al instante."""
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

def crear_estudiante(datos):
    """datos: diccionario con las claves de CAMPOS_ESTUDIANTE. Devuelve (exito, mensaje)."""
    try:
        valores = {campo: str(datos.get(campo, "")).strip() for campo in CAMPOS_ESTUDIANTE}

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

        estudiante = Estudiante(archivo.siguiente_id(), **valores)

        registros = archivo.leer()
        registros.append(estudiante.a_diccionario())
        if not archivo.guardar(registros):
            return False, "No se pudo escribir el archivo"

        return True, f"Estudiante {estudiante.nombre_completo()} creado con id {estudiante.id}"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== R · READ =====================

def obtener_todos():
    """LISTA de objetos Estudiante."""
    return [Estudiante.desde_diccionario(registro) for registro in archivo.leer()]


def obtener_por_id(id_estudiante):
    for estudiante in obtener_todos():
        if estudiante.id == id_estudiante:
            return estudiante
    return None


# ===================== S · SEARCH =====================

def buscar_estudiantes(termino):
    termino = termino.strip().lower()
    if not termino:
        return []
    encontrados = []
    for registro in archivo.leer():
        for campo in CAMPOS_BUSCABLES:
            if termino in str(registro.get(campo, "")).lower():
                encontrados.append(Estudiante.desde_diccionario(registro))
                break
    return encontrados


# ===================== U · UPDATE =====================

def actualizar_estudiante(id_estudiante, cambios):
    try:
        desconocidos = set(cambios) - set(CAMPOS_ESTUDIANTE)
        if desconocidos:
            return False, f"Campos no válidos: {', '.join(sorted(desconocidos))}"

        if not cambios:
            return False, "No se indicó ningún cambio"

        if "cedula" in cambios:
            if not es_cedula_valida(cambios["cedula"]):
                return False, "La cédula debe tener 10 dígitos numéricos"
            if cambios["cedula"] in _cedulas_registradas(excepto_id=id_estudiante):
                return False, "Esa cédula ya la usa otro estudiante"

        if "email" in cambios:
            if not es_email_valido(cambios["email"]):
                return False, "El email no tiene un formato válido"
            if cambios["email"].lower() in _emails_registrados(excepto_id=id_estudiante):
                return False, "Ese email ya lo usa otro estudiante"

        registros = archivo.leer()
        posicion = None
        for indice, registro in enumerate(registros):
            if registro["id"] == id_estudiante:
                posicion = indice
                break

        if posicion is None:
            return False, f"No existe un estudiante con id {id_estudiante}"

        registros[posicion].update(cambios)
        archivo.guardar(registros)
        return True, f"Estudiante {id_estudiante} actualizado ({len(cambios)} campo/s)"

    except Exception as error:
        return False, f"Error inesperado: {error}"


# ===================== D · DELETE =====================

def eliminar_estudiante(id_estudiante):
    registros = archivo.leer()
    quedan = [registro for registro in registros if registro["id"] != id_estudiante]

    if len(quedan) == len(registros):
        return False, f"No existe un estudiante con id {id_estudiante}"

    archivo.guardar(quedan)
    return True, f"Estudiante {id_estudiante} eliminado"
