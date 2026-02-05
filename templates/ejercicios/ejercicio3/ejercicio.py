from flask import request, render_template_string

def calcular_factorial(n: int) -> int:
    total = 1
    for i in range(1, n + 1):
        total *= i
    return total

HTML = """
<div class="wrap">

  <h3 class="text-center mb-4">Cálculo de Factorial</h3>

  {% if error %}
    <div class="alert alert-danger">
      {{ error }}
    </div>
  {% endif %}

  <div class="card p-4 shadow-sm border-0">
    <form method="POST">
      <div class="mb-3">
        <label class="form-label fw-bold" for="ingresoNumero">Ingrese un número:</label>
        <input type="number" class="form-control"
               name="ingresoNumero" id="ingresoNumero"
               value="{{ form_data.ingresoNumero }}"
               min="0" max="10" step="1" required>
        <div class="form-text">Rango permitido: 0 a 10.</div>
      </div>

      <button type="submit" class="btn btn-primary w-100">
        Calcular
      </button>
    </form>
  </div>

  {% if mostrar_resultado %}
    <div class="card p-4 mt-3 shadow-sm border-0 text-center">
      <div class="alert alert-success mb-0">
        El factorial de <strong>{{ numero }}</strong> es:
        <br>
        <strong>{{ resultado }}</strong>
      </div>
    </div>
  {% endif %}

</div>
"""

def ejecutar():
    error = None
    mostrar_resultado = False
    numero = None
    resultado = None
    form_data = {"ingresoNumero": 0}

    if request.method == "POST":
        try:
            raw = request.form.get("ingresoNumero", "0").strip()
            n = int(raw)

            form_data["ingresoNumero"] = n

            if n < 0:
                error = "El número no puede ser negativo."
            elif n > 10:
                error = "El número debe estar entre 0 y 10."
            else:
                numero = n
                resultado = calcular_factorial(n)
                mostrar_resultado = True

        except Exception:
            error = "Error al procesar el número ingresado. Asegúrate de escribir un entero válido."

    return render_template_string(
        HTML,
        error=error,
        mostrar_resultado=mostrar_resultado,
        numero=numero,
        resultado=resultado,
        form_data=form_data
    )
