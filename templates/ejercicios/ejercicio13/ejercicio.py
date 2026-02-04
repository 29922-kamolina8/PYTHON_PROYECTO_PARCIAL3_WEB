import math
from flask import request

# ============================
# CLASE FIGURA (POO)
# ============================
class Figura:
    def __init__(self, tipo, l1, l2=None, l3=None):
        self.tipo = tipo
        self.l1 = l1
        self.l2 = l2
        self.l3 = l3
        self.area = 0
        self.perimetro = 0

    def calcular_perimetro(self):
        if self.tipo == "cuadrado":
            self.perimetro = self.l1 * 4

        elif self.tipo == "rectangulo":
            self.perimetro = (self.l1 * 2) + (self.l2 * 2)

        elif self.tipo == "triangulo":
            self.perimetro = self.l1 + self.l2 + self.l3

        return self.perimetro

    def calcular_area(self):
        if self.tipo == "cuadrado":
            self.area = self.l1 ** 2

        elif self.tipo == "rectangulo":
            self.area = self.l1 * self.l2

        elif self.tipo == "triangulo":
            self.calcular_perimetro()
            s = self.perimetro / 2
            self.area = math.sqrt(
                s * (s - self.l1) * (s - self.l2) * (s - self.l3)
            )

        return self.area


# ============================
# FUNCIÓN EJECUTAR (FLASK)
# ============================
def ejecutar():

    # GET → solo muestra formulario
    if request.method == "GET":
        return ""

    # POST → procesa datos
    tipo = request.form["tipo"]
    l1 = float(request.form["lado1"])
    l2 = request.form.get("lado2")
    l3 = request.form.get("lado3")

    l2 = float(l2) if l2 else None
    l3 = float(l3) if l3 else None

    figura = Figura(tipo, l1, l2, l3)

    area = figura.calcular_area()
    per = figura.calcular_perimetro()

    return f"""
    <div class="alert alert-success">
      <h4>Resultado</h4>
      <p><strong>Figura:</strong> {tipo.capitalize()}</p>
      <p><strong>Área:</strong> {area:.2f}</p>
      <p><strong>Perímetro:</strong> {per:.2f}</p>
    </div>
    """
