# backend/geometry.py
import math

def to_positive_float(value_str, field_name, errors):
    if value_str == "":
        return None
    try:
        value = float(value_str)
        if value <= 0:
            errors.append(f"El valor de {field_name} debe ser positivo.")
            return None
        return value
    except ValueError:
        errors.append(f"El valor de {field_name} debe ser numérico.")
        return None

def is_valid_triangle(sides, errors):
    a,b,c = sides
    if a+b<=c or a+c<=b or b+c<=a:
        errors.append("Los lados ingresados no forman un triángulo válido (desigualdad triangular).")
        return False
    return True

def triangle_type(sides):
    a,b,c = sides
    eps=1e-9
    iguales=[abs(a-b)<eps,abs(a-c)<eps,abs(b-c)<eps]
    if all(iguales): return "equilátero"
    elif any(iguales): return "isósceles"
    else: return "escaleno"

def process_figure(figura, l1_str, l2_str, l3_str):
    errors=[]
    result=None
    if not figura:
        errors.append("Debe seleccionar una figura geométrica.")
        return None, errors
    figura=figura.lower()
    if figura not in ["cuadrado","rectangulo","triangulo"]:
        errors.append("Figura no válida.")
        return None, errors

    l1 = to_positive_float(l1_str,"l1",errors) if l1_str!="" else None
    l2 = to_positive_float(l2_str,"l2",errors) if l2_str!="" else None
    l3 = to_positive_float(l3_str,"l3",errors) if l3_str!="" else None

    if figura=="cuadrado":
        if l1 is None:
            errors.append("Debe ingresar l1.")
        else:
            area=l1*l1
            perimetro=4*l1
            result={"figura":"Cuadrado","lados":[l1],"area":area,"perimetro":perimetro}

    elif figura=="rectangulo":
        if l1 is None or l2 is None:
            errors.append("Debe ingresar l1 y l2.")
        else:
            area=l1*l2
            perimetro=2*(l1+l2)
            result={"figura":"Rectángulo","lados":[l1,l2],"area":area,"perimetro":perimetro}

    elif figura=="triangulo":
        if l1 is None or l2 is None or l3 is None:
            errors.append("Debe ingresar l1, l2 y l3.")
        else:
            lados=[l1,l2,l3]
            if is_valid_triangle(lados,errors):
                perimetro=sum(lados)
                s=perimetro/2
                area=math.sqrt(s*(s-l1)*(s-l2)*(s-l3))
                tipo=triangle_type(lados)
                result={"figura":"Triángulo","lados":lados,"area":area,"perimetro":perimetro,"tipo_triangulo":tipo}

    return result, errors
