from flask import request, render_template_string

# =====================================================
# EJERCICIO: TALLER PAISES (ARREGLOS / MATRICES)
# CONVERSIÓN DIRECTA DE PHP A PYTHON
# =====================================================

HTML = """
<h2 class="text-center mb-4">TALLER - PAISES</h2>

{% for tabla in tablas %}
  {{ tabla|safe }}
{% endfor %}
"""

def ejecutar():
    """
    EJERCICIO DE ARREGLOS Y MATRICES
    Conversión directa del código PHP original a Python
    """

    # -------------------------------------------------
    # INDICES NUMERICOS (equivalente a $cantones)
    # -------------------------------------------------
    cantones = [
        ["QUITO", "CAYAMBE", "RUMIÑAHUI"],
        ["GUAYAQUIL", "DAULE", "SAMBORONDON", "BAEZA"],
        ["CUENCA", "LOJA"],
        ["ROCAFUERTE", "CHONE"]
    ]

    # -------------------------------------------------
    # MATRICES ASOCIATIVAS (equivalente a $Pais)
    # -------------------------------------------------
    Pais = {
        "ECUADOR": {
            "Pichincha": ["QUITO", "CAYAMBE", "RUMIÑAHUI"],
            "Guayas": cantones[1],
            "Azuay": ["Cuenca"],
            "Manabi": cantones[3],
            "Tunguragua": ["Ambato"]
        },

        "ESTADOS UNIDOS": {
            "NEW YORK": ["BUFALO", "ALBANY", "TROY", "NEW YORK"],
            "PENSILVANNIA": ["FILALDEFIA", "PISTBURG"],
            "FLORIDA": ["MIAMI", "ORLANDO", "TAMPA", "FORT LOUDARLE"],
            "COLORADO": ["GOLDEN", "AVON", "DURANGO", "COMMERCECITY", "STERLING", "PUEBLOWEST"]
        },

        "ARGENTINA": {
            "BUENOS AIRES": ["BUFALO", "ALBANY", "TROY", "NEW YORK"],
            "JUJUY": ["FILALDEFIA", "PISTBURG"],
            "LA PAMPA": ["MIAMI", "ORLANDO", "TAMPA"]
        },

        "COLOMBIA": {
            "ANTIOQUIA": ["MEDELLIN", "PASTO"],
            "ARAUCA": ["RUMBA", "BOGOTA", "BARANQUILLA"]
        }
    }

    # -------------------------------------------------
    # PROCESO PRINCIPAL (equivalente al foreach PHP)
    # -------------------------------------------------
    tablas = []

    for pais, info in Pais.items():

        html = "<br><br>"
        html += f"<strong>PAIS : {pais}</strong><br>"

        # ---------------------------------------------
        # CALCULO DEL MAXIMO DE COLUMNAS
        # ---------------------------------------------
        maxColum = 0
        for provincia, arreglo in info.items():
            tam = len(arreglo)
            maxColum = max(maxColum, tam)

        html += f"MAXCOLUM: {maxColum}<br>"
        html += f"NUMERO DE PROVINCIAS: {len(info)}<br><br>"

        # ---------------------------------------------
        # CREAR TABLA
        # ---------------------------------------------
        html += "<table border='1' align='center'>"

        # TITULO
        html += f"""
        <tr>
          <th colspan="{len(info)}" bgcolor="#EC7063">
            {pais}
          </th>
        </tr>
        """

        # CABECERA (provincias)
        html += "<tr>"
        for provincia in info.keys():
            html += f"<th>{provincia}</th>"
        html += "</tr>"

        # ---------------------------------------------
        # CUERPO DE LA TABLA (recorrido tipo cubo)
        # ---------------------------------------------
        for f in range(maxColum):
            html += "<tr>"
            for data in info.values():
                if f < len(data):
                    html += f"<td bgcolor='#D6FAF2'>{data[f]}</td>"
                else:
                    html += "<td bgcolor='#D6DEFA'>&nbsp;</td>"
            html += "</tr>"

        html += "</table><br><br>"

        tablas.append(html)

    # -------------------------------------------------
    # SALIDA FINAL
    # -------------------------------------------------
    return render_template_string(HTML, tablas=tablas)
