# Pregunta 1

**Si quiero mostrar la distribución de una variable en una y detectar valores atípicos, ¿por qué es mejor usar un Boxplot que un gráfico de barras tradicional? Explica las ventajas técnicas.**



Porque están diseñados para cosas opuestas. El gráfico de barras resume **un solo número** (normalmente la media o el conteo), el boxplot resume **cómo se distribuyen todos los datos**.

## Ventajas técnicas del boxplot

**1. Guarda el resumen de cinco números, no uno**

- Caja inferior = Q1 (percentil 25)
- Línea roja = mediana (percentil 50)
- Caja superior = Q3 (percentil 75)
- Bigotes = Q1 − 1.5×IQR y Q3 + 1.5×IQR
- Puntos fuera = outliers

Con eso ves rango, dispersión y posición central en un vistazo. Una barra solo te da $\bar{x}$ o suma, y pierdes toda la forma.

**2. Detecta atípicos con una regla objetiva**
El boxplot usa el rango intercuartílico:
$IQR = Q3 - Q1$

Cualquier valor $< Q1 - 1.5 \times IQR$ o $> Q3 + 1.5 \times IQR$ se marca automáticamente. No tienes que adivinar. El gráfico de barras no tiene ese mecanismo, el outlier se diluye en la media.

**3. Es robusto a extremos**
La mediana y los cuartiles no se mueven mucho si añades un valor de 200. La media de una barra sí, y te puede hacer creer que todo el grupo subió. Por eso en datos sesgados (salarios, tiempos de respuesta, ventas) el boxplot es más honesto.

**4. Te muestra asimetría y concentración**

- Caja larga = alta variabilidad
- Mediana pegada a Q1 = cola derecha larga
- Bigotes asimétricos = sesgo

Una barra es simétrica por diseño, no puede comunicar eso.

**5. Compara distribuciones, no solo promedios**
Si pones 3 boxplots lado a lado, ves al instante quién tiene más dispersión o más outliers, aunque las medias sean idénticas. Con 3 barras iguales pensarías que los grupos son iguales.

## Por qué la barra tradicional falla para esto

- **Agregación destructiva:** reduce n valores a 1. Pierdes varianza, curtosis, multimodalidad.
- **Dependencia de la media:** sensible a outliers, y oculta justo lo que quieres detectar.
- **No tiene escala de dispersión:** no hay forma estándar de dibujar IQR en una barra sin convertirla en otra cosa.
- **Asume normalidad implícita:** la gente interpreta la altura como "típico", pero si la distribución es bimodal, esa lectura es falsa.

## Resumen rápido

| Característica     | Boxplot                                        | Gráfico de barras                 |
| ------------------ | ---------------------------------------------- | --------------------------------- |
| Qué muestra        | Mediana, Q1, Q3, rango, outliers               | Media, suma o conteo              |
| Detecta atípicos   | Sí, con regla 1.5×IQR                          | No                                |
| Muestra dispersión | Sí                                             | No                                |
| Robusto a extremos | Sí                                             | No                                |
| Ideal para         | Análisis exploratorio de una variable continua | Comparar totales entre categorías |

Usa barra cuando quieras comparar cuántos o cuánto en categorías discretas. Usa boxplot cuando la pregunta es "¿cómo se distribuye esto y qué valores se salen de lo normal?" — que es exactamente tu caso.



---



# Pregunta 2

**¿Cuáles son las principales diferencias entre Matplotlib y Seaborn en términos de sintaxis y facilidad de uso para realizar un análisis de correlación bivariable?**



Para correlación bivariable, Matplotlib es como armar el gráfico con piezas sueltas, Seaborn es como pedir el kit ya armado. Ambos dibujan sobre el mismo motor, porque Seaborn está construido encima de Matplotlib, pero la sintaxis cambia por completo.



## 1. Sintaxis

**Matplotlib**

```python
import matplotlib.pyplot as plt
import numpy as np

# necesitas los arrays sueltos
plt.scatter(df['x'], df['y'], alpha=0.6)
r = np.corrcoef(df['x'], df['y'])[0,1]
plt.title(f'r = {r:.2f}')
plt.xlabel('x'); plt.ylabel('y')
plt.grid(True)
```

- Trabaja con vectores. Si usas DataFrame, tienes que extraer las columnas.
- Cada elemento se añade por separado: puntos, línea, texto, leyenda.

**Seaborn**

```python
import seaborn as sns

# trabaja directo con nombres de columnas
sns.regplot(data=df, x='x', y='y', ci=95)
# o para el gráfico completo:
sns.jointplot(data=df, x='x', y='y', kind='reg')
```

- Sintaxis declarativa: le dices qué variables, no cómo dibujarlas.
- Acepta `data=df` y entiende `x='x'`, `hue='categoria'` sin bucles.

## 2. Facilidad para análisis de correlación

| Tarea                          | Matplotlib                                     | Seaborn                                  |
| ------------------------------ | ---------------------------------------------- | ---------------------------------------- |
| Scatter básico                 | `plt.scatter(x, y)`                            | `sns.scatterplot(data=df, x='x', y='y')` |
| Añadir regresión               | Calcular con `np.polyfit`, luego `plt.plot`    | `sns.regplot(...)` lo hace solo          |
| Intervalo de confianza         | Tienes que calcularlo a mano                   | `ci=95` por defecto                      |
| Ver distribuciones marginales  | Crear 3 subplots manualmente                   | `sns.jointplot(kind='reg')`              |
| Colorear por tercera variable  | Bucle por grupo y `plt.scatter` cada uno       | `hue='grupo'` en una línea               |
| Matriz de correlación completa | `plt.imshow(df.corr())` + anotaciones manuales | `sns.heatmap(df.corr(), annot=True)`     |

## 3. Por qué Seaborn es más rápido para bivariable

1. **Estadística integrada.** `regplot`, `lmplot` y `jointplot` calculan Pearson/Spearman, ajustan la recta y dibujan el IC sin que escribas fórmulas.
2. **Manejo de DataFrames.** No necesitas `df['x'].values`. Seaborn infiere tipos, maneja NaN y etiquetas de ejes automáticamente.
3. **Estética por defecto.** Paletas, rejilla y tamaños están pensados para exploración, no para publicación final. Con Matplotlib partes de un lienzo en blanco.
4. **Una función = un análisis.** Para correlación bivariable sueles querer tres cosas: ver la nube, ver la tendencia, ver la fuerza. Seaborn te las da en `jointplot(kind='reg')`.

## 4. Cuándo Matplotlib sigue ganando

- Necesitas control total del pixel: anotaciones complejas, múltiples ejes, animaciones.
- Estás construyendo un gráfico que Seaborn no tiene.
- Quieres evitar dependencias y tu análisis es solo `scatter`.

En la práctica, la mayoría hace esto: usa Seaborn para explorar la correlación en 2 líneas, y si necesita ajustar detalles finos, toma el objeto `ax` que Seaborn devuelve y lo retoca con Matplotlib.

```python
g = sns.jointplot(data=df, x='x', y='y', kind='reg')
g.ax_joint.set_title('Correlación x-y', pad=40)  # aquí ya es Matplotlib puro
```

Resumen: para correlación bivariable, Seaborn te ahorra 5 a 10 líneas de código por gráfico, reduce errores de cálculo y te da contexto estadístico inmediato. Matplotlib te da libertad absoluta, pero pagas con verbosidad.

---



# Pregunta 3

**Dame 3 ejemplos de cómo se pueden 'manipular' visualmente los datos para engañar a una audiencia en una presentación y cómo puedo evitar cometer estos errores en mi proyecto de Data Science** 



Manipular no siempre es mentir con números, muchas veces es mentir con la forma en que los dibujas. En Data Science estos tres son los clásicos que aparecen en presentaciones y que arruinan la confianza.

### 1. Recortar el eje Y para inflar una diferencia pequeña

**Cómo se hace:** pones la barra o la línea a empezar en 90 en vez de 0. Una subida de 95 a 100 parece que se duplica.



Izquierda: parece que B es el doble de A. Derecha: ves que la diferencia real es 5%.

**Por qué engaña:** nuestro cerebro compara alturas, no lee los números del eje. Si quitas la base, amplificas ruido.

**Cómo evitarlo en tu proyecto:**

- Barras y columnas: eje Y siempre desde 0. Si necesitas zoom, usa un gráfico de puntos o muestra el cambio porcentual al lado, no recortes.
- Si recortas por necesidad (series temporales con poca variación), añade una ruptura visual clara en el eje y anota "eje truncado".
- En código: `ax.set_ylim(0, None)` en Matplotlib, o deja que Seaborn lo haga por defecto.

### 2. Doble eje Y con escalas elegidas a mano

**Cómo se hace:** graficas dos variables con escalas distintas para que las líneas coincidan y sugerir correlación.



Aquí ventas suben 10% en 6 años y temperatura fluctúa. Ajustando los límites (99-111 vs 14-29) parecen moverse juntas.

**Por qué engaña:** puedes forzar cualquier parecido cambiando el mínimo y máximo de cada eje. La audiencia asume causalidad.

**Cómo evitarlo:**

- No uses doble eje para comparar magnitudes. Si necesitas mostrar dos series, normalízalas a índice base 100 o usa paneles separados con la misma escala temporal.
- Reporta la correlación real: `df[['ventas','temp']].corr()` y muestra el coeficiente, no solo las líneas.
- Si el stakeholder insiste en doble eje, fija ambos ejes con rangos significativos y añade la correlación y p-value en el título.

### 3. Distorsión por área, volumen o perspectiva 3D

**Cómo se hace:** pastel en 3D, burbujas sin escalar por área, pictogramas donde el dibujo crece en alto y ancho.



Izquierda: con ángulo y "explosión", la porción B parece más grande que C aunque son 30% vs 25%. Derecha: vista plana, proporciones correctas.

**Por qué engaña:** percibimos área, no ángulo. En 3D la parte frontal ocupa más píxeles.

**Cómo evitarlo:**

- Nunca uses gráficos 3D para proporciones. Usa barra horizontal ordenada.
- Para burbujas: escala el radio con raíz cuadrada del valor, porque `área = πr²`. En Matplotlib: `s = valor * factor`, no `s = valor`.
- Limita los pasteles a máximo 3 categorías. Si hay más, cambia a barra.
- Evita iconos que crecen en dos dimensiones a la vez.

---

## Checklist rápido para no caer

1. **Muestra el contexto completo.** Antes de exportar, pregunta: ¿qué vería alguien que no conoce el proyecto? Añade cero, muestra rango completo, incluye N.
2. **Documenta transformaciones.** En tu notebook deja una celda con "escala usada, filtros aplicados, outliers eliminados". Facilita auditoría.
3. **Usa métricas, no solo imágenes.** Acompaña cada gráfico de correlación con r y p, cada comparación con diferencia absoluta y relativa.
4. **Revisa con el "test del titular".** Si tu gráfico fuera un titular de periódico, ¿sería honesto? Si no, rehazlo.
5. **Pide revisión ciega.** Pasa el gráfico sin título a un compañero. Si interpreta algo distinto a tu conclusión, la visualización está manipulando.

La regla de oro en Data Science no es "hazlo bonito", es "hazlo reproducible y difícil de malinterpretar". Si sigues esas tres trampas al revés — eje completo, escala única y representación plana — tu audiencia confiará más en el análisis que en el diseño.


