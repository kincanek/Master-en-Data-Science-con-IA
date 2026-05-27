# Pregunta 1

**¿En qué se diferencia la estadística descriptiva con la estadística inferencial?, ¿Qué papel juega el aprendizaje estadístico dentro de la inferencia?**

La estadística descriptiva mira el dato que ya tienes; la inferencial usa ese dato para hablar del mundo que no mediste.

## Estadística descriptiva: qué pasó aquí

Trabaja solo con la muestra observada. No generaliza, no apuesta. Su tarea es resumir y hacer legible.

- **Herramientas típicas**: media, mediana, moda, varianza, percentiles, tablas de frecuencia, histogramas, boxplots, correlaciones muestrales.
- **Pregunta que responde**: ¿cómo se distribuyen mis ventas de abril en Texcoco? ¿qué tan dispersos están los tiempos de entrega?
- **No hay incertidumbre formal**: si calculas que el ticket promedio fue \$312, ese número es correcto para esos datos. No dice nada sobre otros meses ni otras sucursales.

Es el paso obligatorio antes de cualquier modelo. Si no entiendes la forma, los atípicos y las escalas, la inferencia posterior será frágil.

## Estadística inferencial: qué puedo decir allá afuera

Parte de una muestra y, asumiendo un mecanismo de muestreo, saca conclusiones sobre una población o proceso no observado.

- **Herramientas típicas**: estimadores puntuales, intervalos de confianza, pruebas de hipótesis, modelos paramétricos, distribuciones muestrales.
- **Pregunta que responde**: con 200 clientes encuestados, ¿cuál es el gasto promedio real de todos los clientes, y con qué margen de error? ¿la nueva campaña realmente aumentó la conversión o fue azar?
- **La clave es la incertidumbre**: cuantifica el error por muestreo. Habla en probabilidades, no en certezas.

|          | Descriptiva               | Inferencial                            |
| -------- | ------------------------- | -------------------------------------- |
| Alcance  | Solo los datos observados | Población o proceso subyacente         |
| Objetivo | Resumir                   | Estimar, probar, predecir con garantía |
| Producto | Número o gráfico          | Estimación + medida de error           |

## ¿Dónde entra el aprendizaje estadístico?

El aprendizaje estadístico es inferencia, pero cambia el foco. La inferencia clásica pregunta por parámetros interpretables: mu, beta, diferencia de medias. El aprendizaje estadístico pregunta por funciones: ¿qué f(X) predice mejor Y, y cuánto me equivoco fuera de la muestra?

Juega tres papeles dentro de la inferencia moderna:

1. **Amplía el objeto de inferencia.** En vez de estimar un solo coeficiente, estimas toda una superficie de predicción. La teoría del sesgo-varianza reemplaza al p-valor como brújula: controlas complejidad para que el error en datos nuevos sea bajo.

2. **Da herramientas cuando la dimensión crece.** Con 50 variables y 500 observaciones, los intervalos clásicos colapsan. Regularización como lasso o ridge, árboles, boosting, redes, hacen inferencia posible al imponer estructura y luego validar con datos no vistos mediante cross-validation o bootstrap.

3. **Reformula la incertidumbre.** Además de intervalos de confianza para parámetros, ofrece:
   
   - intervalos de predicción conformes, que garantizan cobertura sin asumir normalidad
   - importancia de variables y SHAP para entender qué impulsa f
   - inferencia post-selección y double machine learning, que combinan modelos flexibles con pruebas válidas sobre efectos causales

En la práctica, piénsalo así: la descriptiva te dice que el tiempo promedio de entrega fue 38 minutos. La inferencial clásica te da un intervalo de 35 a 41 minutos para la ciudad entera. El aprendizaje estadístico entrena un modelo que predice el tiempo para cada pedido según distancia, tráfico y hora, y te entrega no solo la predicción sino una banda de error calibrada para nuevos pedidos.

No sustituye a la inferencia, la reubica. Pasa de "¿es este parámetro distinto de cero?" a "¿esta regla aprendida generaliza, es estable y puedo confiar en ella para decidir?" Ahí es donde la estadística deja de describir el pasado y empieza a guiar acciones bajo incertidumbre.

---

# Pregunta 2

**¿Por qué el valor de 0.05 (5%) es el estándar de oro para el p-value en la mayoría de las investigaciones? ¿Qué pasaría si usáramos un estándar más relajado, como 0.10 (10%)?**

No hay nada sagrado en 0.05. Es una convención que se volvió costumbre, y la costumbre se volvió filtro editorial.

## Por qué 0.05 se quedó

La historia empieza con Ronald Fisher en 1925. En *Statistical Methods for Research Workers* necesitaba una regla práctica para juzgar si un resultado era "raro bajo la hipótesis nula". Propuso 1 en 20 como punto cómodo: suficientemente improbable para llamar la atención, pero no tan extremo que nunca ocurriera. No lo presentó como ley, lo presentó como atajo.

Luego llegaron Neyman y Pearson en los años 30 y formalizaron la idea de fijar alfa antes del experimento. La comunidad necesitaba un punto focal para coordinarse, y 0.05 ya estaba en los libros, en las tablas impresas, en los cursos. Se volvió el estándar de oro por tres razones no estadísticas:

- **Simplicidad social.** Todos entienden el mismo semáforo: p < 0.05 publica, p > 0.05 no. Evita negociar un umbral nuevo en cada artículo.
- **Equilibrio histórico.** En experimentos agrícolas de Fisher, un falso positivo costaba sembrar una variedad mala un año. Un falso negativo costaba perder una buena variedad. 5% era un compromiso razonable entre esos dos errores cuando no sabías cuál dolía más.
- **Inercia institucional.** Revistas, revisores y software lo codificaron. Cambiarlo implica reentrenar a generaciones.

## Qué significa realmente ese número

0.05 no es la probabilidad de que tu hipótesis sea falsa. Es la probabilidad de ver datos tan extremos como los tuyos *si* la hipótesis nula fuera cierta y repitieras el experimento muchas veces.

Fijar alfa en 0.05 es decir: estoy dispuesto a equivocarme declarando un efecto cuando no existe, una vez cada 20 estudios bien hechos donde nada pasa. Es un contrato sobre error tipo I, no sobre verdad.

## Si lo relajamos a 0.10, ¿qué cambia?

Cambia la tasa de falsos positivos y, por rebote, todo el ecosistema.

- **Más hallazgos, más ruido.** Bajo la nula, pasarías de 5 rechazos falsos cada 100 pruebas a 10. En campos con miles de pruebas simultáneas, genómica, neuroimagen, ese 5% extra se multiplica y la literatura se llena de resultados que no replican.
- **Menos falsos negativos.** Subir alfa aumenta la potencia. Si el efecto real es pequeño y tu muestra es limitada, con 0.10 detectarías más efectos verdaderos que con 0.05. En estudios piloto, exploratorios o donde perder una señal cuesta caro, muchos economistas y psicólogos ya reportan 0.10 como "marginalmente significativo".
- **Incentivos distorsionados.** Si 0.10 se vuelve la nueva barrera para publicar, los investigadores optimizarán para p < 0.10. Verías más p-hacking justo debajo de 0.10, más "grados de libertad del investigador", y la crisis de replicación empeoraría.
- **El costo depende del contexto.** En aprobación de fármacos, un falso positivo puede matar. Ahí usan 0.01 o 0.001. En una prueba A/B de un botón en una app, un falso positivo cuesta poco y perder una mejora real cuesta ingresos. Ahí 0.10 puede ser racional.

Por eso la discusión moderna ya no es "¿0.05 o 0.10?", sino "¿qué pérdida estoy dispuesto a asumir?". Propuestas como bajar a 0.005 para afirmaciones novedosas, o abandonar el umbral y reportar p-values continuos junto con tamaños de efecto, intervalos compatibles y análisis de potencia, vienen de esa lógica.

Usar 0.10 no rompe la estadística. Solo mueve el compromiso: aceptas el doble de alarmas falsas a cambio de atrapar más señales débiles. Si tu campo puede pagar ese precio, y lo declaras antes de mirar los datos, es una decisión coherente. Si lo usas después para rescatar un p = 0.07, estás cambiando las reglas del juego a mitad del partido.

--- 

# Pregunta 3

**¿Cómo se relaciona una correlación de bivariable con una regresión lineal simple?, ¿Cómo actúa el algoritmo del descenso de gradiente como optimizador para una regresión?**

La correlación y la regresión simple cuentan la misma historia lineal, pero una la cuenta en unidades estándar y la otra en unidades reales. El descenso de gradiente es simplemente la forma de encontrar la recta cuando no quieres resolver la fórmula de una vez.

## Correlación bivariable y regresión lineal simple

Tienes dos variables, $X$ y $Y$.

La correlación de Pearson es:
$$ r = \frac{\text{cov}(X,Y)}{s_x s_y} $$
Mide dirección y fuerza en una escala de -1 a 1. Es simétrica: $r_{xy} = r_{yx}$. No hay predictor ni respuesta, solo co-movimiento.

La regresión simple busca la recta que predice $Y$ desde $X$:
$$ \hat{y} = b_0 + b_1 x $$

El vínculo es directo:

- **Pendiente:** $b_1 = r \frac{s_y}{s_x}$. La correlación te da la dirección, y la razón de desviaciones la pone en las unidades de $Y$ por unidad de $X$.
- **Intercepto:** $b_0 = \bar{y} - b_1 \bar{x}$. Asegura que la recta pase por el centro de la nube de puntos.
- **Bondad de ajuste:** $R^2 = r^2$. En simple, el cuadrado de la correlación es exactamente la proporción de varianza de $Y$ explicada por $X$.

Si estandarizas ambas variables a z-scores, $s_x = s_y = 1$, entonces $b_1 = r$ y $b_0 = 0$. Ahí ves que son la misma herramienta con diferente escala.

Diferencias prácticas:

- Correlación resume asociación. Regresión te da predicción: cuánto cambia $Y$ cuando $X$ sube uno.
- Correlación es simétrica. Regresión no: predecir $Y$ con $X$ minimiza errores verticales, predecir $X$ con $Y$ minimiza errores horizontales, y las pendientes no son recíprocas salvo que $r = \pm 1$.
- Ambas asumen linealidad, pero solo la regresión te deja hablar de residuos, intervalos y extrapolación.

## Cómo actúa el descenso de gradiente en la regresión

La regresión por mínimos cuadrados quiere minimizar el error cuadrático medio:
$$ J(b_0,b_1) = \frac{1}{n}\sum_{i=1}^n (y_i - (b_0 + b_1 x_i))^2 $$

En dos dimensiones, $J$ es un paraboloide. La solución cerrada existe: $b = (X^TX)^{-1}X^Ty$. Pero con millones de filas, con muchas variables o con regularización, invertir matrices es caro. El descenso de gradiente evita la fórmula y camina cuesta abajo.

Funciona así:

1. **Inicializa.** Elige $b_0$, $b_1$ al azar o en cero.
2. **Calcula el gradiente.** Son las derivadas parciales del costo:
   - $\frac{\partial J}{\partial b_0} = -\frac{2}{n}\sum (y_i - \hat{y}_i)$
   - $\frac{\partial J}{\partial b_1} = -\frac{2}{n}\sum (y_i - \hat{y}_i) x_i$
     Te dicen la pendiente de la colina en cada dirección.
3. **Actualiza.** Resta un paso proporcional:
   - $b_0 := b_0 - \alpha \frac{\partial J}{\partial b_0}$
   - $b_1 := b_1 - \alpha \frac{\partial J}{\partial b_1}$
     $\alpha$ es la tasa de aprendizaje. Grande avanza rápido pero puede saltar el mínimo. Pequeña es estable pero lenta.
4. **Repite** hasta que el cambio en $J$ sea mínimo.

Variantes:

- **Batch:** usa todos los datos para cada gradiente. Preciso, lento.
- **Estocástico:** usa un punto a la vez. Ruidoso, escapa de mínimos locales, ideal para datos en streaming.
- **Mini-batch:** compromiso habitual en la práctica.

¿Por qué usarlo si la recta tiene solución exacta? Porque el mismo mecanismo funciona sin cambios cuando añades más predictores, términos no lineales, lasso, ridge o redes. No necesitas derivar una nueva fórmula, solo necesitas que $J$ sea diferenciable.

Intuición geométrica: la correlación te dice hacia dónde apunta la nube. La regresión te da la pendiente exacta de la mejor recta. El descenso de gradiente es el método para llegar a esa pendiente caminando, midiendo el error en cada paso y corrigiendo, en vez de saltar directamente con álgebra.
