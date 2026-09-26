from shared.consola import (
    imprimir_titulo, imprimir_exito, imprimir_error, imprimir_info, confirmar, pausa
)

import controllers.controlador_estudiante as ctrl_estudiante
import controllers.controlador_docente as ctrl_docente
import controllers.controlador_asignatura as ctrl_asignatura
import controllers.controlador_curso as ctrl_curso

from models.estudiante import CAMPOS_ESTUDIANTE
from models.docente import CAMPOS_DOCENTE


def _pedir_id(etiqueta="Id"):
    try:
        return int(input(f"{etiqueta}: "))
    except ValueError:
        imprimir_error("El id debe ser un número entero")
        return None


class InterfazConsola:
    """VISTA (COMPLETO): todo el input()/print() del sistema vive aquí.

    No valida reglas de negocio ni toca archivos: solo pide datos, llama a
    los controladores y muestra lo que estos devuelven.
    """

    # =========================================================
    # ESTUDIANTES
    # =========================================================

    def _tabla_estudiantes(self, estudiantes):
        print(f"{'ID':<5}{'CÉDULA':<14}{'NOMBRE':<28}{'EMAIL':<28}{'CARRERA':<20}")
        print("-" * 95)
        for e in estudiantes:
            print(f"{e.id:<5}{e.cedula:<14}{e.nombre_completo():<28}{e.email:<28}{e.carrera:<20}")
        print("-" * 95)
        imprimir_info(f"Total: {len(estudiantes)} estudiante(s)")

    def crear_estudiante(self):
        imprimir_titulo("CREAR ESTUDIANTE")
        datos = {campo: input(f"{campo.capitalize()}: ") for campo in CAMPOS_ESTUDIANTE}
        exito, mensaje = ctrl_estudiante.crear_estudiante(datos)
        imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
        pausa()

    def listar_estudiantes(self):
        imprimir_titulo("LISTA DE ESTUDIANTES")
        estudiantes = ctrl_estudiante.obtener_todos()
        if not estudiantes:
            imprimir_info("Todavía no hay estudiantes registrados.")
        else:
            self._tabla_estudiantes(estudiantes)
        pausa()

    def buscar_estudiantes(self):
        imprimir_titulo("BUSCAR ESTUDIANTE")
        termino = input("Cédula, nombre, apellido, email o carrera: ")
        encontrados = ctrl_estudiante.buscar_estudiantes(termino)
        if not encontrados:
            imprimir_info(f"Ningún estudiante coincide con '{termino}'.")
        else:
            self._tabla_estudiantes(encontrados)
        pausa()

    def actualizar_estudiante(self):
        imprimir_titulo("ACTUALIZAR ESTUDIANTE")
        id_estudiante = _pedir_id("Id del estudiante")
        if id_estudiante is None:
            return pausa()

        estudiante = ctrl_estudiante.obtener_por_id(id_estudiante)
        if not estudiante:
            imprimir_error(f"No existe un estudiante con id {id_estudiante}")
            return pausa()

        print("Deje en blanco el campo que no quiera cambiar.\n")
        cambios = {}
        for campo in CAMPOS_ESTUDIANTE:
            actual = getattr(estudiante, campo)
            nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
            if nuevo:
                cambios[campo] = nuevo

        exito, mensaje = ctrl_estudiante.actualizar_estudiante(id_estudiante, cambios)
        imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
        pausa()

    def eliminar_estudiante(self):
        imprimir_titulo("ELIMINAR ESTUDIANTE")
        id_estudiante = _pedir_id("Id del estudiante")
        if id_estudiante is None:
            return pausa()

        estudiante = ctrl_estudiante.obtener_por_id(id_estudiante)
        if not estudiante:
            imprimir_error(f"No existe un estudiante con id {id_estudiante}")
            return pausa()

        if confirmar(f"¿Confirma eliminar a {estudiante}?"):
            exito, mensaje = ctrl_estudiante.eliminar_estudiante(id_estudiante)
            imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
        else:
            imprimir_info("Operación cancelada")
        pausa()

    def menu_estudiantes(self):
        opciones = {
            "1": ("Crear estudiante", self.crear_estudiante),
            "2": ("Listar estudiantes", self.listar_estudiantes),
            "3": ("Buscar estudiante", self.buscar_estudiantes),
            "4": ("Actualizar estudiante", self.actualizar_estudiante),
            "5": ("Eliminar estudiante", self.eliminar_estudiante),
            "0": ("Volver al menú principal", None),
        }
        while True:
            imprimir_titulo("GESTIÓN DE ESTUDIANTES")
            for tecla, (texto, _f) in opciones.items():
                print(f"  {tecla}. {texto}")
            tecla = input("\nSeleccione una opción: ").strip()
            if tecla == "0":
                return
            if tecla not in opciones:
                imprimir_error("Opción no válida")
                pausa()
                continue
            opciones[tecla][1]()

    # =========================================================
    # DOCENTES
    # =========================================================

    def _tabla_docentes(self, docentes):
        print(f"{'ID':<5}{'CÉDULA':<14}{'NOMBRE':<28}{'TÍTULO':<15}{'ESPECIALIDAD':<20}")
        print("-" * 90)
        for d in docentes:
            print(f"{d.id:<5}{d.cedula:<14}{d.nombre_completo():<28}{d.titulo:<15}{d.especialidad:<20}")
        print("-" * 90)
        imprimir_info(f"Total: {len(docentes)} docente(s)")

    def crear_docente(self):
        imprimir_titulo("CREAR DOCENTE")
        datos = {campo: input(f"{campo.capitalize()}: ") for campo in CAMPOS_DOCENTE}
        exito, mensaje = ctrl_docente.crear_docente(datos)
        imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
        pausa()

    def listar_docentes(self):
        imprimir_titulo("LISTA DE DOCENTES")
        docentes = ctrl_docente.obtener_todos()
        if not docentes:
            imprimir_info("Todavía no hay docentes registrados.")
        else:
            self._tabla_docentes(docentes)
        pausa()

    def buscar_docentes(self):
        imprimir_titulo("BUSCAR DOCENTE")
        termino = input("Cédula, nombre, apellido, email o especialidad: ")
        encontrados = ctrl_docente.buscar_docentes(termino)
        if not encontrados:
            imprimir_info(f"Ningún docente coincide con '{termino}'.")
        else:
            self._tabla_docentes(encontrados)
        pausa()

    def actualizar_docente(self):
        imprimir_titulo("ACTUALIZAR DOCENTE")
        id_docente = _pedir_id("Id del docente")
        if id_docente is None:
            return pausa()

        docente = ctrl_docente.obtener_por_id(id_docente)
        if not docente:
            imprimir_error(f"No existe un docente con id {id_docente}")
            return pausa()

        print("Deje en blanco el campo que no quiera cambiar.\n")
        cambios = {}
        for campo in CAMPOS_DOCENTE:
            actual = getattr(docente, campo)
            nuevo = input(f"{campo.capitalize()} [{actual}]: ").strip()
            if nuevo:
                cambios[campo] = nuevo

        exito, mensaje = ctrl_docente.actualizar_docente(id_docente, cambios)
        imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
        pausa()

    def eliminar_docente(self):
        imprimir_titulo("ELIMINAR DOCENTE")
        id_docente = _pedir_id("Id del docente")
        if id_docente is None:
            return pausa()

        docente = ctrl_docente.obtener_por_id(id_docente)
        if not docente:
            imprimir_error(f"No existe un docente con id {id_docente}")
            return pausa()

        if confirmar(f"¿Confirma eliminar a {docente}?"):
            exito, mensaje = ctrl_docente.eliminar_docente(id_docente)
            imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
        else:
            imprimir_info("Operación cancelada")
        pausa()

    def menu_docentes(self):
        opciones = {
            "1": ("Crear docente", self.crear_docente),
            "2": ("Listar docentes", self.listar_docentes),
            "3": ("Buscar docente", self.buscar_docentes),
            "4": ("Actualizar docente", self.actualizar_docente),
            "5": ("Eliminar docente", self.eliminar_docente),
            "0": ("Volver al menú principal", None),
        }
        while True:
            imprimir_titulo("GESTIÓN DE DOCENTES")
            for tecla, (texto, _f) in opciones.items():
                print(f"  {tecla}. {texto}")
            tecla = input("\nSeleccione una opción: ").strip()
            if tecla == "0":
                return
            if tecla not in opciones:
                imprimir_error("Opción no válida")
                pausa()
                continue
            opciones[tecla][1]()

    # =========================================================
    # ASIGNATURAS
    # =========================================================

    def _tabla_asignaturas(self, asignaturas):
        print(f"{'ID':<5}{'CÓDIGO':<15}{'NOMBRE':<28}{'CRÉDITOS':<10}{'DOCENTE_ID':<10}")
        print("-" * 70)
        for a in asignaturas:
            print(f"{a.id:<5}{a.codigo:<15}{a.nombre:<28}{a.creditos:<10}{a.docente_id or '-':<10}")
        print("-" * 70)
        imprimir_info(f"Total: {len(asignaturas)} asignatura(s)")

    def crear_asignatura(self):
        imprimir_titulo("CREAR ASIGNATURA")
        datos = {
            "codigo": input("Código: "),
            "nombre": input("Nombre: "),
            "creditos": input("Créditos (1-10): "),
            "docente_id": input("Id del docente (opcional, Enter para omitir): ").strip() or None,
        }
        exito, mensaje = ctrl_asignatura.crear_asignatura(datos)
        imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
        pausa()

    def listar_asignaturas(self):
        imprimir_titulo("LISTA DE ASIGNATURAS")
        asignaturas = ctrl_asignatura.obtener_todos()
        if not asignaturas:
            imprimir_info("Todavía no hay asignaturas registradas.")
        else:
            self._tabla_asignaturas(asignaturas)
        pausa()

    def buscar_asignaturas(self):
        imprimir_titulo("BUSCAR ASIGNATURA")
        termino = input("Código o nombre: ")
        encontradas = ctrl_asignatura.buscar_asignaturas(termino)
        if not encontradas:
            imprimir_info(f"Ninguna asignatura coincide con '{termino}'.")
        else:
            self._tabla_asignaturas(encontradas)
        pausa()

    def eliminar_asignatura(self):
        imprimir_titulo("ELIMINAR ASIGNATURA")
        id_asignatura = _pedir_id("Id de la asignatura")
        if id_asignatura is None:
            return pausa()

        if confirmar("¿Confirma la eliminación?"):
            exito, mensaje = ctrl_asignatura.eliminar_asignatura(id_asignatura)
            imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
        else:
            imprimir_info("Operación cancelada")
        pausa()

    def menu_asignaturas(self):
        opciones = {
            "1": ("Crear asignatura", self.crear_asignatura),
            "2": ("Listar asignaturas", self.listar_asignaturas),
            "3": ("Buscar asignatura", self.buscar_asignaturas),
            "4": ("Eliminar asignatura", self.eliminar_asignatura),
            "0": ("Volver al menú principal", None),
        }
        while True:
            imprimir_titulo("GESTIÓN DE ASIGNATURAS")
            for tecla, (texto, _f) in opciones.items():
                print(f"  {tecla}. {texto}")
            tecla = input("\nSeleccione una opción: ").strip()
            if tecla == "0":
                return
            if tecla not in opciones:
                imprimir_error("Opción no válida")
                pausa()
                continue
            opciones[tecla][1]()

    # =========================================================
    # CURSOS
    # =========================================================

    def _tabla_cursos(self, cursos):
        print(f"{'ID':<5}{'NOMBRE':<30}{'PARALELO':<10}{'ASIG_ID':<9}{'DOC_ID':<8}{'MATRIC.':<8}")
        print("-" * 75)
        for c in cursos:
            print(f"{c.id:<5}{c.nombre:<30}{c.paralelo:<10}{c.asignatura_id:<9}"
                  f"{c.docente_id:<8}{c.total_matriculados():<8}")
        print("-" * 75)
        imprimir_info(f"Total: {len(cursos)} curso(s)")

    def crear_curso(self):
        imprimir_titulo("CREAR CURSO")
        datos = {
            "nombre": input("Nombre: "),
            "paralelo": input("Paralelo (ej. A): "),
            "asignatura_id": input("Id de la asignatura: "),
            "docente_id": input("Id del docente: "),
        }
        exito, mensaje = ctrl_curso.crear_curso(datos)
        imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
        pausa()

    def listar_cursos(self):
        imprimir_titulo("LISTA DE CURSOS")
        cursos = ctrl_curso.obtener_todos()
        if not cursos:
            imprimir_info("Todavía no hay cursos registrados.")
        else:
            self._tabla_cursos(cursos)
        pausa()

    def matricular_estudiante(self):
        imprimir_titulo("MATRICULAR ESTUDIANTE EN CURSO")
        id_curso = _pedir_id("Id del curso")
        if id_curso is None:
            return pausa()
        id_estudiante = _pedir_id("Id del estudiante")
        if id_estudiante is None:
            return pausa()

        exito, mensaje = ctrl_curso.matricular_estudiante(id_curso, id_estudiante)
        imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
        pausa()

    def retirar_estudiante(self):
        imprimir_titulo("RETIRAR ESTUDIANTE DE CURSO")
        id_curso = _pedir_id("Id del curso")
        if id_curso is None:
            return pausa()
        id_estudiante = _pedir_id("Id del estudiante")
        if id_estudiante is None:
            return pausa()

        exito, mensaje = ctrl_curso.retirar_estudiante(id_curso, id_estudiante)
        imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
        pausa()

    def companeros_en_comun(self):
        imprimir_titulo("COMPAÑEROS EN COMÚN ENTRE DOS CURSOS")
        id_curso_a = _pedir_id("Id del primer curso")
        if id_curso_a is None:
            return pausa()
        id_curso_b = _pedir_id("Id del segundo curso")
        if id_curso_b is None:
            return pausa()

        exito, resultado = ctrl_curso.companeros_en_comun(id_curso_a, id_curso_b)
        if not exito:
            imprimir_error(resultado)
        elif not resultado:
            imprimir_info("Estos cursos no comparten ningún estudiante.")
        else:
            imprimir_exito(f"Ids de estudiantes en común: {sorted(resultado)}")
        pausa()

    def eliminar_curso(self):
        imprimir_titulo("ELIMINAR CURSO")
        id_curso = _pedir_id("Id del curso")
        if id_curso is None:
            return pausa()

        if confirmar("¿Confirma la eliminación?"):
            exito, mensaje = ctrl_curso.eliminar_curso(id_curso)
            imprimir_exito(mensaje) if exito else imprimir_error(mensaje)
        else:
            imprimir_info("Operación cancelada")
        pausa()

    def menu_cursos(self):
        opciones = {
            "1": ("Crear curso", self.crear_curso),
            "2": ("Listar cursos", self.listar_cursos),
            "3": ("Matricular estudiante", self.matricular_estudiante),
            "4": ("Retirar estudiante", self.retirar_estudiante),
            "5": ("Compañeros en común (2 cursos)", self.companeros_en_comun),
            "6": ("Eliminar curso", self.eliminar_curso),
            "0": ("Volver al menú principal", None),
        }
        while True:
            imprimir_titulo("GESTIÓN DE CURSOS")
            for tecla, (texto, _f) in opciones.items():
                print(f"  {tecla}. {texto}")
            tecla = input("\nSeleccione una opción: ").strip()
            if tecla == "0":
                return
            if tecla not in opciones:
                imprimir_error("Opción no válida")
                pausa()
                continue
            opciones[tecla][1]()
