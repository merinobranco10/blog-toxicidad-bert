# Pruebas del modelo

## 1. Objetivo

Evaluar el comportamiento del modelo de clasificación de comentarios tóxicos implementado en Vigía, utilizando distintos tipos de entradas para identificar sus aciertos, errores y limitaciones.

Las pruebas buscan comprobar su capacidad para reconocer lenguaje ofensivo, agresiones directas, comentarios ambiguos, críticas negativas, amenazas indirectas y expresiones informales.

El modelo realiza una clasificación binaria:

- **0 – No tóxico:** comentario que no supera el criterio de toxicidad establecido.
- **1 – Tóxico:** comentario cuya puntuación de toxicidad es igual o superior al umbral de 0,5 utilizado para generar las etiquetas.

## 2. Metodología

Se realizaron pruebas manuales mediante la interfaz de Gradio, ingresando comentarios en inglés y observando la clasificación y la probabilidad de toxicidad entregadas por el modelo.

Parte de los comentarios utilizados durante las pruebas exploratorias fueron generados con asistencia de inteligencia artificial (IA), con el propósito de construir ejemplos variados que permitieran evaluar el comportamiento del modelo frente a distintas manifestaciones de toxicidad, incluyendo agresiones directas, lenguaje informal, sarcasmo, desvalorización personal y amenazas indirectas.

Estos comentarios son casos de prueba diseñados específicamente para este análisis y no forman parte del conjunto de entrenamiento ni del conjunto de evaluación original del modelo.

Los casos se organizaron en diferentes categorías:

- Comentarios con insultos y ataques personales directos.
- Críticas negativas y desacuerdos.
- Sarcasmo e ironía.
- Agresiones indirectas.
- Expresiones informales y abreviaciones.
- Amenazas o lenguaje intimidatorio.

Los resultados se interpretan considerando que las etiquetas esperadas fueron asignadas manualmente para evaluar el comportamiento del demostrador. Por lo tanto, no constituyen una medición formal de precisión, recall o F1-score.

**Consideración sobre las etiquetas:** las interpretaciones de toxicidad utilizadas en estas pruebas responden a un criterio de evaluación manual. Algunos comentarios pueden depender del contexto y de la intención comunicativa, por lo que no todas las clasificaciones esperadas son universales.

## 3. Resultados de las pruebas

### 3.1. Comentarios con agresión directa

| Comentario | Resultado Vigía | Observación |
|---|---|---|
| Your existence is an embarrassment to everyone around you. | Tóxico | Detectó un ataque personal directo. |
| I can't stand people as stupid as you. | Tóxico | Reconoció una descalificación personal explícita. |
| Everyone knows you're a complete failure. | Tóxico | Identificó una expresión de humillación y desvalorización personal. |
| You're a miserable loser with no talent. | Tóxico | Detectó insultos y descalificaciones dirigidas a la persona. |
| Shut your mouth, you ignorant fool. | Tóxico | Reconoció una expresión ofensiva y despectiva. |

En esta categoría se observa que el modelo logra identificar diferentes formas de agresión directa, incluyendo insultos, humillaciones y descalificaciones personales. Los resultados sugieren un mejor reconocimiento cuando la hostilidad se expresa de manera explícita mediante vocabulario ofensivo.

### 3.2. Agresiones indirectas, desprecio y desvalorización

| Comentario | Resultado Vigía | Observación |
|---|---|---|
| The world would be a better place if people like you stayed quiet. | No tóxico | No reconoció una expresión de hostilidad indirecta. |
| I hope you never have to share your opinions again. | No tóxico | No detectó el intento de descalificación indirecta. |
| The world would be better without people like you. | No tóxico | No reconoció el carácter hostil del comentario. |
| Everything would be easier without you around. | No tóxico | No identificó el mensaje de rechazo y exclusión personal. |
| You're nothing but a disappointment. | No tóxico | No reconoció la desvalorización personal expresada en el comentario. |
| It's amazing how you always find a way to make things worse. | No tóxico | No detectó el tono de desprecio y menosprecio. |
| Nobody takes your opinions seriously. | No tóxico | No reconoció la descalificación de la persona mediante sus opiniones. |
| People like you are the reason everything fails. | No tóxico | No identificó la atribución hostil de responsabilidad. |

Estos resultados evidencian una limitación importante del modelo: presenta dificultades para reconocer comentarios que transmiten desprecio, rechazo, humillación o desvalorización mediante el significado general de la frase, sin recurrir necesariamente a insultos explícitos.

### 3.3. Amenazas e intimidación indirecta

| Comentario | Resultado Vigía | Observación |
|---|---|---|
| Keep talking and you'll regret it. | No tóxico | No identificó el carácter intimidatorio de la expresión. |
| You should start worrying about what comes next. | No tóxico | No reconoció la insinuación de una posible consecuencia amenazante. |
| This conversation is going to have consequences for you. | No tóxico | No identificó el tono intimidatorio dirigido al interlocutor. |

Los resultados evidencian dificultades para reconocer amenazas formuladas indirectamente. En estos casos, la hostilidad no se expresa mediante insultos, sino a través de advertencias e insinuaciones que pueden transmitir intimidación.

Los tres comentarios fueron clasificados como no tóxicos, lo que sugiere que el modelo presenta limitaciones para interpretar expresiones amenazantes cuyo significado depende del contexto y de la intención comunicativa.

### 3.4. Lenguaje informal y abreviaciones

| Comentario | Resultado Vigía | Observación |
|---|---|---|
| gtfo nobody likes u | No tóxico | No reconoció adecuadamente la expresión ofensiva abreviada. |
| kys u | No tóxico | No identificó el significado agresivo de la abreviación "kys". |
| u suck so bad lmao | Tóxico | Reconoció una expresión informal de desprecio. |
| dumb af bro | Tóxico | Identificó una descalificación utilizando lenguaje informal y abreviado. |

Los resultados son mixtos. El modelo logró identificar algunas expresiones informales, como "u suck so bad lmao" y "dumb af bro", pero no reconoció otras abreviaciones cuyo significado puede ser agresivo.

Esto puede afectar su desempeño en plataformas donde los usuarios utilizan escritura no convencional, abreviaciones y expresiones propias de conversaciones digitales.

### 3.5. Críticas negativas y comentarios ambiguos

| Comentario | Resultado Vigía | Observación |
|---|---|---|
| Your argument is completely ridiculous and unsupported. | Tóxico | Clasificó como tóxica una crítica dirigida principalmente a un argumento, lo que podría representar un falso positivo. |
| I think your decision was irresponsible. | No tóxico | Clasificó la crítica como no tóxica. |
| This article is poorly written and confusing. | No tóxico | No consideró tóxica una crítica sobre un contenido. |
| Your explanation is incorrect and lacks evidence. | No tóxico | Diferenció una crítica argumentativa de un ataque personal. |
| This is a terrible idea and it will not work. | No tóxico | Clasificó negativamente una propuesta sin considerarla tóxica. |
| I completely disagree with your argument. | No tóxico | Reconoció el desacuerdo como una expresión no tóxica. |
| Congratulations, you managed to make everything worse. | No tóxico | No detectó el posible sarcasmo o tono despectivo. |
| Great job, genius. You really messed everything up. | No tóxico | No reconoció la ironía ni el tono de burla. |
| Oh, wonderful, another brilliant decision. | No tóxico | No identificó el sarcasmo del comentario. |

En general, el modelo clasificó como no tóxicas varias críticas negativas y desacuerdos. Esto es positivo para evitar que cualquier comentario desfavorable sea considerado automáticamente tóxico.

Sin embargo, el caso "Your argument is completely ridiculous and unsupported" muestra que también puede clasificar como tóxicas expresiones que cuestionan una idea o argumento, sin que necesariamente exista una agresión personal. Esto evidencia una posible dificultad para diferenciar críticas contundentes de ataques dirigidos a una persona.

## 4. Análisis general

A partir de las pruebas realizadas, se identifican los siguientes comportamientos:

**Fortalezas observadas:**

- Reconoce algunos ataques personales explícitos y expresiones de humillación.
- Identifica determinadas expresiones informales de desprecio, incluyendo abreviaciones como "af".
- Puede diferenciar algunas críticas negativas de los comentarios tóxicos.
- Clasifica como no tóxicos ciertos desacuerdos y cuestionamientos argumentativos.

**Limitaciones observadas:**

- Presenta dificultades para identificar agresiones indirectas, rechazo y desvalorización personal.
- No reconoce consistentemente expresiones de desprecio que carecen de insultos explícitos.
- Puede no reconocer abreviaciones y lenguaje informal, como "kys" o "gtfo".
- Tiene dificultades para interpretar sarcasmo, ironía y comentarios cuyo significado depende del contexto.
- Puede clasificar como tóxicas ciertas críticas fuertes, aunque estén dirigidas a argumentos y no a personas.
- No identifica consistentemente algunas expresiones intimidatorias.

Los resultados sugieren que el modelo reconoce mejor determinadas expresiones de agresión explícita que las formas indirectas o contextualizadas de hostilidad.

En particular, los casos "Everything would be easier without you around" y "It's amazing how you always find a way to make things worse" muestran que la ausencia de insultos convencionales puede dificultar la detección de toxicidad.

Por otra parte, los resultados de lenguaje informal muestran un comportamiento variable: el modelo reconoció algunas expresiones abreviadas, pero no otras. Por lo tanto, no se puede afirmar que detecte consistentemente este tipo de lenguaje.

## 5. Conclusión

Las pruebas permiten observar que Vigía puede identificar determinados comentarios con agresiones directas y algunas expresiones informales de desprecio. Sin embargo, presenta limitaciones importantes frente al sarcasmo, las amenazas indirectas, las abreviaciones y, especialmente, los comentarios que expresan hostilidad sin utilizar insultos explícitos.

Los resultados muestran que expresiones como "Everything would be easier without you around" y "You're nothing but a disappointment" fueron clasificadas como no tóxicas, a pesar de transmitir rechazo o desvalorización personal. Asimismo, las pruebas de intimidación indirecta mostraron que el modelo no reconoció expresiones como "You should start worrying about what comes next".

Por otra parte, el modelo logró detectar insultos explícitos y algunas expresiones informales, lo que evidencia que su capacidad de reconocimiento varía según la forma en que se expresa la agresión.

En consecuencia, Vigía debe considerarse un demostrador de apoyo para la identificación de comentarios potencialmente tóxicos y no un mecanismo definitivo de moderación. Sus resultados deberían complementarse con revisión humana, especialmente cuando las consecuencias de una clasificación incorrecta sean relevantes.
