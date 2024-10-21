# El archivo de configuración por omisión para tex2html.py

from textwrap import dedent
listas = [
    ["itemize", "ul"],
    ["enumerate", "ol"],
    ["description", "dl"]
]

enunciados_distinguidos = [
    ["theorem", "Teorema", "theorem", "theorem", 1],
    ["thm", "Teorema", "theorem", "theorem", 1],
    ["teorema", "Teorema", "theorem", "theorem", 1],
    ["teo", "Teorema", "theorem", "theorem", 1],
    ["lema", "Lema", "theorem", "theorem", 1],
    ["lemma", "Lema", "theorem", "theorem", 1],
    ["corolario", "Corolario", "theorem", "theorem", 1],
    ["coro", "Corolario", "theorem", "theorem", 1],
    ["cor", "Corolario", "theorem", "theorem", 1],
    ["defi", "Definición", "theorem", "theorem", 1],
    ["prop", "Proposición", "theorem", "theorem", 1],
    ["obs", "Observación", "theorem", "theorem", 1],
    ["con", "Conjetura", "theorem", "theorem", 1],
    ["proof", "Demostración", "theorem", "theorem", 1],
]

otros_ambientes = [
    ["verse", "verse"],
    ["epigrafe", "epigrafe"],
    ["quotation", "quotation"],
    ["center", "verse"],
]

estilos_fuentes = [
    "textbf",
    "textit",
    "textsl",
    "texttt",
    "textsc",
    "emph",
]

excepciones = [
    "equation",
    "align",
    "gather",
]

entornos = [
    ["mdframed", "mdframed"],
    ["abstract", "resumen"],
]

floats = [
    ["figure", "captionFigura"],
    ["table", "captionTabla"],
]

# La jerarquía de los encabezados:
# Si el nivel principal es part entonces la jerarquía es 0 (libros)
# Si el nivel principal es chapter entonces la jerarquía es 1 (libros)
# Si el nivel principal es section entonces la jerarquía es 2 (artículos, etc)
jerarquia = 2

titularesTeX = [
    "part",
    "chapter",
    "section",
    "subsection",
    "subsubsection"
]

reemplazosLimpiezaTeX = [
    ["\\\%", "\\\Porcentaje"],
    [r'\%.*', '\n'],
    ["<", " \\\menorque "],
    [">", " \\\mayorque "],
    [r'^\s*$', ''],
    [r' +$', ''],
    [r'  +', ' '],
    [u'\ufeff', '']
    # [r'\n','']
]

reemplazosTeXaHTML = [
    ["\\\Porcentaje", "%"],
    # Útil para diferenciar de \textit. Para uso dentro de \text en modo matemático.
    ["\\\itshape", ''],
    ["---", "&mdash;"],
    ["\\\\nocite{\*}", ''],
    ["\\\printbibliography", '<h2 class="section-starred">Referencias</h2>'],  # Para MM
    ["\\\\begin{commentTeX}", ''],
    ["\\\\end{commentTeX}", ''],
]

comandosTeXaHTML = [
    # El archivo de LaTeX no debe tener comillas, usar el comando enquote
    ["enquote", "q"],
]


htmlHeaderArt = ''

# htmlHeaderArt = dedent("""\
# <!DOCTYPE html>
# <html>
# <head>
# 	<title></title>
# 	<meta charset="utf-8">
# 	<link rel="stylesheet" type="text/css" href="./scripts/css/ptn-art-logic.css">
# 	<link rel="stylesheet" type="text/css" href="./scripts/css/ptn-art-graphic.css">
# 	<link rel="stylesheet" type="text/css" href="./scripts/css/ptn-art-media.css">
# 	<script src="https://ajax.googleapis.com/ajax/libs/jquery/1.11.3/jquery.min.js"></script>
#   <script type="text/javascript" src="../../scripts/js/menu.js"></script>

# <script type="text/x-mathjax-config">
#       MathJax.Hub.Config({
#         tex2jax: {
#           inlineMath: [["$","$"],["\\\\(","\\\\)"]],
#           processEscapes: true,
#         },
#         TeX: {equationNumbers: {autoNumber: "AMS",
#           formatURL: function (id) {return 'aplicadas.html'+'#'+escape(id) }
#           },
#         }
#       });

# </script>

# <script type="text/javascript"
#    src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
# </script>
# </head>
# <body>
# """)

htmlHeaderBook = dedent("""\
<!DOCTYPE html>
<html>
<head>
	<title></title>
	<meta charset="utf-8">
	<link rel="stylesheet" type="text/css" href="../src/scripts/css/ptn-book-logic.css">
	<link rel="stylesheet" type="text/css" href="../src/scripts/css/ptn-book-graphic.css">
	<link rel="stylesheet" type="text/css" href="../src/scripts/css/ptn-book-media.css">
	<script type="text/x-mathjax-config">
		MathJax.Hub.Config({
			tex2jax: {inlineMath: [['$','$'], ['\\\\(','\\\\)']]}
		});
	</script>
	<script type="text/javascript"
		src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.1/MathJax.js?config=TeX-AMS-MML_HTMLorMML">
	</script>	
</head>
<body>
""")

htmlFooter = ''

# htmlFooter = dedent("""\
# </body>
# </html>
# """)
