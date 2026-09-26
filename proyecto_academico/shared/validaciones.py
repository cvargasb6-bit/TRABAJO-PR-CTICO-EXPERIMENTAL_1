# Funciones de validación reutilizadas por todos los controladores.
# Ninguna toca el disco ni imprime nada: solo devuelven True/False.

# TUPLA: sufijos de correo institucional aceptados (fija, no cambia en ejecución)
DOMINIOS_PERMITIDOS = (".edu", ".edu.ec", ".com", ".org", ".net")


def es_email_valido(texto):
    """Validación mínima: un @, algo antes, algo después y un punto al final."""
    texto = (texto or "").strip()
    if texto.count("@") != 1:
        return False
    usuario, dominio = texto.split("@")
    return len(usuario) > 0 and "." in dominio and not dominio.endswith(".")


def es_cedula_valida(texto):
    """Cédula ecuatoriana: 10 dígitos numéricos."""
    texto = (texto or "").strip()
    return texto.isdigit() and len(texto) == 10


def es_numero_en_rango(valor, minimo, maximo):
    """Valida que 'valor' sea numérico y esté entre minimo y maximo (inclusive)."""
    try:
        numero = float(valor)
    except (TypeError, ValueError):
        return False
    return minimo <= numero <= maximo


def texto_no_vacio(texto):
    return bool((texto or "").strip())
