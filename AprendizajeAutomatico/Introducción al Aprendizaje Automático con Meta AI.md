# Paradigmas del ML

Los 3 paradigmas de Machine Learning se diferencian por **qué tipo de feedback reciben para aprender** y **qué pregunta responden**.

### 1. Aprendizaje Supervisado
**Idea central**: Aprender una función $y = f(x)$ usando ejemplos etiquetados. Es como estudiar con guía de respuestas.

**Qué necesita**:
- **Datos**: Pares $(x, y)$. Input + etiqueta correcta. $x$ = features, $y$ = target.
- **Objetivo**: Minimizar error entre predicción $\hat{y}$ y etiqueta real $y$. Aprendes a mapear inputs a outputs conocidos.

**Tipos**: Clasificación si $y$ es discreta, Regresión si $y$ es continua.

**Caso de uso real en industria: Scoring de crédito en bancos**
- **Datos**: Histórico de 500k clientes con features: `[ingreso, edad, historial_pagos, deudas, empleo]` + etiqueta $y$ = `¿hizo default en 12 meses? 0/1`.
- **Objetivo**: Dado un cliente nuevo, predecir probabilidad de default.
- **Algoritmos**: Logistic Regression, XGBoost, Redes Neuronales.
- **Valor de negocio**: Automatizar aprobación de créditos. Baja morosidad 20-30%, decisión en segundos vs días.
- **Requisito clave**: Necesitas miles de labels históricos. Si no tienes defaults pasados etiquetados, no funciona.

### 2. Aprendizaje No Supervisado  
**Idea central**: Encontrar estructura oculta en datos sin etiquetas. Es como que te den un cajón de fotos y te pidan “organízalas como tenga sentido”.

**Qué necesita**:
- **Datos**: Solo $x$. No hay $y$. Solo inputs.
- **Objetivo**: Agrupar, reducir dimensionalidad, o detectar patrones/anomalías. No hay “respuesta correcta”, solo estructura útil.

**Tipos principales**: Clustering, Reducción de dimensionalidad, Detección de anomalías, Reglas de asociación.

**Caso de uso real en industria: Segmentación de clientes en e-commerce**
- **Datos**: 10M usuarios con features: `[productos_vistos, gasto_mensual, hora_compra, dispositivo, categorías]`. Sin etiquetas.
- **Objetivo**: Descubrir grupos naturales. K-Means/HDBSCAN encuentra: “cazadores de ofertas nocturnos”, “mamás que compran los lunes”, “gamers que gastan en quincena”.
- **Algoritmos**: K-Means, DBSCAN, UMAP + HDBSCAN, PCA.
- **Valor de negocio**: Personalización. Netflix usa esto para recomendar. Amazon atribuye 35% de revenue a recomendaciones que arrancan con segmentación no supervisada. Mandas email correcto al segmento correcto → +10% conversión.
- **Requisito clave**: Necesitas muchos datos, pero no labels. La validación es difícil: ¿el cluster es útil para negocio?

### 3. Aprendizaje por Refuerzo, RL
**Idea central**: Un agente aprende a tomar acciones en un entorno para maximizar recompensa acumulada. Es como entrenar a un perro: premio si lo hace bien, no hay “respuesta correcta” paso a paso.

**Qué necesita**:
- **Datos**: No pares $(x,y)$. Necesitas un entorno donde puedas probar acciones y recibir feedback: $(estado, acción, recompensa, siguiente_estado)$.
- **Objetivo**: Aprender una política $\pi(acción|estado)$ que maximice recompensa a largo plazo. Prueba y error.

**Conceptos**: Agente, entorno, estado, acción, recompensa, política.

**Caso de uso real en industria: Optimización de bids en publicidad digital**
- **Datos**: Entorno = subasta de ads en tiempo real. Estado = `[perfil_usuario, hora, sitio_web, budget_restante]`. Acción = `¿cuánto pujar por mostrar el ad?`. Recompensa = `si hubo click +1, si hubo compra +10, si gastaste budget -1`.
- **Objetivo**: Aprender política de puja que maximice ROAS a lo largo del día, no solo en una subasta.
- **Algoritmos**: Q-Learning, PPO, Deep Q-Networks.
- **Valor de negocio**: Google y Meta usan RL para auto-bidding. Mejora ROAS 15-30% vs reglas fijas, porque el agente aprende cuándo pujar agresivo y cuándo ahorrar budget.
- **Requisito clave**: Necesitas simular millones de interacciones o un entorno real donde fallar es barato. No sirve si cada error cuesta $1M.

### Tabla comparativa

| | **Supervisado** | **No Supervisado** | **Refuerzo** |
| --- | --- | --- | --- |
| **Datos** | $(x, y)$ etiquetados | Solo $x$, sin etiquetas | $(estado, acción, recompensa)$ vía interacción |
| **Pregunta** | ¿Qué $y$ corresponde a este $x$? | ¿Qué estructura hay en $x$? | ¿Qué acción tomar para maximizar recompensa futura? |
| **Feedback** | Inmediato y correcto: “la respuesta era 1” | Ninguno. Tú evalúas si sirve. | Retrasado y escalar: “+10 puntos 5 pasos después” |
| **Output** | Predicción | Clusters, embeddings, scores | Política de acción |
| **Caso industria** | Detección de fraude, diagnóstico médico | Segmentación, detección anomalías | Trading, robótica, ads, juegos |
| **Falla si...** | No hay labels o son caros | No sabes qué buscar | No puedes simular/probar sin riesgo |

**Regla para elegir**:
1. ¿Tienes inputs y outputs históricos? → **Supervisado**.
2. ¿Tienes inputs pero no sabes qué buscar? → **No supervisado**.
3. ¿Tienes que tomar secuencias de decisiones y solo ves si funcionó al final? → **Refuerzo**.

En la práctica se combinan: Usas no supervisado para segmentar, supervisado para predecir churn por segmento, y refuerzo para decidir qué descuento ofrecer a cada segmento.

---
# Redes Neuronales

**Una red neuronal artificial, ANN** es un modelo matemático inspirado muy vagamente en el cerebro. No es una réplica, pero toma 3 ideas clave de la neurociencia:

### Relación con el cerebro humano

| **Cerebro humano** | **Red neuronal artificial** |
| --- | --- |
| **Neurona biológica**: Recibe señales eléctricas por dendritas, si supera un umbral dispara por el axón | **Neurona artificial**: Recibe números $x_1, x_2...$, hace suma ponderada, pasa por función de activación, saca un número |
| **Sinapsis**: Conexiones entre neuronas. Su "fuerza" cambia con el aprendizaje | **Pesos $w$**: Número que multiplica cada input. Aprender = ajustar $w$ |
| **Aprendizaje**: Sinapsis se refuerzan si las neuronas se activan juntas. “Hebbian learning” | **Backpropagation**: Ajustas pesos para reducir error. Mucho más matemático, nada biológico |

**Diferencias críticas**: El cerebro tiene 86 mil millones de neuronas, aprende con poquísimos ejemplos, consume 20W, y es masivamente paralelo y asíncrono. Una ANN tipo GPT-4 tiene billones de parámetros, necesita millones de ejemplos, consume MW, y es secuencial por capas. La inspiración es conceptual, no literal.

### Arquitectura básica de una ANN
Tienes capas de neuronas:

1. **Capa de entrada**: Recibe los datos. 1 neurona por feature. `[edad, ingreso, deudas]`
2. **Capas ocultas**: Donde pasa la "magia". Cada neurona hace: $z = w_1x_1 + w_2x_2 + b$, luego $a = f(z)$. $f$ es activación: ReLU, Sigmoid.
3. **Capa de salida**: Da la predicción. 1 neurona para regresión, N neuronas + softmax para clasificación de N clases.

Aprender = encontrar los valores de todos los $w$ y $b$ que hacen que la red dé buenas predicciones.

### Los 3 conceptos clave del entrenamiento

#### 1. Función de pérdida / Loss Function
**Qué es**: Una fórmula que mide "qué tan mal lo está haciendo el modelo ahora". Compara predicción vs realidad.

**Ejemplos**:
- **Regresión - MSE**: $L = \frac{1}{n}\sum (y_{real} - y_{pred})^2$. Penaliza fuerte errores grandes.
- **Clasificación - Cross-Entropy**: $L = -\sum y_{real} \log(y_{pred})$. Penaliza estar seguro y equivocado.

Si $L=0$, predicción perfecta. Si $L$ grande, la red está perdida. Tu objetivo es minimizar $L$.

#### 2. Descenso de gradiente / Gradient Descent
**Qué es**: El algoritmo para minimizar la pérdida. Idea: estás en una montaña con niebla y quieres bajar. Miras la pendiente a tus pies y das un paso en la dirección que más baja.

Matemáticamente: El gradiente $\nabla L$ es un vector que apunta a donde la pérdida sube más rápido. Entonces te mueves al contrario:

$$
w_{nuevo} = w_{viejo} - \alpha \cdot \nabla_w L
$$

- $w$: pesos de la red
- $\alpha$: learning rate, tamaño del paso. Si $\alpha$ muy grande, te pasas. Si muy chico, tardas años.
- $\nabla_w L$: derivada de la pérdida respecto a cada peso. Te dice "si subo este peso, la pérdida sube/baja cuánto".

**Backpropagation** es el algoritmo que calcula $\nabla L$ eficientemente usando regla de la cadena, desde la salida hacia atrás.

#### 3. Épocas de entrenamiento / Epochs
**Qué es**: Una época = ver todo el dataset de entrenamiento 1 vez completa.

Como el dataset suele ser gigante, no calculas gradiente con todos los datos. Usas **mini-batches**: Tomas 32 o 128 ejemplos, calculas gradiente, actualizas pesos. Cuando pasaste por todos los mini-batches, completaste 1 época.

**Por qué varias épocas**: 1 pasada no basta. Es como leer un libro 1 vez vs 50 veces. Cada época, los pesos se ajustan un poco más. Típico: 10 a 500 épocas.

- **Pocas épocas**: Underfitting. El modelo no aprendió.
- **Muchas épocas**: Overfitting. El modelo memoriza el train y falla en datos nuevos. Por eso usas validation set para parar.

### Cómo trabajan juntos: el ciclo de aprendizaje

Piensa en entrenar una red para reconocer gatos:

1. **Inicialización**: Pesos $w$ aleatorios. La red dice disparates. $L$ = muy alto.

2. **Forward pass**: Metes un batch de 32 imágenes. La red propaga números capa por capa y saca predicciones: `[0.2, 0.8, 0.1...]` = prob de gato.

3. **Calcular pérdida**: Comparas con labels reales `[0, 1, 0...]`. Cross-entropy da $L = 2.3$.

4. **Backward pass / Backprop**: Calculas gradiente $\nabla L$. Te dice: "sube $w_{152}$ y baja $w_{907}$ para reducir error".

5. **Descenso de gradiente**: Actualizas todos los pesos: $w = w - 0.001 * \nabla L$. Ahora la red es un poquito menos mala.

6. **Repite**: Haces esto con todos los batches. Al terminar el dataset = 1 época. $L$ bajó de 2.3 a 2.1.

7. **Más épocas**: Época 2: $L=1.8$. Época 10: $L=0.4$. Época 50: $L=0.15$. La red ya reconoce gatos.

**Analogía**: La **función de pérdida** es el "examen" que califica qué tan mal vas. El **descenso de gradiente** es el "método de estudio" que te dice qué cambiar. Las **épocas** son "cuántas veces repasaste toda la guía".

Sin pérdida no sabes si mejoras. Sin gradiente no sabes cómo cambiar. Sin épocas no ves suficientes datos para generalizar.

**Resultado**: Tras suficientes épocas, los pesos $w$ convergen a valores que minimizan $L$. La red "aprendió" la relación entre pixeles y "gato".

---
# Scikit-learn vs TensorFlow

**Scikit-learn vs TensorFlow** = "cuchillo suizo para ML clásico" vs "motor para deep learning". Resuelven problemas distintos, aunque hay traslape.

### Diferencias fundamentales

| **Aspecto** | **Scikit-learn** | **TensorFlow** |
| --- | --- | --- |
| **Paradigma principal** | **ML clásico**: modelos estadísticos que corren en CPU. Todo está implementado y listo. | **Deep Learning + Computación numérica**: Tú construyes redes neuronales capa por capa. Motor de tensores. |
| **Nivel de abstracción** | Alto. `model.fit(X,y)` y listo. 3 líneas tienes un RandomForest. | Bajo-medio. Con Keras es alto, pero puedes bajar a grafos y derivadas. Tú controlas arquitectura. |
| **Algoritmos nativos** | SVM, RandomForest, KNN, K-Means, PCA, Logistic Regression. 100+ algoritmos. | Redes neuronales: DNN, CNN, RNN, Transformers. Para ML clásico tienes que programarlo tú. |
| **Hardware** | CPU. Algunos modelos usan multi-core, pero no GPU nativo. | GPU/TPU nativo. Entrenar ResNet en CPU tarda semanas, en GPU horas. |
| **Datos que maneja bien** | **Datos tabulares**: CSV de 10k-1M filas, 100 columnas. Lo que ves en Kaggle. | **Datos no estructurados**: Imágenes, texto, audio, video, series largas. |
| **Entrenamiento** | Batch. Cargas todo a RAM. Si no cabe, sufres. | Mini-batch + out-of-core. Puedes entrenar con 100GB de imágenes en streaming. |
| **Deployment** | Exportas `.pkl` con joblib. Fácil en Flask/FastAPI. | Exportas `.pb` o TFLite. Optimizado para móvil, edge, serving a escala con TF-Serving. |
| **Curva de aprendizaje** | 1 día. API consistente: `.fit`, `.predict`, `.transform`. | 1-4 semanas. Tienes que entender tensores, grafos, backprop, epochs. |

### ¿Cuándo usar cada uno?

**Usa Scikit-learn cuando:**

1. **Problema tabular clásico**: Churn, scoring de crédito, predicción de precios de casas, segmentación. Si tus datos caben en un DataFrame de pandas, Scikit-learn gana.
2. **Necesitas baseline rápido**: 10 líneas y tienes 5 modelos + cross-val. En 30 min sabes si el problema es factible.
3. **Interpretabilidad importa**: RandomForest + SHAP te da feature importance. Reguladores en banca piden explicar el modelo. En deep learning es caja negra.
4. **Dataset pequeño-mediano <1M filas**: KNN, SVM, XGBoost funcionan mejor que redes con pocos datos.
5. **No tienes GPU**: Tu laptop entrena RandomForest en 2 min. TensorFlow sin GPU es doloroso.

**Ejemplo real**: Banco quiere predecir default. 200k clientes, 50 features. Scikit-learn: `RandomForestClassifier` + `GridSearchCV`. AUC 0.91 en 1 hora de trabajo. Deploy en 1 día.

**Usa TensorFlow cuando:**

1. **Datos no estructurados**: Imágenes, texto, audio, series temporales largas. Clasificar radiografías, traducir idiomas, generar texto. Scikit-learn no puede.
2. **Necesitas Deep Learning**: CNNs para visión, Transformers para NLP, LSTMs para secuencias. 10M+ parámetros.
3. **Escala masiva**: Entrenar con 50M imágenes. Necesitas GPU/TPU y data pipelines con `tf.data`.
4. **Deployment especializado**: Modelo en Android con TFLite, en browser con TF.js, o sirviendo 100k req/s con TF-Serving.
5. **Custom loss / arquitectura**: Quieres una red siamesa, loss con física, attention custom. TF te da control total.

**Ejemplo real**: Tesla Autopilot. Input: video 8 cámaras. Output: segmentación + depth + objetos. Solo deep learning con TF/PyTorch. 48 GPUs, 2 semanas entrenando.

### ¿Se usan juntos? Sí, y es muy común. Pipeline híbrido.

Scikit-learn y TensorFlow no compiten, se complementan. Típico en industria:

**Caso 1: Preprocesamiento Sklearn + Modelo TF**
Tienes tabular + texto.
```python
from sklearn.preprocessing import StandardScaler
from sklearn.compose import ColumnTransformer
from tensorflow import keras

# 1. Sklearn para features tabulares
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), numeric_cols),
    ('cat', OneHotEncoder(), categorical_cols)
])
X_tab = preprocessor.fit_transform(X)

# 2. TF para modelo mixto: tabular + embeddings de texto
tab_input = keras.Input(shape=(X_tab.shape[1],))
text_input = keras.Input(shape=(None,))
x = keras.layers.Embedding(10000, 128)(text_input)
x = keras.layers.LSTM(64)(x)
combined = keras.layers.concatenate([tab_input, x])
output = keras.layers.Dense(1, activation='sigmoid')(combined)
model = keras.Model([tab_input, text_input], output)
```
Aquí Sklearn hace lo que hace mejor: encoding/scaling. TF hace lo que Sklearn no puede: LSTM.

**Caso 2: Embeddings de TF como features para Sklearn**
Tienes imágenes de productos. Usas ResNet pre-entrenada en TF para extraer embedding de 2048 dims por imagen. Luego metes esos 2048 dims + precio + categoría a un `XGBClassifier` de Sklearn/XGBoost.
Ventaja: XGBoost es mejor que una red densa para tabular + overfitting menor con pocos datos.

**Caso 3: Pipeline completo con `scikeras`**
`SciKeras` envuelve modelos de Keras para que tengan API de Sklearn. Así puedes meter una red de TF dentro de `GridSearchCV` o `Pipeline` de Sklearn:
```python
from scikeras.wrappers import KerasClassifier
model = KerasClassifier(build_fn=create_model)
grid = GridSearchCV(model, param_grid={'epochs':[10,50], 'batch_size':[32,128]})
```
Ahora haces CV y tuning de una red TF con sintaxis de Sklearn.

**Caso 4: Sklearn para baseline, TF si hace falta**
Regla de oro en industria: Siempre prueba Sklearn/XGBoost primero. Si llegas a 92% AUC y negocio necesita 93%, ya evalúas TF. El 80% de problemas tabulares no necesitan deep learning.

**Resumen de decisión**:

1. **Datos tabulares <10M filas** → Empieza Scikit-learn + XGBoost. Solo si fallan, prueba TF TabNet.
2. **Imágenes/Texto/Audio** → TensorFlow o PyTorch directo.
3. **Mixto tabular + no estructurado** → Usa ambos: Sklearn preprocesa, TF modela, o TF genera embeddings para Sklearn.
4. **Deploy en móvil/edge** → TF/TFLite. Sklearn no está optimizado para eso.
