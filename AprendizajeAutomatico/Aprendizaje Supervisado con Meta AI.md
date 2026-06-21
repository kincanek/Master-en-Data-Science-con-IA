# KNN y la Distancia

**K-Nearest Neighbors, KNN** es un algoritmo de aprendizaje supervisado, pero es “perezoso”: no entrena un modelo. Solo memoriza todo el dataset y, cuando llega una predicción nueva, busca a sus vecinos.

### Cómo funciona matemáticamente paso a paso

Tienes un dataset de entrenamiento $D = \{(x_1, y_1), (x_2, y_2),..., (x_n, y_n)\}$ donde $x_i \in \mathbb{R}^d$ son features y $y_i$ la etiqueta.

**Para predecir un punto nuevo $x_q$:**

**Paso 1: Calcular distancias**
Mides la distancia de $x_q$ a todos los puntos de entrenamiento. La más común es la **distancia euclidiana**:

$$
d(x_q, x_i) = \sqrt{\sum_{j=1}^{d} (x_{q,j} - x_{i,j})^2}
$$

Pero también se usa Manhattan $d = \sum |x_{q,j} - x_{i,j}|$, Minkowski, o Coseno para texto. La euclidiana asume espacio “recto” y que todas las dimensiones importan igual.

**Paso 2: Encontrar los K vecinos más cercanos**
Ordenas las $n$ distancias y te quedas con los $K$ puntos $x_{i1}, x_{i2},..., x_{iK}$ con menor $d(x_q, x_i)$.

**Paso 3: Votar / Promediar**
- **Clasificación**: Haces votación mayoritaria. La clase predicha es la moda de $\{y_{i1},..., y_{iK}\}$.
  $$
  \hat{y}_q = \text{mode}(\{y_{i1},..., y_{iK}\})
  $$
- **Regresión**: Promedias los valores.
  $$
  \hat{y}_q = \frac{1}{K} \sum_{j=1}^{K} y_{ij}
  $$

Variante: **KNN ponderado**. Das más peso a vecinos más cercanos: $w_i = \frac{1}{d(x_q, x_i)^2}$. Así un vecino a distancia 1 vale 100x más que uno a distancia 10.

**No hay “entrenamiento”**: La fase de `fit` solo guarda los datos. Todo el cómputo pasa en `predict`. Por eso es O(n) por predicción y lento con datasets grandes.

### El papel de K: sobreajuste vs subajuste

K controla la complejidad del modelo. Es el hiperparámetro más importante.

| **K pequeño, ej. K=1** | **K grande, ej. K=50** |
| --- | --- |
| **Frontera de decisión muy compleja** | **Frontera muy suave** |
| Alta varianza, bajo sesgo | Bajo varianza, alto sesgo |
| **Sobreajuste**: Se adapta al ruido. Un punto mal etiquetado cambia toda la predicción en su región. | **Subajuste**: Ignora patrones locales. Si K=n, siempre predice la clase mayoritaria. |
| Sensible a outliers | Robusto a outliers, pero pierde detalle |

**Visual**: Imagina 2 clases en espiral. Con K=1, la frontera sigue cada punto y se ve dentada. Con K=50, la frontera es casi una línea recta que no separa bien la espiral.

**Cómo elegir K**: Validación cruzada. Típico: prueba K impares de 3 a 21, elige el que minimice error de validación. K impar evita empates en clasificación binaria.

### Por qué la normalización es obligatoria en KNN

KNN usa distancia, y la distancia euclidiana suma diferencias al cuadrado de cada feature. Si una feature tiene escala mayor, domina todo el cálculo.

**Ejemplo que lo rompe**:
Dataset de casas: `[m2, num_habitaciones]`
Casa A: [100 m², 3 hab]
Casa B: [120 m², 2 hab]
Casa nueva: [110 m², 3 hab]

Sin normalizar:
$d(A, nueva) = \sqrt{(100-110)^2 + (3-3)^2} = 10$
$d(B, nueva) = \sqrt{(120-110)^2 + (2-3)^2} = \sqrt{101} ≈ 10.05$

Gana A por muy poco, aunque B es casi igual en habitaciones. Los m² dominaron porque 10²=100 vs 1²=1. La feature “habitaciones” es invisible.

**Normalizando con MinMax a **:
m2: 100→0, 110→0.5, 120→1
hab: 2→0, 3→1
$d(A, nueva) = \sqrt{(0-0.5)^2 + (1-1)^2} = 0.5$
$d(B, nueva) = \sqrt{(1-0.5)^2 + (0-1)^2} = \sqrt{1.25} ≈ 1.12$[0][1]

Ahora gana A por mucho, porque en ambas dimensiones está más cerca. La escala ya no sesga.

**Métodos comunes**:
1. **StandardScaler**: $x' = \frac{x - \mu}{\sigma}$. Bueno si hay outliers.
2. **MinMaxScaler**: $x' = \frac{x - min}{max - min}$. Lleva todo a.[0][1]

Si no normalizas, KNN básicamente solo usa la feature con mayor varianza numérica. En finanzas, “monto de transacción” aplastaría a “hora del día”.

**Otras consideraciones**:
1. **Curse of dimensionality**: En >20-30 dimensiones, todas las distancias tienden a ser similares. KNN deja de funcionar. Necesitas reducción de dimensionalidad tipo PCA.
2. **Costo computacional**: O(nd) por predicción. Para millones de puntos usas estructuras como KD-Tree, Ball Tree, o aproximados como FAISS/Annoy.
3. **Datos desbalanceados**: Si 95% es clase 0, con K=20 casi siempre ganas por mayoría. Solución: ponderar por distancia o hacer undersampling.

**Regla práctica**: Si usas KNN, pipeline = `StandardScaler` → `KNN`. Nunca KNN solo. Y valida K con cross-val.


---

# Métricas de Clasificación

**Precisión, Recall y F1-score** miden diferentes aspectos del error en clasificación binaria. Para entenderlos, parte de la matriz de confusión:

| | **Predicho Positivo** | **Predicho Negativo** |
| --- | --- | --- |
| **Real Positivo** | TP: True Positive | FN: False Negative |
| **Real Negativo** | FP: False Positive | TN: True Negative |

Donde "Positivo" = la clase que te importa detectar. En tumores, Positivo = "tiene cáncer".

### Qué mide cada métrica

**1. Precisión = TP / (TP + FP)**

Pregunta que responde: *"De todos los casos que dije que eran positivos, ¿cuántos realmente lo eran?"*

Mide la pureza de tus predicciones positivas. Precisión alta = pocos falsos positivos. Si tu modelo dice "tienes cáncer" a 10 personas y 9 sí tienen, precisión = 90%.

**2. Recall = Sensibilidad = TP / (TP + FN)**  

Pregunta que responde: *"De todos los casos positivos reales que existían, ¿cuántos logré capturar?"*

Mide qué tan completo eres detectando la clase positiva. Recall alto = pocos falsos negativos. Si había 100 pacientes con cáncer y detectaste 95, recall = 95%.

**3. F1-score = 2 * (Precisión * Recall) / (Precisión + Recall)**

Es la media armónica de ambas. Penaliza fuerte si una de las dos es baja. F1 = 100% solo si Precisión = Recall = 100%. Si Precisión=100% pero Recall=10%, F1=18%. Te obliga a balancear.

### ¿Por qué en tumores malignos prefieres recall sobre precisión?

Por el **costo asimétrico del error**. No todos los errores valen lo mismo.

| **Tipo de error** | **Qué pasa en diagnóstico de cáncer** | **Costo** |
| --- | --- | --- |
| **Falso Negativo, FN** | Decir "estás sano" a alguien que sí tiene tumor | **Catastrófico**. El cáncer avanza, metástasis, muere. Costo: vida humana. |
| **Falso Positivo, FP** | Decir "puede que tengas cáncer" a alguien sano | **Alto pero tolerable**. Ansiedad, biopsia, gastos. Pero al final descartas y el paciente vive. |

**Recall alto = minimizar FN**. Quieres capturar al 99%+ de los enfermos, aunque eso implique que por cada 1 enfermo real marques a 5 sanos como sospechosos.

**Ejemplo numérico**:
Tienes 1000 pacientes, 10 tienen cáncer.

**Modelo A - Optimiza Precisión**: 
Predice 5 positivos. TP=5, FP=0, FN=5  
Precisión = 5/5 = 100%. Recall = 5/10 = 50%.  
Resultado: Dejaste a 5 personas con cáncer irse a casa sin tratar. Inaceptable.

**Modelo B - Optimiza Recall**: 
Predice 50 positivos. TP=10, FP=40, FN=0  
Precisión = 10/50 = 20%. Recall = 10/10 = 100%.  
Resultado: Detectaste a los 10 enfermos. 40 sanos van a biopsia innecesaria, pero nadie muere por no ser detectado.

En medicina el estándar es: **primero sensibilidad, luego especificidad**. Primero aseguras no dejar escapar casos, después refinas para reducir falsas alarmas con más pruebas.

### Cuándo SÍ importa más la precisión

Caso inverso: filtro de spam en email de trabajo.  
FP = marcar un email importante del jefe como spam → puedes perder un contrato.  
FN = que se cuele un spam → lo borras en 2 seg.  
Aquí optimizas precisión. Prefieres dejar pasar spam antes que perder correos críticos.

**Regla práctica**:
1. **Recall alto** cuando FN es caro: cáncer, fraude, defectos en aviones, detección de terremotos.
2. **Precisión alta** cuando FP es caro: recomendaciones legales, bloqueo de cuentas bancarias, despidos automáticos.
3. **F1** cuando ambos errores duelen similar, o cuando clases están desbalanceadas y accuracy miente.

En cáncer, el flujo real es 2 etapas: Modelo 1 con recall 99% hace screening barato = mamografía. Todos los positivos van a Modelo 2 con precisión alta = biopsia. Así optimizas recall al inicio y precisión al final.

---

# Clasificación Binaria vs. Multiclase

**Clasificación binaria vs multiclase** parece solo "2 clases vs 3+ clases", pero los desafíos técnicos cambian bastante.

### Principales desafíos que distinguen binaria de multiclase

| **Aspecto** | **Binaria** | **Multiclase** | **Por qué es más difícil** |
| --- | --- | --- | --- |
| **Frontera de decisión** | 1 frontera: A vs B | K fronteras: K clases, K(K-1)/2 pares | La complejidad crece cuadráticamente. Con 10 clases tienes 45 fronteras que aprender. |
| **Desbalance de clases** | Solo 2 clases. Si una es 5%, es obvio. | Con 10 clases, 3 pueden tener 90% de datos y 7 solo 10% | El modelo ignora clases raras. Accuracy ya no sirve: 95% accuracy puede ser 0% en 8 clases. |
| **Métricas** | Precisión, Recall, AUC son claros | ¿Macro F1, Micro F1, Weighted F1? | Tienes que decidir si todas las clases valen igual o no. Macro-F1 castiga clases pequeñas. |
| **Función de pérdida** | Binary cross-entropy | Categorical cross-entropy, softmax | Softmax asume que clases son mutuamente excluyentes. Si no lo son, falla. |
| **Calibración de probas** | 1 umbral: >0.5 = clase 1 | K-1 umbrales o softmax completo | Elegir threshold por clase es más difícil. |
| **Costo computacional** | 1 modelo | 1 vs resto = K modelos, o 1 modelo más complejo | Entrenar y servir es K veces más lento si usas One-vs-Rest. |

**Desafío clave**: Ambigüedad entre clases. En binaria es "perro o no perro". En multiclase es "perro, lobo, coyote, zorro". Las clases se parecen. El error ya no es binario: confundir lobo con perro duele menos que confundir lobo con gato. Necesitas matriz de costos.

### Cómo KNN se adapta a multiclase

KNN es naturalmente multiclase. No cambia mucho el algoritmo:

**Binaria con K=5**: Buscas 5 vecinos. Si 3 votan "Positivo" y 2 "Negativo" → predices Positivo.

**Multiclase con K=5 y clases A,B,C**: Buscas 5 vecinos.
Vecinos: → votos: A=3, B=1, C=1 → predices A.[A][B][C]

Matemáticamente:
$$
\hat{y}_q = \text{argmax}_{c \in \{1,...,K_{clases}\}} \sum_{i=1}^{K} \mathbb{I}(y_i = c)
$$
Donde $\mathbb{I}$ es 1 si el vecino i tiene clase c. Gana la clase con más votos.

**Variante ponderada**: $w_i = 1/d_i$. Útil en multiclase porque reduce empates. Si tienes A,A,B,B,C con distancias 1,1,2,2,10, el voto ponderado da más peso a A.

**Problema de KNN en multiclase**: Con muchas clases, necesitas K más grande para tener votos estables. Pero K grande suaviza fronteras y confunde clases similares. Y el costo: para 10 clases desbalanceadas, la clase mayoritaria siempre tiene más vecinos cerca → sesgo.

### Estrategias para clases con pocos ejemplos

El problema se llama "class imbalance" y es peor en multiclase. Si tienes 10 clases, 3 con 10k ejemplos y 7 con 50 ejemplos, el modelo ignora las 7.

**1. A nivel de datos: Resampling**

| **Técnica** | **Qué hace** | **Cuándo usarla** |
| --- | --- | --- |
| **Oversampling: SMOTE, ADASYN** | Crea ejemplos sintéticos de la clase minoritaria interpolando vecinos | Tabular, <20 dimensiones. SMOTE falla en alta dimensión. |
| **Undersampling** | Quita ejemplos de clase mayoritaria | Si tienes millones de datos y puedes tirar. |
| **Class weights** | Penaliza más los errores en clases chicas. Loss = w_c * loss | Funciona en casi todo: árboles, NN, SVM. En KNN usas KNN ponderado por clase. |
| **Data augmentation** | Para imágenes/texto: rota, recorta, back-translation | Deep learning. Generas más variedad real. |

**2. A nivel de algoritmo**

- **Ensambles con balanceo**: BalancedRandomForest. Cada árbol se entrena con bootstrap balanceado.
- **Focal Loss**: Para redes neuronales. Baja el peso de ejemplos fáciles, se enfoca en difíciles que suelen ser clase minoritaria.
- **Threshold moving**: Entrenas normal, pero al predecir bajas el umbral para clases chicas. Si softmax da [0.4, 0.3, 0.3], normal dices clase 0. Pero si clase 1 es rara, con umbral 0.2 ya la eliges.

**3. A nivel de evaluación**

No uses Accuracy. Usa:
- **Macro-F1**: Promedio de F1 por clase. Todas valen igual.
- **Balanced Accuracy**: Promedio de recall por clase.
- **Matriz de confusión**: Ve qué clase se confunde con cuál.
- **Precision-Recall por clase**: Para ver si el problema es recall bajo en clase 3.

**Específico para KNN + clases raras**:

1. **KNN con distancia adaptativa**: Usar Mahalanobis o aprender métrica con LMNN. Así las clases pequeñas no son aplastadas por la escala.
2. **SMOTE + KNN**: Generas puntos sintéticos de clase minoritaria, luego KNN tiene más vecinos de esa clase.
3. **K diferente por clase**: K pequeño cerca de clases raras, K grande en zonas densas. Algoritmo: ENN o Tomek Links para limpiar.
4. **No usar KNN**: En alta desbalance, KNN sufre porque la clase mayoritaria domina el vecindario. Mejor árboles o SVM con class_weight.

**Regla de oro en industria**: Si una clase tiene <1% de datos, trátala como problema de detección de anomalías. No como clasificación. Es más fácil decir "esto no es normal" que "esto es clase 7 de 20".

Ejemplo: Fraude con 0.1% positivos y 15 tipos de fraude. No haces 16 clases. Haces binario "fraude vs no fraude" con recall alto, y después clustering sobre los fraudes para tipificarlos.
