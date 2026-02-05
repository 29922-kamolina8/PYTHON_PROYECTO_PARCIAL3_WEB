import os
import importlib.util
from flask import request, render_template_string

# =====================================================
# Cargar pascal_triangle.py por ruta (seguro con importlib)
# =====================================================
def cargar_pascal():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    ruta_pascal = os.path.join(base_dir, "pascal_triangle.py")

    if not os.path.exists(ruta_pascal):
        raise FileNotFoundError(
            f"No se encontró pascal_triangle.py en: {ruta_pascal}"
        )

    spec = importlib.util.spec_from_file_location(
        "pascal_triangle_ejercicio", ruta_pascal
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_pascal = cargar_pascal()
generar_triangulo_pascal = _pascal.generar_triangulo_pascal
formatear_triangulo_pascal = _pascal.formatear_triangulo_pascal


# =====================================================
# HTML del ejercicio (se inyecta en detalle.html)
# =====================================================
HTML = """
<div class="wrap">

  <h3 class="text-center mb-4">Triángulo de Pascal</h3>

  {% if error %}
    <div class="alert alert-danger">
      {{ error }}
    </div>
  {% endif %}

  <div class="card p-4 shadow-sm border-0">
    <form method="POST">

      <div class="mb-3">
        <label for="numfilas" class="form-label fw-bold">
          Ingrese un número entre 1 y 10:
        </label>
        <input type="number"
               id="numfilas"
               name="numfilas"
               class="form-control"
               min="1"
               max="10"
               required
               value="{{ form_data.numfilas }}">
      </div>

      <button type="submit" class="btn btn-primary w-100">
        Generar Triángulo de Pascal
      </button>
    </form>
  </div>

  {% if triangulo_html %}
    <div class="card p-4 mt-3 shadow-sm border-0 text-center">
      {{ triangulo_html | safe }}
    </div>
  {% endif %}

</div>
"""

# =====================================================
# Función estándar llamada por ejecutar_ejercicio(slug)
# =====================================================
def ejecutar():
    error = None
    triangulo_html = None
    form_data = {"numfilas": ""}

    if request.method == "POST":
        try:
            filas = int(request.form.get("numfilas", "").strip())
            form_data["numfilas"] = filas

            if filas < 1 or filas > 10:
                error = "El número de filas debe estar entre 1 y 10."
            else:
                pascal = generar_triangulo_pascal(filas)
                triangulo_html = formatear_triangulo_pascal(pascal)

        except Exception:
            error = "Error al procesar el número ingresado."

    return render_template_string(
        HTML,
        error=error,
        triangulo_html=triangulo_html,
        form_data=form_data
    )
