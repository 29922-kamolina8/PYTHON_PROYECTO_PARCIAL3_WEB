from flask import request, render_template_string

# ✅ Cada grupo pega aquí su HTML (puede ser grande)
HTML = """
<h4 class="mb-3 text-center">Ejercicio (Formulario / Interacción)</h4>

<form method="post">
  <label class="form-label">Dato 1:</label>
  <input class="form-control mb-3" type="text" name="dato1" required>

  <label class="form-label">Dato 2:</label>
  <input class="form-control mb-4" type="number" name="dato2" required>

  <button class="btn btn-success w-100" type="submit">Enviar</button>
</form>

{% if mostrar %}
<hr>
<div class="alert alert-info mt-3">
  <strong>Resultado:</strong> {{ resultado }}
</div>
{% endif %}
"""

def ejecutar():
    """
    ✅ FUNCIÓN ESTÁNDAR
    - GET: muestra el formulario
    - POST: procesa y muestra resultados
    """

    if request.method == "POST":
        # ✅ Cada grupo implementa aquí lo que hace el ejercicio
        dato1 = request.form.get("dato1")
        dato2 = request.form.get("dato2")

        # Ejemplo (cambiar por la lógica real del ejercicio)
        resultado = f"Recibí: {dato1} y {dato2}"

        return render_template_string(HTML, mostrar=True, resultado=resultado)

    return render_template_string(HTML, mostrar=False)
