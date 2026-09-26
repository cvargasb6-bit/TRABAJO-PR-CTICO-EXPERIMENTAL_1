from shared.consola import imprimir_titulo, imprimir_info, imprimir_error, pausa
from views.interfaz_consola import InterfazConsola


class SistemaAcademico:
    """Integra todo el sistema: arma el menú principal y despacha hacia
    los submenús de cada entidad que vive en InterfazConsola."""

    def __init__(self):
        self.interfaz = InterfazConsola()
        # DICCIONARIO de opciones: tecla -> (texto del menú, función a ejecutar)
        self.opciones = {
            "1": ("Gestión de Estudiantes", self.interfaz.menu_estudiantes),
            "2": ("Gestión de Docentes", self.interfaz.menu_docentes),
            "3": ("Gestión de Asignaturas", self.interfaz.menu_asignaturas),
            "4": ("Gestión de Cursos", self.interfaz.menu_cursos),
            "0": ("Salir", None),
        }

    def mostrar_menu_principal(self):
        imprimir_titulo("SISTEMA ACADÉMICO - MVC")
        for tecla, (texto, _funcion) in self.opciones.items():
            print(f"  {tecla}. {texto}")
        print()

    def ejecutar(self):
        while True:
            self.mostrar_menu_principal()
            tecla = input("Seleccione una opción: ").strip()

            if tecla == "0":
                imprimir_info("¡Hasta luego! 👋")
                break

            if tecla not in self.opciones:
                imprimir_error("Opción no válida")
                pausa()
                continue

            _texto, funcion = self.opciones[tecla]
            funcion()


if __name__ == "__main__":
    try:
        SistemaAcademico().ejecutar()
    except KeyboardInterrupt:
        print("\nPrograma interrumpido por el usuario.")
