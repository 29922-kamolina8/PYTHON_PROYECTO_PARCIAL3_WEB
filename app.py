from flask import Flask, render_template, abort
import sys
import os
import importlib.util
from collections import defaultdict


app = Flask(__name__)

# --- CONFIGURACIÓN NUEVA (LISTA) ---
# Necesaria para que funcione el menú desplegable y el orden de los temas
TEMAS = [
    {
        "slug": "infraestructura-backend",
        "titulo": "1. Infraestructura Backend",
        "archivo": "teoria/teoria_infraestructura.html",
        "subtemas": [
            {"id": "que-es-backend", "titulo": "¿Qué es el Backend?"},
            {"id": "arquitectura-cliente-servidor", "titulo": "Arquitectura Cliente–Servidor"},
            {"id": "flujo-peticion", "titulo": "Flujo de una Petición Web"},
            {"id": "estructura-proyecto", "titulo": "Estructura de un Proyecto Profesional"},
            {"id": "sistema-rutas", "titulo": "El Sistema de Rutas"},
            {"id": "backend-vs-herramientas", "titulo": "Backend: Concepto vs Herramienta"},
            {"id": "errores-backend", "titulo": "Errores Comunes en el Desarrollo Backend"},
            {"id": "cuestionario", "titulo": "Cuestionario de Aprendizaje"},
            {"id": "juego", "titulo": "Mini-juego: Arma la Petición Backend"},
        ]
    },
    {
        "slug": "historia-python",
        "titulo": "2. Historia de Python",
        "archivo": "teoria/teoria_historia.html",
        "subtemas": [
            {"id": "que-es-python", "titulo": "¿Qué es Python?"},
            {"id": "HistoriaPython", "titulo": "Historia de Python"},
            {"id": "arquitectura-web-python", "titulo": "Arquitectura Web de Python"},
            {"id": "html-motores-plantillas", "titulo": "HTML y Motores de Plantillas"},
            {"id": "gigantes-python", "titulo": "Gigantes construidos con Python"},
            {"id": "ecosistema-frameworks", "titulo": "Ecosistema de Frameworks en Python"},
            {"id": "ventajas-desventajas-python", "titulo": "Ventajas y Desventajas de Python"},
            {"id": "cuestionario-historia-python", "titulo": "Cuestionario de Aprendizaje"},
            {"id": "Mini-juego-evolucion-python", "titulo": "Mini-juego: Reconstruye la evolución de Python"},
        ]
    },
    {
        "slug": "html-python-web",
        "titulo": "3. HTML y Python (Web)",
        "archivo": "teoria/teoria_htmlpyhon.html",
        "subtemas": [
            {"id": "que-es-html", "titulo": "Páginas estáticas"},
            {"id": "flujo-web", "titulo": "Flujo Web"},
            {"id": "estructura-basica", "titulo": "Sintaxis Jinja2"},
            {"id": "integracion-python", "titulo": "Integración Python"},
            {"id": "timeline-jinja", "titulo": "Evolución Web"},
            {"id": "http-basico", "titulo": "HTTP básico"},
            {"id": "jinja-filtros", "titulo": "Filtros Jinja2"},
            {"id": "ejemplo-tabla", "titulo": "Tabla dinámica"},
            {"id": "cuestionario-web", "titulo": "Cuestionario"},
            {"id": "mini-juego-web", "titulo": "Mini-juego"}
        ]
    },
    {
        "slug": "sintaxis-comentarios",
        "titulo": "4. Sintaxis y Comentarios",
        "archivo": "teoria/teoria_sintaxisComentarios.html",
        "subtemas": [
            {"id": "indentacion", "titulo": "La Indentación"},
            {"id": "bloques", "titulo": "Bloques y dos puntos"},
            {"id": "errores-comunes", "titulo": "Errores comunes"},
            {"id": "comentarios-python", "titulo": "Comentarios en Python"},
            {"id": "comentarios-html", "titulo": "Comentarios en HTML"},
            {"id": "comparacion", "titulo": "Comparación rápida"},
            {"id": "quiz-sintaxis", "titulo": "Cuestionario"},
            {"id": "mini-juego-sintaxis", "titulo": "Mini-juego"}
        ]
    },
    {
        "slug": "variables-constantes",
        "titulo": "5. Variables y Constantes",
        "archivo": "teoria/teoria_variablesConstantes.html",
        "subtemas": [
            {"id": "variables", "titulo": "1. Variables"},
            {"id": "declaracion", "titulo": "1.1 Declaración"},
            {"id": "nombrado", "titulo": "1.2 Reglas de nombrado"},
            {"id": "constantes", "titulo": "2. Constantes"},
            {"id": "uso-constantes", "titulo": "2.1 Uso recomendado"},
            {"id": "playground", "titulo": "Práctica interactiva"},
            {"id": "video", "titulo": "Video"},
            {"id": "cuestionario", "titulo": "Cuestionario"},
        ]
    },
    {
        "slug": "tipos-de-datos",
        "titulo": "6. Tipos de Datos",
        "archivo": "teoria/teoria_tiposDatos.html",
        "subtemas": [
            {"id": "intro", "titulo": "¿Qué es un tipo de dato?"},
            {"id": "int", "titulo": "Enteros"},
            {"id": "float", "titulo": "Decimales"},
            {"id": "bool", "titulo": "Booleano"},
            {"id": "str", "titulo": "Texto"},
            {"id": "none", "titulo": "None"},
            {"id": "video", "titulo": "Video"},
            {"id": "cuestionario", "titulo": "Cuestionario"},
        ]
    },
    {
        "slug": "operadores",
        "titulo": "7. Operadores",
        "archivo": "teoria/teoria_operadores.html",
        "subtemas": [
            {"id": "aritmeticos", "titulo": "1. Operadores Aritméticos"},
            {"id": "comparacion", "titulo": "2. Operadores de Comparación"},
            {"id": "logicos", "titulo": "3. Operadores Lógicos"},
        ]
    },
    {
        "slug": "estructuras-de-control",
        "titulo": "8. Estructuras de Control",
        "archivo": "teoria/teoria_estructuras_de_control.html",
        "subtemas": [
            {"id": "condicionales", "titulo": "Condicionales (if / elif / else)"},
            {"id": "bucles", "titulo": "Bucle For"},
            {"id": "control-flujo", "titulo": "Bucle While"},
        ]
    },
    {
        "slug": "funciones",
        "titulo": "9. Funciones",
        "archivo": "teoria/teoria_funciones.html",
        "subtemas": [
            {"id": "que-son-funciones", "titulo": "¿Qué es una función?"},
            {"id": "parametros", "titulo": "Componentes Clave"},
            {"id": "retorno", "titulo": "Scope (Alcance)"},
        ]
    },
    {
        "slug": "manejo-formularios",
        "titulo": "10. Manejo de Formularios",
        "archivo": "teoria/teoria_manejoFormularios.html",
        "subtemas": [
            {"id": "formularios-html", "titulo": "GET vs POST"},
            {"id": "captura-datos", "titulo": "Recibir datos con Flask"},
            {"id": "validacion", "titulo": "Validación"},
        ]
    },
    {
        "slug": "arreglos",
        "titulo": "11. Arreglos",
        "archivo": "teoria/teoria_arreglos.html",
        "subtemas": [
            {"id": "listas", "titulo": "1. Listas (Lists)"},
            {"id": "tuplas", "titulo": "2. Tuplas (Tuples)"},
            {"id": "diccionarios", "titulo": "3. Diccionarios (Dicts)"},
        ]
    },
    {
        "slug": "poo",
        "titulo": "12. Programación Orientada a Objetos",
        "archivo": "teoria/teoria_poo.html",
        "subtemas": [
            {"id": "clases", "titulo": "Clase vs Objeto"},
            {"id": "herencia", "titulo": "Sintaxis en Python"},
            {"id": "polimorfismo", "titulo": "¡Felicidades!"},
        ]
    },
]

# =========================
# EJERCICIOS (aquí tú pones los 20)
# =========================
EJERCICIOS = [
    # --- FORMULARIOS GET Y POST ---
    {
        "id": 1,
        "slug": "ejercicio1",
        "tema": "Procesamiento de formularios",
        "titulo": "Formulario request.form",
        "descripcion": "Desarrolla un formulario usando método POST.",
        "practica": ["Formularios", "GET/POST", "Validación"],
        "detalle_largo": ""
    },
    {
        "id": 2,
        "slug": "ejercicio2",
        "tema": "Procesamiento de formularios",
        "titulo": "Formulario request.files",
        "descripcion": "Formulario POST con subida de archivos (files).",
        "practica": ["Formularios", "POST", "Archivos"],
        "detalle_largo": ""
    },

    # --- ESTRUCTURAS DE CONTROL ---
    {
        "id": 3,
        "slug": "ejercicio3",
        "tema": "Estructuras de Control",
        "titulo": "Factorial",
        "descripcion": "Cálculo de factorial usando estructuras de control.",
    },
    {
        "id": 4,
        "slug": "ejercicio4",
        "tema": "Estructuras de Control",
        "titulo": "Triángulo de Pascal",
        "descripcion": "Generación del triángulo de Pascal.",
    },
    {
        "id": 5,
        "slug": "ejercicio5",
        "tema": "Estructuras de Control",
        "titulo": "Es primo",
        "descripcion": "Determinar si un número es primo.",
    },
    {
        "id": 6,
        "slug": "ejercicio6",
        "tema": "Estructuras de Control",
        "titulo": "Cédula",
        "descripcion": "Validación de cédula (según reglas definidas en el ejercicio).",
    },
    # --- ARREGLOS ---
    {
        "id": 7,
        "slug": "ejercicio7",
        "tema": "Arreglos",
        "titulo": "Ejemplo 01",
        "descripcion": "Ejercicio de práctica de estructuras de control (Ejemplo 01).",
    },
    {
        "id": 8,
        "slug": "ejercicio8",
        "tema": "Arreglos",
        "titulo": "Ejemplo 02",
        "descripcion": "Ejercicio de práctica de estructuras de control (Ejemplo 02).",
    },
    {
        "id": 9,
        "slug": "ejercicio9",
        "tema": "Arreglos",
        "titulo": "Arreglo",
        "descripcion": "Trabajo con arreglos/listas.",
    },
    {
        "id": 10,
        "slug": "ejercicio10",
        "tema": "Arreglos",
        "titulo": "Matriz",
        "descripcion": "Manejo de matrices (listas anidadas).",
    },
    {
        "id": 11,
        "slug": "ejercicio11",
        "tema": "Arreglos",
        "titulo": "Cubo",
        "descripcion": "Trabajo con arreglos 3D (cubo).",
    },
    {
        "id": 12,
        "slug": "ejercicio12",
        "tema": "Arreglos",
        "titulo": "Tablas dinámicas",
        "descripcion": "Implementación de tablas dinámicas (parte específica).",
    },

    # --- POO ---
    {
        "id": 13,
        "slug": "ejercicio13",
        "tema": "POO",
        "titulo": "Clases",
        "descripcion": "Ejercicio de clases y objetos.",
    },
    {
        "id": 14,
        "slug": "ejercicio14",
        "tema": "POO",
        "titulo": "Herencia",
        "descripcion": "Ejercicio de herencia en POO.",
    },
    {
        "id": 15,
        "slug": "ejercicio15",
        "tema": "POO",
        "titulo": "Abstracta",
        "descripcion": "Clases abstractas (concepto y aplicación).",
    },
    {
        "id": 16,
        "slug": "ejercicio16",
        "tema": "POO",
        "titulo": "Interfaces",
        "descripcion": "Simulación/uso de interfaces (según enfoque del curso).",
    },
    {
        "id": 17,
        "slug": "ejercicio17",
        "tema": "POO",
        "titulo": "Polimorfismo",
        "descripcion": "Ejercicio de polimorfismo.",
    },
]

def obtener_ejercicios_por_tema():
    agrupados = defaultdict(list)
    for ej in EJERCICIOS:
        agrupados[ej["tema"]].append(ej)
    return dict(agrupados)


@app.context_processor
def inject_global_data():
    return {
        "ejercicios_por_tema": obtener_ejercicios_por_tema()
    }

@app.context_processor
def inject_temas():
    # Inyectamos la lista para el menú de base.html
    return dict(lista_temas=TEMAS)

# =========================
# RUTAS BASE
# =========================
@app.route("/")
def home():
    return render_template("home.html")

@app.route("/teoria")
def teoria_general():
    return render_template("teoria.html")

@app.route("/teoria/<slug>")
def teoria_tema(slug):
    tema_actual = next((t for t in TEMAS if t["slug"] == slug), None)
    if not tema_actual:
        return render_template("home.html"), 404
    return render_template(tema_actual["archivo"], tema=tema_actual)

# =========================
# RUTAS EJERCICIOS
# =========================
@app.route("/ejercicios")
def ejercicios():
    return render_template("ejercicios.html", ejercicios=EJERCICIOS)

@app.route("/ejercicios/<slug>")
def ver_ejercicio(slug):
    ejercicio = next((e for e in EJERCICIOS if e["slug"] == slug), None)
    if not ejercicio:
        abort(404)

    template_path = f"ejercicios/{slug}/detalle.html"
    if not os.path.exists(os.path.join("templates", template_path)):
        abort(404)
    idx = next((i for i, e in enumerate(EJERCICIOS) if e["slug"] == slug), None)
    anterior = EJERCICIOS[idx - 1] if idx is not None and idx > 0 else None
    siguiente = EJERCICIOS[idx + 1] if idx is not None and idx < len(EJERCICIOS) - 1 else None


    return render_template(template_path, ejercicio=ejercicio, contenido=None,
                        anterior=anterior, siguiente=siguiente)

def cargar_modulo_ejercicio(slug):
    """
    Carga dinámicamente templates/ejercicios/<slug>/ejercicio.py
    y devuelve el módulo. Permite múltiples archivos .py dentro de esa carpeta.
    """
    carpeta = os.path.join("templates", "ejercicios", slug)
    archivo = os.path.join(carpeta, "ejercicio.py")

    if not os.path.exists(archivo):
        return None

    # ✅ Para que el ejercicio pueda hacer: import clases / import utils / etc.
    if carpeta not in sys.path:
        sys.path.insert(0, carpeta)

    spec = importlib.util.spec_from_file_location(f"{slug}_mod", archivo)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

@app.route("/ejercicios/<slug>/ejecutar", methods=["GET", "POST"])
def ejecutar_ejercicio(slug):
    ejercicio = next((e for e in EJERCICIOS if e["slug"] == slug), None)
    if not ejercicio:
        abort(404)

    template_path = f"ejercicios/{slug}/detalle.html"
    if not os.path.exists(os.path.join("templates", template_path)):
        abort(404)

    mod = cargar_modulo_ejercicio(slug)
    if not mod or not hasattr(mod, "ejecutar"):
        return "No existe ejercicio.py o falta la función ejecutar()", 404

    contenido = mod.ejecutar()
    idx = next((i for i, e in enumerate(EJERCICIOS) if e["slug"] == slug), None)
    anterior = EJERCICIOS[idx - 1] if idx is not None and idx > 0 else None
    siguiente = EJERCICIOS[idx + 1] if idx is not None and idx < len(EJERCICIOS) - 1 else None


    return render_template(template_path, ejercicio=ejercicio, contenido=contenido,
                       anterior=anterior, siguiente=siguiente)

if __name__ == "__main__":
    app.run(debug=True)
