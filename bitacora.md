# Bitácora de Trabajo

## Agosto

- Semana del 5: Quedamos en aprender a programar en Python y HTML por separado y traer un convertidor funcional minimal dentro de dos semanas.
- Semana del 12: Nos reunimos nuevamente porque no sentimos que ayudaran las cosas que aprendimos de Python en el diseño del convertidor.
- Semana del 19: Vimos cómo leer y escribir datos en un .txt desde Python, con el objeto file.
- Semana del 23: Acordamos vernos lunes, miércoles y viernes para estar en sintonía y avanzar más rápido. Martes y jueves trabajaremos por nuestra cuenta en nuestras habilidades de programación.
  - Lunes: Investigamos sobre la programación orientada a objetos, los principios SOLID y su relevancia para un convertidor mantenible.
  - Miércoles: Vimos definiciones y ejemplos de clases y objetos, y discutimos cómo modelaríamos nosotros esos ejemplos.
  - Viernes: Discutimos cómo modelar con objetos el convertidor. Quedamos en hacer pruebas con el .tex de Pablo y escribir archivos .tex de prueba minimales.

## Septiembre

- Semana del 2:
  - Lunes:
    - Seguimos discutiendo el diseño del convertidor con objetos. Usaremos un árbol (parecido al del Document Object Model) como estructura intermedia del convertidor, el "árbol de estructura del documento".
    - Jimena se encargará de convertir del árbol a HTML y Erick de LaTeX al árbol. Joseph limpiará el LaTeX de Campero.
    - Definimos "documento limpio" como aquel que reconozca un convertidor. 
  - Miércoles:
    - Escribimos esta bitácora porque se nos había olvidado y tenemos el presentimiento de que Pablo está enojado con nosotros por no mandar avances.
    - Vimos la definición de tipo abstracto de dato y sus ventajas [Necaise].
    - Discutimos superficialmente el primer principio SOLID.
    - Acordamos que el primer paso para diseñar el convertidor es definir el árbol intermedio.
    - Podemos ver el árbol intermedio como dos estructuras distintas, un objeto "árbol ordenado" que tenga sus nodos ordenados, y cada nodo contiene objetos capítulo, sección, etc.
    - Discutimos si los párrafos deben ser nodos del árbol (como en el DOM) o información contenida en otros nodos, y no sabemos. Vamos a experimentar.
    - Revisamos el árbol de Ulam-Harris y las sucesiones de Prüfer como maneras, quizá complementarias, de identificar y ordenar los nodos.
  - Viernes:
    - Seguimos discutiendo la forma del árbol intermedio.
    - Tratamos de construir el árbol abstracto para un documento que teníamos.
    - Ese documento tenía inputs y no supimos qué hacer con ellos.
    - Pensamos que podíamos aplanar el árbol y convertirlo en una lista porque cada input no era necesariemente un árbol independiente.
    - También discutimos si los encabezados deberían tener la misma jerarquía que los párrafos, y al parecer si.
    - Una alternativa a la estructura final es una lista de listas.
- Semana del 9:
  - Lunes:
    - Quedamos en que una buena forma de tener un documento abstracto es tomar pares ordenados (texto, formato), y una lista de ellos. También pueden tener forma ((texto, formato), formato) o ((texto, texto, ...), formato), o combinaciones. Esto representa los ambientes definidos por el usuario. El formato podría ser un objeto cuyos atributos sean los parámetros del ambiente.
    - Martes:
      - Escribimos un cachito de prueba.tex en formato abstracto. A partir de ahora ya podremos trabajar por separado: una parte del equipo se encarga de convertir el .tex a un documento abstracto y la otra parte se encarga de convertir el documento abstracto a html.
      - TeX2AbsDoc: Un párrafo de texto debe estar escrito en una sola línea. Esta se dividirá en varios objetos de texto con formato, divididos al usar comandos dentro de la línea o texto plano. Los ambientes se dividirán en varias líneas. Queda la duda de cómo representar comandos dentro de comandos.
      - AbsDoc2HTML: Se definen funciones tales que cada una realice realice: lean el archivo en texto plano, identifiquen y asignen el formato correcto, iteren los formatos de ser necesario, excluyan los textos que no indican formato y los mande a <p>. Queda pendiente plantear las clases a utilizar y un archivo CSS que contenga los formatos.
