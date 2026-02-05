def generar_triangulo_pascal(filas):
    """
    Genera el triángulo de Pascal con el número de filas especificado.

    Args:
        filas (int): Número de filas del triángulo (1 a 10)

    Returns:
        list: Lista de listas con los valores del triángulo de Pascal
    """
    if filas < 1 or filas > 10:
        return []

    pascal = []

    for i in range(filas):
        pascal.append([])
        pascal[i].append(1)  # Primer elemento siempre es 1

        # Elementos intermedios
        for j in range(1, i):
            pascal[i].append(pascal[i - 1][j - 1] + pascal[i - 1][j])

        # Último elemento siempre es 1 (excepto en la primera fila)
        if i > 0:
            pascal[i].append(1)

    return pascal


def formatear_triangulo_pascal(pascal):
    """
    Formatea el triángulo de Pascal para mostrarlo centrado en HTML.

    Args:
        pascal (list): Lista de listas con el triángulo de Pascal

    Returns:
        str: Código HTML con el triángulo formateado
    """
    if not pascal:
        return ""

    filas = len(pascal)
    columnas = 2 * filas - 1
    centro = filas - 1
    ancho = 4  # Espacio fijo por número

    # Crear matriz vacía para centrar los números
    grid = [['' for _ in range(columnas)] for _ in range(filas)]

    # Colocar los números del triángulo
    for f in range(filas):
        for k in range(len(pascal[f])):
            c = centro - f + 2 * k
            grid[f][c] = str(pascal[f][k])

    # Construir HTML
    html = (
        "<pre style='font-size:20px; line-height:1.3; "
        "text-align:center; font-family:\"Courier New\", monospace;'>"
    )

    for f in range(filas):
        for c in range(columnas):
            if grid[f][c] == '':
                html += ' ' * ancho
            else:
                html += grid[f][c].center(ancho)
        html += "\n"

    html += "</pre>"

    return html
