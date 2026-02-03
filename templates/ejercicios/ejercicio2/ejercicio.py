import os
import random
import string
from flask import request, render_template_string

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join("static", "images")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def get_name_file(nombre_original, tamanio):
    ext = nombre_original.split('.')[-1]
    letras = string.ascii_letters
    nombre = ''.join(random.choice(letras) for _ in range(tamanio))
    return f"{nombre}.{ext}"

HTML = """
<div class="wrap">
<h3 class="text-center mb-4">Formulario de Registro Vehicular</h3>

<form method="post" enctype="multipart/form-data">

<label>Placa:</label>
<input type="text" name="placa" class="form-control mb-3" required>

<label>Marca:</label>
<input type="text" name="marca" class="form-control mb-3" required>

<label>Combustible:</label>
<select name="combustible" class="form-select mb-3">
  <option>Gasolina</option>
  <option>Diésel</option>
  <option>Eléctrico</option>
</select>

<label>Accesorios:</label>
<div class="mb-3">
  <div><input type="radio" name="accesorio" value="Radio" required> Radio</div>
  <div><input type="radio" name="accesorio" value="Aros"> Aros</div>
  <div><input type="radio" name="accesorio" value="Radio y Aros"> Radio y Aros</div>
  <div><input type="radio" name="accesorio" value="Ninguno"> Ninguno</div>
</div>

<label>Comentarios:</label>
<textarea name="comentarios" class="form-control mb-3"></textarea>

<label>Foto:</label>
<input type="file" name="foto" class="form-control mb-4">

<button type="submit" class="btn btn-success w-100">
  Enviar
</button>
</form>

{% if mostrar %}
<hr>
<div class="alert alert-info mt-4">
  <strong>Placa:</strong> {{ placa }}<br>
  <strong>Marca:</strong> {{ marca }}<br>
  <strong>Combustible:</strong> {{ combustible }}<br>
  <strong>Accesorios:</strong> {{ accesorios }}<br>
  <strong>Comentarios:</strong> {{ comentarios }}<br>

  {% if foto %}
    <img src="{{ foto }}" class="img-fluid mt-3 rounded">
  {% endif %}
</div>
{% endif %}
</div>
"""

def ejecutar():
    if request.method == 'POST':
        placa = request.form.get('placa')
        marca = request.form.get('marca')
        combustible = request.form.get('combustible')
        comentarios = request.form.get('comentarios')
        accesorios = request.form.get('accesorio')

        foto = request.files.get('foto')
        foto_url = None

        if foto and foto.filename:
            nombre = get_name_file(foto.filename, 15)
            ruta = os.path.join(UPLOAD_FOLDER, nombre)
            foto.save(ruta)
            foto_url = f"/static/images/{nombre}"

        return render_template_string(
            HTML,
            placa=placa,
            marca=marca,
            combustible=combustible,
            accesorios=accesorios,
            comentarios=comentarios,
            foto=foto_url,
            mostrar=True
        )

    return render_template_string(HTML, mostrar=False)
