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
    - Acordamos que el primer paso para diseñar el convertidor es definir el árbol intermedio.
    - Podemos ver el árbol intermedio como dos estructuras distintas, un objeto "árbol ordenado" que tenga sus nodos ordenados, y cada nodo contiene objetos capítulo, sección, etc.
    - Discutimos si los párrafos deben ser nodos del árbol o información contenida en otros nodos, y no sabemos. Vamos a experimentar.
    - Revisamos el árbol de Ulam-Harris y las sucesiones de Prüfer como maneras, quizá complementarias, de identificar y ordenar los nodos.
