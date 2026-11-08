# Notebooks del proyecto

Notebooks desarrollados en Google Colab (GPU T4) que dan origen al modelo usado
en el blog de moderación. **No son necesarios para ejecutar el blog**: la app
descarga el modelo directamente desde Hugging Face. Se incluyen como evidencia de
datos, entrenamiento, validación y decisiones.

| Notebook | Contenido |
|---|---|
| `T04_D03_Equipo_MerinoBranco_DiazMatias.ipynb` | Preparación de datos, entrenamiento y comparación de modelos |
| `T03_D03_Equipo_MerinoBranco_DiazMatias.ipynb` | Integración del modelo en una aplicación (inferencia, validación de entradas, interfaz) |

El orden lógico es **T04 primero** (genera el modelo) y **T03 después** (lo usa).

---

## T04: Pipeline de datos y entrenamiento

**Objetivo:** preparar los datos de Civil Comments y entrenar/comparar modelos
para clasificar comentarios como tóxicos o no tóxicos.

**Qué hace, en orden:**
1. Carga 50.000 filas del split `train` de `google/civil_comments` (semilla 42).
2. Diagnóstico de calidad: tipos, faltantes, vacíos, duplicados y rango de `toxicity`.
3. Limpieza: elimina espacios, textos vacíos, puntuaciones inválidas y 75 textos repetidos (quedan 49.925).
4. Etiqueta binaria: `toxico = 1` si `toxicity >= 0.5`.
5. Partición estratificada 70/15/15 (entrenamiento / validación / prueba) con control de que no haya textos compartidos.
6. Bitácora de decisiones y controles (`bitacora_pipeline.csv`).
7. Modelos: TF-IDF + Regresión Logística y BERT (`google-bert/bert-base-uncased`).
8. Baseline mayoritario (`DummyClassifier`) como referencia.
9. Comparación final y guardado de los modelos en `modelos_toxicidad.zip`.

**Resultados en el conjunto de prueba:**

| Modelo | Accuracy | F1 macro | F1 tóxicos |
|---|---|---|---|
| Baseline mayoritario | 0.9210 | 0.4794 | 0.0000 |
| TF-IDF + Reg. Logística | 0.8896 | 0.7082 | 0.4782 |
| BERT | 0.9424 | 0.8043 | 0.6399 |

**Salidas generadas:**
- `bitacora_pipeline.csv`
- `modelos_toxicidad.zip` (contiene `modelo_bert_toxicidad/` y `modelo_tfidf_toxicidad/`)

**Cómo ejecutarlo:**
1. Abrir en Google Colab y activar GPU (Entorno de ejecución → Cambiar tipo → T4).
2. Ejecutar **todas las celdas en orden**. Requiere conexión a internet para descargar el dataset y BERT.
3. El entrenamiento de BERT tarda unos 37 minutos en T4 (5 épocas).
4. Al final se descarga `modelos_toxicidad.zip`.

---

## T03: Integración del modelo con una aplicación

**Objetivo:** usar el modelo BERT ya entrenado (sin reentrenar) dentro de una
función de inferencia con validación de entradas e interfaz de prueba.

**Qué hace:**
1. Carga el modelo y el tokenizador desde el ZIP, en modo `eval()` y sin gradientes.
2. Define el contrato de entrada y salida (campos, tipos y reglas).
3. Valida entradas: separa **errores** (vacío, tipo incorrecto, sin letras, muy corto o largo; el modelo no se ejecuta) de **advertencias** (texto en español o truncado; el modelo sí se ejecuta).
4. Función `predecir()` que devuelve etiqueta, probabilidad, confianza, umbral, advertencias y limitación.
5. Casos de prueba: válidos, inválidos y con advertencia.
6. Control de que la inferencia no modifica los pesos (suma de verificación antes y después).
7. Diagrama de arquitectura (`diagrama_arquitectura_T03.png`).
8. Interfaz web básica con Gradio (Vigía) para probar el modelo.

**Requisito previo:** tener el ZIP generado por T04.

**Cómo ejecutarlo:**
1. Abrir en Google Colab (GPU opcional; con CPU funciona más lento).
2. Subir `modelos_toxicidad.zip` a `/content`. Si no está, la celda 2 abre un selector para subirlo.
3. Ejecutar todas las celdas en orden.
4. La interfaz Gradio (sección 9) se abre en la misma sesión de Colab.

> La lógica de `predecir()` y la validación de este notebook es la que se adaptó
> en `moderador.py` de la raíz del repositorio.

---

## Dependencias

`transformers`, `torch`, `accelerate`, `datasets`, `pandas`, `numpy`,
`scikit-learn`, `matplotlib`, `gradio` (solo T03, interfaz). En Colab se instalan
con la primera celda de cada notebook.

## Limitaciones

- Modelo entrenado solo con inglés; en español su fiabilidad es nula.
- Clase tóxica minoritaria (~7,9 %): hay falsos positivos.
- La etiqueta binaria depende del umbral 0,5, elegido por el equipo.
- Resultados verificables solo si se re-ejecuta el notebook completo; el entrenamiento puede variar levemente entre ejecuciones.

## Uso de IA generativa

Se usaron herramientas de IA generativa (ChatGPT en T04, Claude en T03) para
estructurar y redactar partes del código y las explicaciones. El equipo ejecutó
los notebooks, revisó las salidas y es responsable del contenido.
