from abc import ABC, abstractmethod
from math import sqrt
from typing import Dict, Any
from flask import request, render_template_string


# ---------------------------
# 1) CLASE ABSTRACTA
# ---------------------------
class Figura(ABC):
    @staticmethod
    def get_form_html() -> str:
        return """
        <form method="POST" id="figForm" class="mt-3">

          <div class="mb-3">
            <label class="form-label fw-bold">Tipo de figura</label>
            <select name="tipo" id="tipo" class="form-select" onchange="updateFields()" required>
              <option value="">Seleccione...</option>
              <option value="cuadrado">Cuadrado</option>
              <option value="rectangulo">Rectángulo</option>
              <option value="triangulo">Triángulo</option>
            </select>
          </div>

          <div class="row g-3">
            <div class="col-md-4" id="r_l1">
              <label class="form-label">Lado 1</label>
              <input type="number" name="l1" step="any" class="form-control">
            </div>

            <div class="col-md-4" id="r_l2">
              <label class="form-label">Lado 2</label>
              <input type="number" name="l2" step="any" class="form-control">
            </div>

            <div class="col-md-4" id="r_l3">
              <label class="form-label">Lado 3</label>
              <input type="number" name="l3" step="any" class="form-control">
            </div>
          </div>

          <div class="d-grid mt-4">
            <button type="submit" class="btn btn-primary btn-lg">
              Calcular fórmulas
            </button>
          </div>
        </form>

        <script>
        function updateFields(){
          const tipo = document.getElementById('tipo').value;
          const r1 = document.getElementById('r_l1');
          const r2 = document.getElementById('r_l2');
          const r3 = document.getElementById('r_l3');

          // Ocultar todos
          r1.style.display = 'none';
          r2.style.display = 'none';
          r3.style.display = 'none';

          if(tipo === 'cuadrado'){
            r1.style.display = 'block';
          } else if(tipo === 'rectangulo'){
            r1.style.display = 'block';
            r2.style.display = 'block';
          } else if(tipo === 'triangulo'){
            r1.style.display = 'block';
            r2.style.display = 'block';
            r3.style.display = 'block';
          }
        }
        document.addEventListener('DOMContentLoaded', updateFields);
        </script>
        """

    @abstractmethod
    def area(self) -> None:
        pass

    @abstractmethod
    def perimetro(self) -> None:
        pass

    @abstractmethod
    def get_area(self) -> float:
        pass

    @abstractmethod
    def get_perimetro(self) -> float:
        pass

    @abstractmethod
    def get_tipo(self) -> str:
        pass

# ---------------------------
# 2) CLASES HIJAS
# ---------------------------
class Cuadrado(Figura):
    def __init__(self, lado1: float):
        self.tipo = "cuadrado"
        self.lado1 = float(lado1)
        self._a = 0.0
        self._p = 0.0

    def area(self) -> None:
        self._a = self.lado1 ** 2

    def perimetro(self) -> None:
        self._p = self.lado1 * 4

    def get_area(self) -> float:
        return self._a

    def get_perimetro(self) -> float:
        return self._p

    def get_tipo(self) -> str:
        return self.tipo


class Rectangulo(Figura):
    def __init__(self, lado1: float, lado2: float):
        self.tipo = "rectangulo"
        self.lado1 = float(lado1)
        self.lado2 = float(lado2)
        self._a = 0.0
        self._p = 0.0

    def area(self) -> None:
        self._a = self.lado1 * self.lado2

    def perimetro(self) -> None:
        self._p = 2 * (self.lado1 + self.lado2)

    def get_area(self) -> float:
        return self._a

    def get_perimetro(self) -> float:
        return self._p

    def get_tipo(self) -> str:
        return self.tipo


class Triangulo(Figura):
    def __init__(self, lado1: float, lado2: float, lado3: float):
        self.tipo = "triangulo"
        self.lado1 = float(lado1)
        self.lado2 = float(lado2)
        self.lado3 = float(lado3)
        self._a = 0.0
        self._p = 0.0

    def perimetro(self) -> None:
        self._p = self.lado1 + self.lado2 + self.lado3

    def area(self) -> None:
        # Fórmula de Herón
        self.perimetro()
        sp = self._p / 2
        self._a = sqrt(sp * (sp - self.lado1) * (sp - self.lado2) * (sp - self.lado3))

    def get_area(self) -> float:
        return self._a

    def get_perimetro(self) -> float:
        return self._p

    def get_tipo(self) -> str:
        return self.tipo


# ---------------------------
# 3) PROCESAR FORM (request.form)
# ---------------------------
def process_form(form_data: Dict[str, Any]) -> str:
    tipo = (form_data.get("tipo") or "").strip()

    # Si aún no eligió tipo, mostramos el formulario
    if not tipo:
        return Figura.get_form_html()

    try:
        if tipo == "cuadrado":
            l1 = (form_data.get("l1") or "").strip()
            if not l1:
                return Figura.get_form_html() + "<div class='alert alert-warning mt-3'>Ingrese el lado 1.</div>"
            obj: Figura = Cuadrado(float(l1))

        elif tipo == "rectangulo":
            l1 = (form_data.get("l1") or "").strip()
            l2 = (form_data.get("l2") or "").strip()
            if not l1 or not l2:
                return Figura.get_form_html() + "<div class='alert alert-warning mt-3'>Ingrese lado 1 y lado 2.</div>"
            obj = Rectangulo(float(l1), float(l2))

        elif tipo == "triangulo":
            l1 = (form_data.get("l1") or "").strip()
            l2 = (form_data.get("l2") or "").strip()
            l3 = (form_data.get("l3") or "").strip()
            if not l1 or not l2 or not l3:
                return Figura.get_form_html() + "<div class='alert alert-warning mt-3'>Ingrese los tres lados.</div>"
            obj = Triangulo(float(l1), float(l2), float(l3))

        else:
            return Figura.get_form_html() + "<div class='alert alert-danger mt-3'>Tipo inválido.</div>"

        # Calcular
        obj.area()
        obj.perimetro()

        # Mostrar resultados (y dejamos el formulario arriba para que puedan recalcular)
        return (
            Figura.get_form_html()
            + "<hr>"
            + f"<p><b>Figura:</b> {obj.get_tipo()}</p>"
            + f"<p><b>Área:</b> {obj.get_area():.2f}</p>"
            + f"<p><b>Perímetro:</b> {obj.get_perimetro():.2f}</p>"
        )

    except ValueError:
        return Figura.get_form_html() + "<div class='alert alert-danger mt-3'>Ingrese números válidos.</div>"


# ---------------------------
# 4) FUNCIÓN PARA TU SISTEMA 
# ---------------------------
def ejecutar():
    """
    Esta función se usa en tu ruta /ejecutar/<slug>.
    Devuelve HTML (como string) para que 'detalle.html' lo muestre con {{ contenido|safe }}.
    """
    if request.method == "POST":
        contenido = process_form(request.form)
    else:
        contenido = Figura.get_form_html()

    # Si quieres envolverlo con algo extra, puedes hacerlo aquí
    return render_template_string(contenido)
