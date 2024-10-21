#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# tex2html.py
# Primera versión

import argparse
import os.path
import config_ptn as ptn
import re
import shutil
from textwrap import dedent

# Configuración de argumentos para el programa usando argparse
parser = argparse.ArgumentParser(
    description='Convierte archivo LaTeX a html/mathJaX')
parser.add_argument("TeXfile", help="TeXfile es el archivo a convertir")
# Estaría bueno agregar un argumento -j --jerarquia con opciones 0 1 2 (por omisión 2)
# para poder cambiar la jerarquía desde la línea de comando
args = parser.parse_args()
# Hasta aquí la configuración de argparse


def docStrip(entrada, original, reemplazo):
    entrada = outputFileName

    if os.path.isfile(entrada):
        shutil.copyfile(entrada, entrada + ".tmp")
        salida = entrada

        with open(entrada + ".tmp") as infile:
            content = infile.read()

        with open(salida, "w") as temp:
            temp.write(re.sub(original, reemplazo, content,
                       flags=re.MULTILINE | re.UNICODE))

    else:
        print("El archivo " + entrada + " no existe.")


def docStripALL(entrada, original, reemplazo):
    entrada = outputFileName

    if os.path.isfile(entrada):
        shutil.copyfile(entrada, entrada + ".tmp")
        salida = entrada

        with open(entrada + ".tmp") as infile:
            content = infile.read()

        with open(salida, "w") as temp:
            temp.write(re.sub(original, reemplazo, content,
                       flags=re.MULTILINE | re.UNICODE | re.DOTALL))

    else:
        print("El archivo " + entrada + " no existe.")


def limpiarTeX():
    for i in range(len(ptn.reemplazosLimpiezaTeX)):
        docStrip(outputFileName,
                 ptn.reemplazosLimpiezaTeX[i][0], ptn.reemplazosLimpiezaTeX[i][1])


def quitaPreambuloTeX():
    inicial = "\\begin{document}"
    final = "\\end{document}"
    with open(outputFileName) as entrada:
        conpreambulo = entrada.read()
        preambulo = conpreambulo.split(inicial)[0]
        sinpreambulo = conpreambulo.split(inicial)[1]

        sinpostambulo = sinpreambulo.split(final)[0]

    with open(outputFileName, "w") as salida:
        salida.write(sinpostambulo)

    with open(preambuloFile, "w") as salidaPreambulo:
        salidaPreambulo.write(preambulo)


def obtenerJerarquia(archivo):
    jerarquia = -1
    with open(archivo) as infile:
        if '\\section' in infile.read():
            jerarquia = 2
    with open(archivo) as infile:
        if '\\chapter' in infile.read():
            jerarquia = 1
    with open(archivo) as infile:
        if '\\part' in infile.read():
            jerarquia = 0

    return jerarquia


def comandosTeXaHTML():
    for i in range(len(ptn.reemplazosTeXaHTML)):
        docStrip(outputFileName,
                 ptn.reemplazosTeXaHTML[i][0], ptn.reemplazosTeXaHTML[i][1])
    docStrip(outputFileName,
             r'\\begin\{abstract\}',
             r'<h3>Resumen</h3>\n'
             )
    docStrip(outputFileName,
             r'\\end\{abstract\}',
             r''
             )


def titularesTeXaHTML(jerarquia):
    count = 1
    for i in range(jerarquia, len(ptn.titularesTeX)):
        count += 1
        docStrip(outputFileName,
                 r'\\(\b' + ptn.titularesTeX[i] +
                 r'\b)(?:[{])(.*)(?:\})(?:\s*)(?:\\label)(?:[{])(.*)(?:\})',
                 r'<h' + str(count) + r' class="\1" id="\3">\2</h' +
                 str(count) + r'>'
                 )
        docStrip(outputFileName,
                 r'\\(' + ptn.titularesTeX[i] + r')(?:' + "\*" +
                 r')(?:[{])(.*)(?:\})(?:\s*)(?:\\label)(?:[{])(.*)(?:\})',
                 r'<h' +
                 str(count) + r' class="\1-starred" id="\3">\2</h' +
                 str(count) + r'>'
                 )


def restoAmbientesTeXaHTML(lista):
    for i in lista:
        docStrip(outputFileName,
                 "\\\\begin{" + i[0] + "}",
                 '<div class="' + i[0] + '">'
                 )
        docStrip(outputFileName,
                 '\\\\end{' + i[0] + "\}",
                 "</div>"
                 )


def ambientesTeXaHTML(enun_dist):
    for i in enun_dist:
        docStrip(outputFileName,
                 "\\\\begin{" + i[0] + "}" +
                 r'(?:\s*)(?:\\label)(?:[{])(.*)(?:\})',
                 '<div class="' + i[0] + r'" id="\1">'
                 )
        docStrip(outputFileName,
                 "\\\\begin{" + i[0] + "}\[" + r'([^]]*)' +
                 "\]" + r'(?:\s*)(?:\\label)(?:[{])(.*)(?:\})',
                 '<div class="' + i[0] + r'" id="\2">' + '(' + r'\1' + ')'
                 )
        docStrip(outputFileName,
                 '\\\\end{' + i[0] + "}",
                 "</div>"
                 )

    for i in ptn.entornos:
        docStrip(outputFileName,
                 # + r'(?:\s*)(?:\\label)(?:[{])(.*)(?:\})',
                 "\\\\begin{" + i[0] + "}",
                 '<div class="' + i[0] + '">'
                 )
        docStrip(outputFileName,
                 '\\\\end{' + i[0] + "}",
                 "</div>"
                 )


def estilosFuentesTeXaHTML():
    for i in ptn.estilos_fuentes:
        docStrip(outputFileName,
                 # "\\\\"+i+"{"+r'(.*)'+"}",
                 "\\\\"+i+"{"+r'([^}]*)'+"}",
                 '<em class="'+i+'">'+r'\1'+'</em>')


def urlTeXaHTML():
        docStrip(outputFileName,
                 # "\\\\"+i+"{"+r'(.*)'+"}",
                 "\\\\url{"+r'([^}]*)'+"}",
                 '<a target="_blank" href="'+r'\1'+'">'+r'\1'+'</a>')

def hrefTeXaHTML():
        docStrip(outputFileName,
                 # "\\\\"+i+"{"+r'(.*)'+"}",
                 "\\\\href{"+r'([^}]*)'+"}" + "{" + r'([^}]*)'+"}",
                 '<a target="_blank" href="'+r'\1'+'">'+r'\2'+'</a>')


def comillasTeXaHTML():
    for i in ptn.comandosTeXaHTML:
        docStrip(outputFileName,
                 # "\\\\"+i+"{"+r'(.*)'+"}",
                 "\\\\"+i[0]+"{"+r'([^}]*)'+"}",
                 '<'+i[1]+'>'+r'\1'+'<'+'/'+i[1]+'>')


def floatsTeXaHTML():
    for i in ptn.floats:
        docStrip(outputFileName,
                 "\\\\begin{" + i[0] + "}\[H\]\\\\label{" + r'([^}]*)' + "}"
                 + r'\s+' + "\\\\centering" + r'\s+'
                 + "\\\\includegraphics" + r'[^\{]*' + "{" + r'([^}]*)' + "}"
                 + r'\s+' + "\\\\caption" + r'[^\{]*' + "{" + r'([^}]*)' + "}"
                 + r'\s+' + "\\\\end{" + i[0] + "}",
                 '<div class="' + i[0] + '">\n'
                 + '<img src="./figs/divulgacion/' + r'\2' + '" width=500 />\n'
                 + '<div class="captionFigura" id="' + r'\1' + '">\n'
                 + r'\3' + '\n</div>\n</div>')

# Sustituir:
# \begin{figure}[H]\label{fig:pegado}
# 		\centering
#     \includegraphics[width=12cm]{colapso.pdf}
#     \caption{Función radial para la métrica en la cáscara de polvo.}
# \end{figure}
# Por esto:
# <div class="figure">
#    <img src="./figsDario/fotirris.png" width=500 />
#    <div class="captionFigura" id="usos">Algunos usos de las teselaciones. </div>
# </div>

######################################
# La función obtenerEnunciadosDistinguidos regresa una lista de listas con 5 elementos
## [envname, caption, emphasis, numberedlike, within]
# Esta lista sirve de entrada para dos cosas:
# 1. En la función TeXaHTML(lista) toma envname para determinar la clase de los div's en html
# 2. Todos los elementos sirven para determinar estilos en los css lógico y gráfico (pendiente)


def obtenerEnunciadosDistinguidos(archivo):

    énfasis = ['theorem']
    nivel_numeración = ['simple']
    lista = []

    with open(archivo) as preambulo:
        for line in preambulo:
            búsqueda = re.findall(r'(?:\\theoremstyle{)(.*)(?:})', line)
#			print(énfasis)
            if not búsqueda:  # búsqueda es lista vacía
                pass
            else:  # búsqueda tiene un elemento
                énfasis = búsqueda
            # Hasta aquí para determinar el énfasis

            # Ahora los enunciados del estilo {envname}[numberedlike]{caption}
            búsqueda = re.findall(
                r'(?:\\newtheorem{)(.*)(?:})(?:\[)(.*)(?:\])(?:{)(.*)(?:})', line)
            if not búsqueda:  # búsqueda es lista vacía
                pass
            else:  # búsqueda tiene un elemento
                enun_dist = búsqueda
                enun_dist = list(map(list, enun_dist))
                for i in enun_dist:
                    i[1], i[2] = i[2], i[1]
                    i.append(énfasis[0])
                    # Agregamos el nivel de énfasis
                    i.append(nivel_numeración[0])
                    lista.append(i)

            # Ahora los enunciados del estilo {envname}{caption}[within]
            búsqueda = re.findall(
                r'(?:\\newtheorem{)(.*)(?:})(?:{)(.*)(?:})(?:\[)(.*)(?:\])', line)
            if not búsqueda:  # búsqueda es lista vacía
                pass
            else:  # búsqueda tiene un elemento
                enun_dist = búsqueda
                enun_dist = list(map(list, enun_dist))
                for i in enun_dist:  # Cambiamos de orden nubmeredlike y caption
                    nivel_numeración[0] = i[2]
                    i.remove(i[2])
                    i.append(i[0])
                    i.append(énfasis[0])
                    # Agregamos el nivel de énfasis
                    i.append(nivel_numeración[0])
                    lista.append(i)

            # Ahora los enunciados del estilo {envname}{caption}
            búsqueda = re.findall(
                r'(?:\\newtheorem{)(.*)(?:})(?:{)(.*)(?:})(?:\s)', line)
            if not búsqueda:  # búsqueda es lista vacía
                pass
            else:  # búsqueda tiene un elemento
                enun_dist = búsqueda
                enun_dist = list(map(list, enun_dist))
                for i in enun_dist:
                    i.append(énfasis[0])
                    i.append(i[0])
                    # Agregamos el nivel de énfasis
                    i.append(nivel_numeración[0])
                    lista.append(i)

    return lista


def obtenerComandosMatem(archivo):

    lista = []

    with open(archivo) as preambulo:
        for line in preambulo:
            #			búsqueda = re.findall(r'(\\DeclareMathOperator{.*}{.*})(?:\s)',line)
            búsqueda = re.findall(r'(\\DeclareMathOperator.*)', line)
            if not búsqueda:  # búsqueda es lista vacía
                pass
            else:  # búsqueda tiene un elemento
                for i in búsqueda:
                    lista.append(i)

            búsqueda = re.findall(r'(\\newcommand.*)', line)
            if not búsqueda:  # búsqueda es lista vacía
                pass
            else:  # búsqueda tiene un elemento
                for i in búsqueda:
                    lista.append(i)

    return lista


def parrafosHTML(archivo, formato):
    infile = open(archivo, "r")
    infileread = infile.read().strip()
#	print (archivo, formato)
    pararrayout = []
    # Separamos el documento en párrafos y los guardamos en un arreglo
    pararrayin = infileread.split("\n\n")
    for i in pararrayin:
        if i[0] != '<div':
            pararrayout.append('<p class="'+formato+'">\n' + i + '\n</p>\n')
        else:
            pararrayout.append(i)

    with open(archivo, 'w') as f:
        for item in pararrayout:
            f.write("%s\n" % item)


def TeXaHTMLcompleto(entrada, jerarquia, comandos):
    entrada = outputFileName

    divcomandos = dedent("""\
		<div display="none">
		$\\newcommand{\\menorque}{<}$
		$\\newcommand{\\mayorque}{>}$
		""")
    for i in comandos:
        divcomandos += "$"+i+"$\n"
    divcomandos += "</div>\n"

    if os.path.isfile(entrada):
        shutil.copyfile(entrada, entrada + ".tmp")
        salida = entrada
        with open(entrada + ".tmp") as infile:
            content = infile.read()

        with open(salida, "w") as temp:
            if jerarquia < 2:
                temp.write(ptn.htmlHeaderBook + divcomandos +
                           content + ptn.htmlFooter)
            else:
                temp.write(ptn.htmlHeaderArt + divcomandos +
                           content + ptn.htmlFooter)


def quitaLineasBlancas(entrada):
    entrada = outputFileName

    if os.path.isfile(entrada):
        shutil.copyfile(entrada, entrada + ".tmp")
        salida = entrada
        with open(entrada + ".tmp") as infile:
            content = infile.read()
            sinlineas = content.strip()

        with open(salida, "w") as temp:
            temp.write(sinlineas)


def cleanFolder(archivo):
    nombre = archivo + ".tmp"
    if os.path.exists(nombre):
        os.remove(nombre)


def obtenerEtiquetas(archivo):
    lista_etiquetas = []
    with open(archivo) as aux:
        for line in aux:
            etiqueta = re.findall(r'(?:\\newlabel{)(.*)(?:}{{)([^}]*).*', line)
            if not etiqueta:
                pass
            else:
                lista_etiquetas.append(etiqueta)
    return lista_etiquetas


def sustituirComentariosTeXyHTML():
    docStripALL(outputFileName,
                r'\\begin\{commentHTML\}.*?\\end\{commentHTML\}',
                '')
    quitaLineasBlancas(outputFileName)


def notasalpieTeXaHTML():
    docStripALL(outputFileName,
                r'(\\footnote\{\{\{\{\{\{.*?\}\}\}\}\}\})',
                '<span class="tooltip">*<span class="tooltiptext">' + r'\1' + '</span></span>'
                )
    docStrip(outputFileName,
             r'\\footnote\{\{\{\{\{\{',
             '')
    docStrip(outputFileName,
             r'\}\}\}\}\}\}',
             '')


# def notasalpieTeXaHTML():
#     docStripALL(outputFileName,
#                 r'\\nota\{(.*?)\}\\footnote\{(.*?)\}',
#                 '<span class="tooltip">' + r'\1' + '<span class="tooltiptext">' + r'\2' + '</span></span>'
#                 )
    # docStrip(outputFileName,
    #          r'\\footnote\{\{\{\{\{\{',
    #          '')
    # docStrip(outputFileName,
    #          r'\}\}\}\}\}\}',
    #          '')



def PseudoHTMLaHTML():
    docStripALL(outputFileName,
                r'OpenHTML ',
                '<')
    docStripALL(outputFileName,
                r' CloseHTML',
                '>')


def quitadoblesBlancas():
    docStrip(outputFileName,
             '\n\n\n',
             '\n\n')


def cambiarReferenciasTeXaHTML(lista):

    for i in lista:
        docStrip(outputFileName, r'([~\s]*)'+"\\\\ref{"+i[0][0]+"}",
                 r'&nbsp;'+'<a href="#'+i[0][0]+'">'+i[0][1]+"</a>")


def listadosTeXaHTML(enun_dist):
    for i in ptn.listas:
        docStrip(outputFileName,
                 "\\\\begin{" + i[0] + "}",
                 '<'+i[1]+'>'
                 )
        docStrip(outputFileName,
                 '\\\\end{' + i[0] + "}",
                 "</"+i[1]+">"
                 )
        docStrip(outputFileName,
                 '\\\\item{{{{',
                 r'<li>\n'
                 )
        docStrip(outputFileName,
                 r'(?:\\item{)([^}]*)(?:})',
                 r'<li>\1</li>\n'
                 )
        docStrip(outputFileName,
                 # , re.DOTALL)', #(?:{{{)(\s.*)(?:}}})',
                 r'(?:\\item\[)([^]]*)(?:\]{{{)',
                 r'<dt>\1</dt>\n<dd>'
                 )
        docStrip(outputFileName,
                 "}}}}", '</li>')
        docStrip(outputFileName,
                 "}}}", '</dd>')
        # docStrip(outputFileName,
        #   r'(?:\\item\[)([^]]*)(?:\])(?:\{\{\{)(.*)(?:\}\}\})',
        #   r'<dt>\1</dt>\n<dd>\1</dd>\n'
        #   )
        docStrip(outputFileName,
                 r'(?:\\item\s*\{)(.*)(?:\})',
                 r'<li>\1</li>\n'
                 )
        docStrip(outputFileName,
                 r'(?:\\item)([^(\\<)]*)',
                 r'<li>\1</li>\n'
                 )

inputFileSplit = os.path.splitext(args.TeXfile)
outputFileName = inputFileSplit[0]+"_ptn.html"
preambuloFile = inputFileSplit[0]+'_ptn_preambulo.tex'
auxFile = inputFileSplit[0]+'.aux'

if inputFileSplit[1] != ".tex":
    ArchivoEntrada = args.TeXfile + ".tex"
    exists = os.path.isfile(args.TeXfile + ".tex")

else:
    exists = os.path.isfile(args.TeXfile)
    ArchivoEntrada = args.TeXfile

if exists:
    inputfile = open(ArchivoEntrada, "r")
    outputfile = shutil.copyfile(ArchivoEntrada, outputFileName)


def main():
    limpiarTeX()
    quitaPreambuloTeX()

    jerarquia = obtenerJerarquia(outputFileName)
    listaEnunDist = obtenerEnunciadosDistinguidos(preambuloFile)
    listaComandosMat = obtenerComandosMatem(preambuloFile)
    listaEtiquetas = obtenerEtiquetas(auxFile)

    notasalpieTeXaHTML()
    comandosTeXaHTML()
    titularesTeXaHTML(jerarquia)

    ambientesTeXaHTML(listaEnunDist)

    ambientesTeXaHTML(ptn.enunciados_distinguidos)

    listadosTeXaHTML(ptn.listas)
    
    restoAmbientesTeXaHTML(ptn.otros_ambientes)

    sustituirComentariosTeXyHTML()

#	ambientesTeXaHTML(ptn.otros_ambientes)

    estilosFuentesTeXaHTML()
    urlTeXaHTML()
    hrefTeXaHTML()
    
    cambiarReferenciasTeXaHTML(listaEtiquetas)

    PseudoHTMLaHTML()

    comillasTeXaHTML()

    floatsTeXaHTML()

    quitaLineasBlancas(outputFileName)
    quitadoblesBlancas()
    quitadoblesBlancas()
    quitadoblesBlancas()
    quitadoblesBlancas()
    quitadoblesBlancas()

    parrafosHTML(outputFileName, "justificado")

    TeXaHTMLcompleto(outputFileName, jerarquia, listaComandosMat)

    quitaLineasBlancas(outputFileName)

    cleanFolder(outputFileName)

    # for i in listaEnunDist:
    # 	print(i)

    # for i in listaEtiquetas:
    # 	print(i[0][0]+"\t"+i[0][1])


main()
