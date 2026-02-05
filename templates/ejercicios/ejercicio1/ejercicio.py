import os
import sys
from flask import request, render_template_string

# ✅ Asegura que Python pueda importar geometry.py aunque el módulo se cargue con importlib
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
if BASE_DIR not in sys.path:
    sys.path.insert(0, BASE_DIR)

from geometry import process_figure  # ✅ ahora sí, sin backend_formulario

HTML = """
<div class="wrap">
  <h3 class="text-center mb-4">Formulario de Figuras</h3>

  {% if errors %}
    <div class="alert alert-danger">
      <ul class="mb-0">
        {% for e in errors %}
          <li>{{ e }}</li>
        {% endfor %}
      </ul>
    </div>
  {% endif %}

  <form method="POST" class="card p-4 shadow-sm border-0">

    <label class="fw-bold">Figura:</label>
    <select name="figura" class="form-select mb-3">
      <option value="">Seleccione figura</option>
      <option value="cuadrado" {% if form_data.figura=='cuadrado' %}selected{% endif %}>Cuadrado</option>
      <option value="rectangulo" {% if form_data.figura=='rectangulo' %}selected{% endif %}>Rectángulo</option>
      <option value="triangulo" {% if form_data.figura=='triangulo' %}selected{% endif %}>Triángulo</option>
    </select>

    <label class="fw-bold">Lados:</label>
    <input class="form-control mb-2" name="l1" placeholder="l1" value="{{ form_data.l1 }}">
    <input class="form-control mb-2" name="l2" placeholder="l2" value="{{ form_data.l2 }}">
    <input class="form-control mb-3" name="l3" placeholder="l3" value="{{ form_data.l3 }}">

    <button class="btn btn-primary w-100">Calcular</button>
  </form>

  {% if result %}
    <div class="card p-4 mt-3 shadow-sm border-0">
      <p class="mb-2"><b>Figura:</b> {{ result.figura }}</p>
      <p class="mb-2"><b>Lados:</b> {{ result.lados }}</p>
      <p class="mb-2"><b>Área:</b> {{ result.area }}</p>
      <p class="mb-2"><b>Perímetro:</b> {{ result.perimetro }}</p>

      {% if result.tipo_triangulo %}
        <p class="mb-0"><b>Tipo triángulo:</b> {{ result.tipo_triangulo }}</p>
      {% endif %}
    </div>
  {% endif %}
</div>
"""

def ejecutar():
    errors = []
    result = None
    form_data = {"figura": "", "l1": "", "l2": "", "l3": ""}

    if request.method == "POST":
        figura = request.form.get("figura", "").strip()
        l1 = request.form.get("l1", "").strip()
        l2 = request.form.get("l2", "").strip()
        l3 = request.form.get("l3", "").strip()

        form_data["figura"] = figura
        form_data["l1"] = l1
        form_data["l2"] = l2
        form_data["l3"] = l3

        # ✅ tu backend (geometry.py) devuelve (result, errors)
        result, errors = process_figure(figura, l1, l2, l3)

    return render_template_string(
        HTML,
        errors=errors,
        result=result,
        form_data=form_data
    )
