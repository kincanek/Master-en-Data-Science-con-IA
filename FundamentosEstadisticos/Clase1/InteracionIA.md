# Actividad: Exploración de Librerías con Meta AI

**A continuación se muestran las respuestas de META AI**



## ¿Cuáles son las 5 librerías de Python más importantes para un Científico de Datos y cuál es el rol principal de cada una dentro de un flujo de trabajo?



Las 5 librerías que verás en el 95% de los flujos de trabajo de Data Science son estas. Te las pongo en el orden en que típicamente aparecen en un proyecto:

### Las 5 esenciales para un Científico de Datos

| Librería        | Rol principal en el flujo de trabajo | ¿Para qué la usas exactamente?                                                                                                                                                                                                 |
| --------------- | ------------------------------------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| 1. Pandas       | Manipulación y análisis de datos     | Es tu navaja suiza. Cargas CSVs, Excel, SQL → limpias nulos, filtras filas, creas columnas, haces joins y agregaciones. Si los datos están en tablas, viven en un `DataFrame` de Pandas.                                       |
| 2. NumPy        | Cálculo numérico y álgebra lineal    | Es la base de casi todo lo demás. Maneja arrays multidimensionales súper rápidos. Pandas y Scikit-learn corren sobre NumPy. Lo usas para operaciones matemáticas, estadística, generar datos sintéticos y álgebra de matrices. |
| 3. Matplotlib   | Visualización base                   | Graficar para entender. Histogramas para distribuciones, scatter plots para correlaciones, line plots para series de tiempo. Es la librería más low-level: tú controlas cada detalle.                                          |
| 4. Seaborn      | Visualización estadística            | Se construye sobre Matplotlib pero hace gráficas estadísticas bellas con 1 línea. Heatmaps de correlación, boxplots, pairplots, barplots con intervalos de confianza. Ideal para EDA y comunicar insights.                     |
| 5. Scikit-learn | Machine Learning                     | Aquí entrenas los modelos. Regresión, clasificación, clustering, reducción de dimensionalidad, validación cruzada, pipelines, métricas. Todo con una API consistente: `.fit()` y `.predict()`.                                 |

### Cómo encajan en un flujo típico

1. Ingesta y limpieza → Pandas + NumPy: Lees los datos y los dejas listos. Tratas nulos, tipos de datos, outliers.
2. Análisis exploratorio EDA → Pandas + Seaborn + Matplotlib: Entiendes distribuciones, relaciones y problemas con `df.describe()`, `sns.heatmap(df.corr())`, `plt.hist()`.
3. Feature engineering → Pandas + NumPy: Creas variables nuevas, normalizas, haces encoding. NumPy acelera las operaciones matemáticas pesadas.
4. Modelado → Scikit-learn: Divides train/test, entrenas `RandomForestClassifier`, `LinearRegression`, haces GridSearch, validas con cross_val_score.
5. Comunicación → Seaborn + Matplotlib: Graficas resultados, feature importance, matriz de confusión para el reporte final.



## Explica detalladamente por qué es más eficiente utilizar arreglos de NumPy en lugar de listas nativas de Python cuando trabajamos con millones de datos. Menciona el concepto de 'vectorización'.



La diferencia entre NumPy y listas de Python con millones de datos es brutal: hablamos de 10x a 100x más rápido y usar hasta 5x menos memoria. La razón se resume en 3 conceptos: memoria contigua, tipos fijos y vectorización.

### 1. Cómo se guarda en memoria: contigua vs dispersa

Listas de Python  
Una lista de Python es un arreglo de *punteros* a objetos. Cada número es un objeto Python completo que vive en otra parte de la memoria.

Para `[1][2][3]` Python guarda:

- La lista: `[puntero_a_1, puntero_a_2, puntero_a_3]`
- Objeto 1: tipo, contador de referencias, valor 1 → ∼28 bytes
- Objeto 2: tipo, contador de referencias, valor 2 → ∼28 bytes
- Objeto 3: tipo, contador de referencias, valor 3 → ∼28 bytes

Total: ∼84+ bytes para 3 enteros + overhead de la lista.

Arreglos de NumPy  
Un `np.array([1][2][3], dtype=int32)` guarda todos los valores juntos en un bloque de memoria contiguo, sin objetos individuales.

`[ 00001 | 00000010 | 00000011 ]` → 12 bytes total

Con 1 millón de datos: lista ≈ 28 MB vs NumPy int32 ≈ 4 MB. 7x menos RAM.

### 2. Tipo fijo vs tipo dinámico

Las listas pueden mezclar tipos: `[1, "texto", 3.14, True]`. Por eso Python tiene que revisar el tipo de cada elemento en cada operación.

NumPy fuerza un solo `dtype`. Si dices `int32`, todos son `int32`. Esto permite que la CPU use instrucciones optimizadas y que no haya chequeo de tipos en tiempo de ejecución.

### 3. Vectorización: la razón principal de la velocidad

Vectorización es delegar el bucle a código C/Fortran pre-compilado en lugar de hacer el bucle en Python.

Mira este ejemplo: sumar 1 a 1 millón de números.



| Operación                    | Tiempo aprox  | Por qué                                                |
| ---------------------------- | ------------- | ------------------------------------------------------ |
| Lista con `for`              | 1.2 - 2.0 s   | Bucle Python + objetos individuales                    |
| Lista con list comprehension | 0.9 - 1.5 s   | Bucle Python optimizado pero sigue siendo interpretado |
| NumPy `a * b`                | 0.02 - 0.05 s | Bucle en C + memoria contigua + SIMD                   |



## Proporciona 3 ejemplos de funciones de NumPy que sean esenciales para realizar cálculos estadísticos básicos (como media o desviación estándar) y muestra cómo se aplicarían a un arreglo de una dimensión.



Aquí van 3 funciones de NumPy que usas todo el tiempo en estadística básica. Te pongo el ejemplo con un arreglo 1D para que quede claro:

```python
import numpy as np
# Nuestro arreglo de ejemplo: calificaciones de un examencalificaciones = np.array([7.5, 8.0, 6.5, 9.0, 8.5, 7.0, 10.0, 5.5, 8.0, 7.5])
```

### 1. `np.mean()` - Media o promedio

Para qué: Te da el valor central del conjunto de datos. Es la suma de todos / cantidad de elementos.

```python
promedio = np.mean(calificaciones)print(promedio)  # 7.75
# También funciona como método del arrayprint(calificaciones.mean())  # 7.75, mismo resultado
```

Cuándo usarla: Para reportar el valor "típico" cuando no hay outliers extremos.

### 2. `np.std()` - Desviación estándar

Para qué: Mide qué tan dispersos están los datos respecto a la media. Desviación baja = datos muy juntos. Alta = datos muy regados.

```python
desv_estandar = np.std(calificaciones)print(desv_estandar)  # 1.28127...
# Importante: por defecto NumPy usa N en el denominador, "población"# Si quieres la desviación muestral, usa ddof=1desv_muestral = np.std(calificaciones, ddof=1)print(desv_muestral)  # 1.35165...
```

Cuándo usarla: Para entender la variabilidad. Si la media es 7.75 y la desv. estándar es 1.28, la mayoría de notas están entre 6.47 y 9.03.

### 3. `np.median()` - Mediana

Para qué: El valor que queda justo a la mitad si ordenas todos los datos. No le afectan los outliers como a la media.

Python

```python
mediana = np.median(calificaciones)print(mediana)  # 7.75
# Ejemplo con outlier para ver la diferenciacon_outlier = np.array([7.5, 8.0, 6.5, 9.0, 8.5, 7.0, 10.0, 5.5, 8.0, 0.0])print(np.mean(con_outlier))    # 7.0, el 0.0 bajó el promedioprint(np.median(con_outlier))  # 7.75, la mediana casi no se movió
```

Cuándo usarla: Cuando tienes valores atípicos y quieres una medida de tendencia central más robusta.
