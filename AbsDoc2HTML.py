import re

def leer_tuples(input_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        contenido = file.read()
        return eval(contenido) 

def aplicar_formato(texto, formatos):
    for formato in formatos:
        if formato == "chapter":
            texto = f"<h1>{texto}</h1>\n"
        elif formato == "section":
            texto = f"<h2>{texto}</h2>\n"
        elif formato == "teorema":
            texto = f"<div><strong>Teorema:</strong> {texto}</div>\n"
        elif formato == "paragraph":
            texto = f"<p>{texto}</p>\n"
    return texto

def analizar_tupla(t, formatos_ac=None):
    if formatos_ac is None:
        formatos_ac = []

    if isinstance(t[0], str):
        texto = t[0]
        formato = t[1]
        formatos_ac.append(formato)
        texto_con_formatos = aplicar_formato(texto, reversed(formatos_ac))
        return texto_con_formatos
    elif isinstance(t[0], tuple):
        formato = t[1]
        formatos_ac.append(formato)
        return analizar_tupla(t[0], formatos_ac)
    else:
        raise ValueError("No válido")

def tuplas_2_html(input_file, output_file):
    tuplas = leer_tuples(input_file)
    resultado = ''.join(analizar_tupla(tupla) for tupla in tuplas) 
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('<!DOCTYPE html>\n<html>\n<head>\n')
        file.write('<script id="MathJax-script" async src="https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js"></script>\n')
        file.write('</head>\n<body>\n')
        file.write(resultado)
        file.write('\n</body>\n</html>')

if __name__ == '__main__':
    input_file = 'prueba.txt'  
    output_file = 'prueba.html' 

    tuplas_2_html(input_file, output_file)
    print("El archivo ha sido convertido a prueba.html.")
