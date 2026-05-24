**Explica cuándo es preferible utilizar la Mediana en lugar de la Media en una distribución de datos para reportar resultados y por qué.**



La mediana gana cuando un solo valor extremo puede secuestrar el promedio.

Ambas miden el centro, pero lo hacen con reglas distintas:

- **Media** ($\bar{x}$): suma todo y divide. Minimiza la suma de errores al cuadrado, por eso cada valor tira de ella con fuerza proporcional a su distancia.
- **Mediana**: el valor que deja 50% de los datos por debajo y 50% por arriba. Minimiza la suma de errores absolutos, por eso solo le importa el orden, no la magnitud.

Esa diferencia explica por qué, en ciertos contextos, reportar la mediana es más honesto.

## Cuándo preferir la mediana

### 1. Distribuciones sesgadas

Cuando la cola se estira mucho hacia un lado, la media se va con la cola.

- **Ingresos en Texcoco o en México en general**: la mayoría gana entre $8,000 y $15,000 MXN, pero unos pocos ganan $200,000. La media puede decir $22,000, la mediana dirá $12,500. La segunda describe mejor al trabajador típico.
- **Precios de vivienda**: un par de desarrollos de lujo en el Estado de México suben la media, pero no cambian la mediana.

En sesgo a la derecha (lo más común), media > mediana. En sesgo a la izquierda (ej. edad de jubilación obligatoria), media < mediana.

### 2. Presencia de outliers o errores de medición

La mediana es robusta: puedes multiplicar el valor más grande por 10 y la mediana no se mueve.

Ejemplo simple con cinco sueldos:

- Datos: 10, 12, 13, 14, 100
- Media: 29.8
- Mediana: 13

Si el 100 era un error de captura, la media miente, la mediana sigue contando la historia del grupo.

Por eso se usa en tiempos de respuesta de servidores, latencias de apps, o tiempos de espera en hospitales: un solo caso atascado no debería definir el servicio.

### 3. Datos ordinales o escalas no equidistantes

No puedes promediar "muy insatisfecho, neutral, muy satisfecho" como si fueran números exactos. La mediana sí tiene sentido porque respeta el orden: "la respuesta típica fue neutral".

### 4. Muestras pequeñas o colas pesadas

En n=20 encuestas de satisfacción de un restaurante local, dos críticas extremas arrastran la media. La mediana te da el cliente del medio, que es más estable para decidir si cambiar el menú.

### 5. Cuando quieres comunicar "la persona típica"

La mediana responde a la pregunta que la gente realmente hace: "¿qué le pasa a alguien en el medio?". La media responde a "si repartiéramos todo en partes iguales, ¿cuánto tocaría?". Son preguntas distintas.

## ¿Y cuándo la media sí es mejor?

Si la distribución es aproximadamente simétrica, sin outliers, y te interesa el total acumulado, la media gana. Por ejemplo, consumo promedio de agua por hogar para planear infraestructura: necesitas la suma total, no el hogar mediano.

## Buena práctica para reportar

En trabajo real, reporta ambas y mira la diferencia:

- Si media ≈ mediana: distribución simétrica, usa cualquiera.
- Si media >> mediana: cola derecha, informa la mediana como "valor típico" y la media como "promedio afectado por valores altos".
- Añade percentiles (p25, p75) para mostrar dispersión sin depender de la desviación estándar.

En resumen, usa la mediana cuando tus datos tienen asimetría, extremos, orden pero no intervalo, o cuando quieres proteger tu resumen de que un solo valor cuente más que todos los demás.

---

**¿Cómo se relaciona un histograma, un gráfico de caja y la visualización de la desviación estándar con un gráfico de dispersión para el análisis de univariable?**



En análisis univariable todos miran la misma columna, solo cambian el nivel de zoom. Histograma, caja, media ± desviación estándar y el gráfico de puntos (el primo univariable del "dispersión") son cuatro formas de leer la distribución sin inventar una segunda variable.

Primero aclaremos el término: un gráfico de dispersión clásico es bivariable, x contra y. Para una sola variable usamos su versión simple, el strip plot o dot plot: cada observación es un punto alineado sobre un eje, a veces con un poco de jitter para que no se encimen. Funciona como la materia prima de los otros tres.

## Qué aporta cada uno

### Histograma

- Agrupa los valores en bins y cuenta frecuencias.
- Te muestra forma: sesgo a la derecha, bimodalidad, huecos, colas pesadas.
- Es sensible al ancho del bin, pero es el único que deja ver la densidad real.

### Gráfico de caja (box plot)

- Resume cinco números: mínimo no-atípico, Q1, mediana, Q3, máximo no-atípico. Los puntos fuera son outliers.
- No asume simetría. Te dice dónde está el 50% central (la caja = IQR) y qué tan lejos llegan los bigotes.
- Oculta la forma interna: dos picos iguales y una distribución uniforme pueden dar la misma caja.

### Media ± desviación estándar

- Se visualiza como una barra de error, un punto con bigotes, o una curva normal superpuesta al histograma.
- Resume dispersión alrededor de la media: $ \bar{x} \pm s $.
- Asume que la media tiene sentido. En datos sesgados, ese intervalo puede caer en zonas donde casi no hay datos.

### Strip plot / dot plot univariable

- No resume, muestra. Ves n, empates, granularidad (¿son enteros?, ¿hay redondeo?), y valores extremos reales.
- Es ruidoso con miles de puntos, pero es la prueba de honestidad: si el histograma dice "normal" y el strip muestra dos nubes separadas, confía en el strip.

## Cómo se conectan entre sí

Piensa en capas de la misma distribución empírica:

1. **Datos crudos → strip plot.** Es la lista ordenada puesta en vertical.
2. **Conteo por intervalos → histograma.** Tomas el strip y lo apilas en cubetas.
3. **Cuantiles → box plot.** Tomas el strip, lo ordenas y marcas los percentiles 25, 50, 75.
4. **Momentos → media y sd.** Tomas el strip, calculas $\bar{x}$ y $s$, y los dibujas como centro y radio.

Por eso se complementan:

- El histograma te avisa de sesgo; el box te dice cuánto se mueve la mediana respecto a los cuartiles; la media ± sd te dirá si ese sesgo está inflando el promedio.
- Si histograma es bimodal pero el box parece normal, necesitas el strip para ver que hay dos grupos mezclados.
- Si media y mediana coinciden pero la sd es grande, el histograma te dirá si es por colas simétricas o por outliers que el box marcará como puntos sueltos.

## Mini-guía práctica

| Pregunta                                               | Mira primero                                                           |
| ------------------------------------------------------ | ---------------------------------------------------------------------- |
| ¿Hay sesgo o dos modas?                                | Histograma + strip                                                     |
| ¿Dónde está el típico y qué tan disperso es el centro? | Box plot (mediana, IQR)                                                |
| ¿Cuánto influyen los extremos en el promedio?          | Compara media vs mediana, y dibuja $\bar{x} \pm s$ sobre el histograma |
| ¿Tengo pocos datos o valores repetidos?                | Strip plot                                                             |

Para análisis univariable serio, la combinación más robusta es histograma con la curva de densidad, un box plot alineado debajo, y los puntos individuales con jitter. La media y su desviación estándar van encima solo como referencia, no como resumen único.

Si lo aplicas a algo como ingresos en Texcoco, verás: histograma con cola larga a la derecha, box con mediana mucho más baja que el bigote superior, media desplazada hacia la cola, y strip mostrando la nube densa de sueldos bajos con unos pocos puntos aislados arriba. Esa lectura conjunta evita reportar un "promedio" que nadie gana.





---



**¿Cómo un gráfico de calor multivariable ayuda a determinar la mejor correlación entre las mismas variables de una tabla?** 



Un mapa de calor no crea correlaciones nuevas, solo te deja ver de un vistazo cuáles pares de columnas se mueven juntos. Es la versión visual de la matriz de correlación, y por eso es tan útil cuando tienes la misma tabla con 5, 20 o 100 variables.



En el ejemplo, cada celda es el coeficiente $r$ de Pearson entre dos variables. Rojo intenso = correlación positiva fuerte, azul intenso = negativa fuerte, tonos pálidos = cerca de cero.

## Por qué el ojo gana a la tabla

Una tabla de números te obliga a comparar 10, 45 o 495 valores uno por uno. El mapa de calor convierte magnitud en color y signo en tono:

- **Intensidad**: mientras más saturado, mayor $|r|$.
- **Dirección**: cálidos para $r>0$, fríos para $r<0$.
- **Estructura**: la diagonal siempre es 1, la matriz es simétrica, así que solo necesitas la mitad.

En la imagen, sin leer todos los decimales, detectas inmediatamente:

- Ingreso–Gasto $r=0.85$ es el rojo más fuerte fuera de la diagonal.
- Ingreso–Años_educ $r=0.79$ le sigue.
- Edad casi no se mueve con nadie (celdas gris claro, $|r|<0.15$).

Eso responde a "¿cuál es la mejor correlación?" en dos segundos.

## Cómo usarlo para elegir

La "mejor" depende de tu objetivo, el mapa te ayuda en los tres casos típicos:

### 1. Para predicción

Busca el $|r|$ más alto con tu variable objetivo, pero evita duplicados. Aquí, si quieres predecir Ahorro, Ingreso ($0.70$) es mejor que Años_educ ($0.54$). Sin embargo, Ingreso y Gasto están muy correlacionados entre sí ($0.85$), así que meter ambos en un modelo lineal te dará multicolinealidad. El mapa te muestra ese bloque rojo y te avisa: elige uno.

### 2. Para exploración

Ordena las variables por clustering jerárquico (la mayoría de librerías lo hace automático). Los bloques de color revelan familias: en el ejemplo, Educación, Ingreso, Gasto y Ahorro forman un cluster socioeconómico, Edad queda aislada.

### 3. Para depuración

Un $r$ alto inesperado suele ser error de datos o fuga de información. Si vieras $r=0.99$ entre dos columnas que no deberían relacionarse, el rojo chillón te obliga a revisar antes de modelar.

## Lo que el mapa no te dice y debes verificar

- **No es causalidad.** Ingreso y Gasto se mueven juntos, pero el mapa no dice quién causa a quién.
- **Asume linealidad si usas Pearson.** Para relaciones monótonas pero curvas, usa Spearman y haz otro mapa; los colores cambian.
- **Outliers inflan $r$.** Un punto extremo puede pintar una celda de rojo. Siempre abre el scatter plot del par más fuerte para confirmar que no es un artefacto.
- **Significancia.** Con $n$ pequeño, un $r=0.6$ puede no ser significativo. El color no lo sabe; complementa con p-valores o intervalos.

## Flujo práctico

1. Calcula la matriz con el coeficiente adecuado (Pearson para continuas normales, Spearman para ordinales o sesgadas).
2. Dibuja el heatmap con anotaciones.
3. Identifica los 3 a 5 pares con mayor $|r|$.
4. Valida cada uno con histograma + scatter, como vimos antes, para ver forma y outliers.
5. Decide: ¿te quedas con la variable más explicativa y descartas su gemela correlacionada?

Así, el mapa de calor multivariable funciona como radar: no elige por ti, pero te señala en qué esquinas de la tabla vale la pena enfocar la lupa.
