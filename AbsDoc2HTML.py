import re

# Diccionario con los formatos y equivalencias
formatos_disponibles = {
    "chapter": "<h1 id='{id}'>{}</h1>",
    "section": "<h2 id='{id}'>{}</h2>",
    "subsection": "<h3 id='{id}'>{}</h3>",
    "paragraph": "<p>{}</p>",
    "italics": "<i>{}</i>",
    "boldfont": "<b>{}</b>"
}

# Diccionario para almacenar referencias cruzadas
cross_references = {}

# Extraer etiquetas y referenciarlas
def obtener_etiqueta(item):
    """Extrae y devuelve la etiqueta de un item si existe."""
    if isinstance(item, str) and item.startswith("label:"):
        return item.split("label:")[1]
    return None

# Función para aplicar los formatos desde las tuplas más internas hacia las externas
def aplicar_formato(contenido, formatos, label=None):
    ##Aplica los formatos desde el más interno hasta el más externo.
    for formato in formatos:
        if formato in formatos_disponibles:
            if label:  # Si hay una etiqueta, se inserta en el id del elemento
                contenido = formatos_disponibles[formato].format(contenido, id=label)
            else:
                contenido = formatos_disponibles[formato].format(contenido, id="")
    return contenido

# Función recursiva para transformar la lista de tuplas a HTML
def tuple_2_html(data):
    if isinstance(data, str): 
        return data
    elif isinstance(data, tuple):
        text_parts = []
        formatos = []
        label = None
        for item in data:
            if isinstance(item, str) and item in formatos_disponibles:  # Identifica formato
                formatos.append(item)
            elif isinstance(item, tuple):  # Recursión
                text_parts.append(tuple_2_html(item))
            else:
                # Si es una etiqueta, la almacenamos
                possible_label = obtener_etiqueta(item)
                if possible_label:
                    label = possible_label
                    cross_references[label] = item  # Guarda la referencia
                else:
                    text_parts.append(str(item))
        contenido = "".join(text_parts)
        return aplicar_formato(contenido, formatos, label)
    elif isinstance(data, list):
        html_parts = []
        for item in data:
            html_parts.append(tuple_2_html(item))
        return "".join(html_parts)

# Leer la lista de tuplas desde un archivo .txt
def leer_tuplas(filename):
    """Lee una lista de tuplas desde un archivo de texto y la evalúa como una lista."""
    with open("prueba.txt", "r", encoding="utf-8") as file:
        contenido = file.read()
        # Convertir la cadena leída en una lista de tuplas usando eval
        return eval(contenido)

# Generar índice analítico
def generar_index():
    """Genera un índice analítico con las referencias cruzadas."""
    index_html = "<h2>Índice Analítico</h2><ul>"
    for label, ref in cross_references.items():
        index_html += f"<li><a href='#{label}'>{label}</a></li>"
    index_html += "</ul>"
    return index_html

# Archivo de entrada
input_filename = "prueba.txt"

# Leer la lista de tuplas
data = leer_tuplas(input_filename)

# Convertir la lista a HTML
html_output = tuple_2_html(data)

# Generar el índice analítico y agregarlo al HTML
index_html = generar_index()
html_output += index_html

# Guardar el HTML en un archivo
with open("prueba.html", "w", encoding="utf-8") as file:
    file.write('<!DOCTYPE html>\n<html>\n<head>\n')
    #file.write('<link rel="stylesheet" href="hoja_de_estilo_de_Joseph.css"')
    file.write('<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>\n')
    file.write('</head>\n<body>\n')
    file.write(html_output)
    file.write('\n</body>\n</html>')

print('El archivo ha sido convertido a "prueba.html"')
