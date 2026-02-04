from flask import request, render_template_string

HTML = """
<style>
table{
  margin:auto;
  background:white;
  border-collapse: collapse;
}
td, th{
  padding:6px 10px;
  border:1px solid #333;
  text-align:center;
}
.blink{
  animation: blink 1s linear infinite;
  font-weight:bold;
  color:black;
}
@keyframes blink {
  50% { opacity:0; }
}
.table-wrap{
  width:100%;
  overflow-x:auto;
}
</style>

<h2 class="text-center mb-3">TALLER - PROVINCIAS</h2>

{% if mostrar %}

<h4>Cantones de las provincias de cada país</h4>
<pre style="background:white; padding:15px; border-radius:10px;">
{{ paises }}
</pre>

<h4>Representación en Tablas</h4>

{% for tabla in tablas %}
  <div class="table-wrap">
    {{ tabla|safe }}
  </div>
{% endfor %}

{% else %}
<div class="alert alert-secondary text-center">
  Presione <strong>Ejecutar ejercicio</strong> para visualizar las tablas dinámicas.
</div>
{% endif %}
"""

def ejecutar():

    # ============================
    # CONTROL: NO ejecutar en GET
    # ============================
    if request.method == "GET":
        return render_template_string(HTML, mostrar=False)

    # ============================
    # MATRIZ PRINCIPAL (IGUAL A PHP)
    # ============================
    paises = {

        "ECUADOR": {
            "Pichincha": ["QUITO","CAYAMBE","RUMIÑAHUI","MEJÍA","PEDRO MONCAYO","PUERTO QUITO","SAN MIGUEL DE LOS BANCOS"],
            "Guayas": ["GUAYAQUIL","DURÁN","MILAGRO","DAULE","SAMBORONDÓN","PLAYAS","BALAO"],
            "Azuay": ["CUENCA","GUALACEO","PAUTE","SANTA ISABEL","SÍGSIG","EL PAN","GIRÓN"],
            "Manabí": ["PORTOVIEJO","MANTA","CHONE","JIPIJAPA","PEDERNALES","PAJÁN","ROCAFUERTE"],
            "Tungurahua": ["AMBATO","BAÑOS","CEVALLOS","PÍLLARO","PATATE","QUERO","TISALEO"],
            "Sucumbíos": ["NUEVA LOJA","SHUSHUFINDI","LAGO AGRIO","PUTUMAYO","CUYABENO","GONZALO PIZARRO","CASCALES"],
            "Loja": ["LOJA","CATAMAYO","MACARÁ","ZAPOTILLO","SARAGURO","GONZANAMÁ","CELICA"]
        },

        "COLOMBIA": {
            "Cundinamarca": ["BOGOTÁ","CHÍA","ZIPAQUIRÁ","SOACHA","FACATATIVÁ","FUSAGASUGÁ","LA CALERA"],
            "Antioquia": ["MEDELLÍN","ENVIGADO","ITAGÜÍ","RIONEGRO","BELLO","LA ESTRELLA","COPACABANA"],
            "Valle del Cauca": ["CALI","PALMIRA","YUMBO","JAMUNDÍ","BUGA","BUENAVENTURA","TULUÁ"],
            "Santander": ["BUCARAMANGA","FLORIDABLANCA","GIRÓN","PIEDECUESTA","SAN GIL","BARBOSA","ZAPATOCA"],
            "Atlántico": ["BARRANQUILLA","SOLEDAD","GALAPA","PUERTO COLOMBIA","MALAMBO","TUBARÁ","LURUACO"],
            "Bolívar": ["CARTAGENA","MAGANGUÉ","TURBACO","MOMPÓS","ARJONA","SIMITÍ","SAN JUAN NEPOMUCENO"],
            "Nariño": ["PASTO","TÚQUERRES","IPIALES","SAMANIEGO","LA CRUZ","EL TAMBO","BARBACOAS"]
        },

        "USA": {
            "California": ["SACRAMENTO","LOS ANGELES","SAN DIEGO","SAN FRANCISCO","SAN JOSÉ","FRESNO","OAKLAND"],
            "Texas": ["AUSTIN","HOUSTON","DALLAS","SAN ANTONIO","EL PASO","FORT WORTH","ARLINGTON"],
            "Florida": ["TALLAHASSEE","MIAMI","ORLANDO","TAMPA","JACKSONVILLE","SARASOTA","OCALA"],
            "New York": ["ALBANY","NYC","BUFFALO","ROCHESTER","SYRACUSE","YONKERS","UTICA"],
            "Illinois": ["SPRINGFIELD","CHICAGO","NAPERVILLE","AURORA","JOLIET","ELGIN","WAUKEGAN"],
            "Washington": ["OLYMPIA","SEATTLE","TACOMA","SPOKANE","BELLEVUE","YAKIMA","EVERETT"],
            "Georgia": ["ATLANTA","SAVANNAH","AUGUSTA","COLUMBUS","MACON","ATHENS","ALBANY"]
        },

        "CHINA": {
            "Beijing": ["BEIJING","HAIDIAN","CHAOYANG","DONGCHENG","FANGSHAN","MENTOUGOU","XICHENG"],
            "Shanghai": ["SHANGHAI","PUDONG","XUHUI","MINHANG","JINGAN","BAOSHAN","SONGJIANG"],
            "Guangdong": ["GUANGZHOU","SHENZHEN","FOSHAN","ZHUHAI","DONGGUAN","ZHONGSHAN","JIANGMEN"],
            "Zhejiang": ["HANGZHOU","NINGBO","WENZHOU","JINHUA","HUZHOU","TAIZHOU","SHAOXING"],
            "Sichuan": ["CHENGDU","MIANYANG","NANCHONG","LUZHOU","DÀZHOU","DEYANG","LESHAN"],
            "Hubei": ["WUHAN","YICHANG","XIANGYANG","EZHOU","HUANGGANG","JINGMEN","SHIYAN"],
            "Shandong": ["JINAN","QINGDAO","YANTAI","WEIFANG","RIZHAO","ZIBO","DEZHOU"]
        }
    }

    # ============================
    # GENERACIÓN DE TABLAS (IGUAL PHP)
    # ============================
    tablas = []

    for pais, infoPais in paises.items():

        max_filas = max(len(c) for c in infoPais.values())

        html = f"<br><strong>PAÍS: {pais}</strong><br>"
        html += "<table>"
        html += f"<tr><th colspan='{len(infoPais)}' bgcolor='#EC7063'>{pais}</th></tr><tr>"

        for prov in infoPais:
            html += f"<th>{prov}</th>"
        html += "</tr>"

        for i in range(max_filas):
            html += "<tr>"
            for cantones in infoPais.values():
                if i == 0:
                    html += f"<td class='blink' bgcolor='#D6FAF2'>{cantones[0]}</td>"
                else:
                    html += (
                        f"<td bgcolor='#D6FAF2'>{cantones[i]}</td>"
                        if i < len(cantones)
                        else "<td bgcolor='#D6DEFA'>&nbsp;</td>"
                    )
            html += "</tr>"

        html += "</table><br>"
        tablas.append(html)

    return render_template_string(
        HTML,
        mostrar=True,
        paises=paises,
        tablas=tablas
    )
