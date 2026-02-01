from flask import Flask, render_template, abort

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
            {"id": "que-es-html", "titulo": "El desafío de las páginas estáticas"},
            {"id": "estructura-basica", "titulo": "Sintaxis Básica de Jinja2"},
            {"id": "integracion-python", "titulo": "Ejemplo Completo"},
        ]
    },
    {
        "slug": "sintaxis-comentarios",
        "titulo": "4. Sintaxis y Comentarios",
        "archivo": "teoria/teoria_sintaxisComentarios.html",
        "subtemas": [
            {"id": "indentacion", "titulo": "La Indentación"},
            {"id": "comentarios", "titulo": "Comentarios"},
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
            {"id": "numeros", "titulo": "Tipos Primitivos"},
            {"id": "cadenas", "titulo": "Verificar el tipo"},
            {"id": "booleanos", "titulo": "Booleanos"},
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

@app.context_processor
def inject_temas():
    # Inyectamos la lista para el menú de base.html
    return dict(lista_temas=TEMAS)

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

if __name__ == "__main__":
    app.run(debug=True)