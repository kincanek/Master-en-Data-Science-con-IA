# K-Means en Profundidad

**K-Means** es un algoritmo de clustering no supervisado que busca particionar $n$ puntos en $k$ grupos, de forma que cada punto pertenezca al grupo cuyo centroide esté más cerca.

La idea central: minimizar la varianza intra-cluster. Es decir, que los puntos dentro de cada cluster estén lo más juntos posible.

### Definición matemática

Tienes un dataset $X = \{x_1, x_2, ..., x_n\}$ donde cada $x_i \in \mathbb{R}^d$. Quieres encontrar $k$ centroides $C = \{c_1, c_2, ..., c_k\}$ que minimicen la **inercia** o **WCSS - Within-Cluster Sum of Squares**:

$$
\text{Inercia} = \sum_{j=1}^{k} \sum_{x_i \in S_j} \|x_i - c_j\|^2
$$

Donde $S_j$ es el conjunto de puntos asignados al cluster $j$, y $\|x_i - c_j\|^2$ es la distancia euclidiana al cuadrado.

**Rol de los centroides**: Cada centroide $c_j$ es el "representante" del cluster $j$. Geométricamente es el centro de masa de todos los puntos asignados a ese cluster.

**Rol de la inercia**: Es la función objetivo que K-Means intenta minimizar. Inercia baja = clusters compactos. Inercia = 0 solo si cada punto es su propio centroide.

### Algoritmo paso a paso

**Input**: Dataset $X$, número de clusters $k$  
**Output**: Asignación de cada punto a un cluster, y posición final de centroides

**Paso 0: Inicialización**  
Elige $k$ centroides iniciales $c_1^{(0)}, c_2^{(0)}, ..., c_k^{(0)}$. Métodos comunes:
- Aleatorio: escoge $k$ puntos del dataset al azar
- K-Means++: escoge el primer centroide aleatorio, los siguientes se escogen con probabilidad proporcional a la distancia^2 al centroide más cercano. Reduce malas inicializaciones.

**Paso 1: Asignación**  
Para cada punto $x_i$, asígnalo al cluster cuyo centroide esté más cerca:

$$
S_j^{(t)} = \{x_i : \|x_i - c_j^{(t)}\|^2 \leq \|x_i - c_l^{(t)}\|^2 \quad \forall l, 1 \leq l \leq k\}
$$

En palabras: calculas la distancia de cada punto a los $k$ centroides y te quedas con el mínimo. Esto crea una partición de Voronoi.

**Paso 2: Actualización**  
Recalcula cada centroide como la media de los puntos asignados a su cluster:

$$
c_j^{(t+1)} = \frac{1}{|S_j^{(t)}|} \sum_{x_i \in S_j^{(t)}} x_i
$$

Si un cluster se queda vacío, estrategias comunes: lo re-inicializas aleatorio o lo eliminas y haces $k-1$.

**Paso 3: Repetir**  
Repite Pasos 1 y 2 hasta que se cumpla un criterio de parada:
1. Los centroides ya no se mueven: $\|c_j^{(t+1)} - c_j^{(t)}\| < \epsilon$
2. Las asignaciones no cambian
3. Se alcanzó un número máximo de iteraciones

### Ejemplo numérico mini
Puntos: (1,1), (1.5,2), (3,4), (5,7), (3.5,5), (4.5,5), (3.5,4.5), $k=2$  
Iter 0: centroides iniciales $c_1=(1,1)$, $c_2=(5,7)$  
Asignación: los 2 primeros a $c_1$, el resto a $c_2$  
Actualización: $c_1=(1.25, 1.5)$, $c_2=(3.9, 5.1)$  
Repites hasta que $c_1≈(1.25,1.5)$, $c_2≈(3.9,5.1)$ y ya no se mueven.

### ¿Por qué K-Means siempre converge?

Porque en cada iteración la inercia nunca aumenta. Prueba:

1. **Paso de asignación**: Cada punto se mueve al centroide más cercano. Si antes estaba a distancia $d_1$ y ahora a $d_2$, sabemos que $d_2 \leq d_1$. La inercia total baja o queda igual.

2. **Paso de actualización**: Para un cluster fijo, la media minimiza la suma de distancias al cuadrado. Es un resultado de cálculo: si derivas $\sum \|x_i - c\|^2$ respecto a $c$ e igualas a 0, obtienes $c = \text{media}$. Así que mover el centroide a la media también baja o mantiene la inercia.

Como la inercia es ≥ 0 y en cada paso baja o se mantiene igual, tiene que converger. Hay un número finito de particiones posibles de $n$ puntos en $k$ grupos, así que no puede ciclar infinitamente.

### ¿Por qué no siempre encuentra el óptimo global?

Porque la inercia como función de los centroides no es convexa. Tiene muchos mínimos locales.

**Intuición**: K-Means es un algoritmo "greedy". En cada paso toma la mejor decisión local: asignar al centroide más cercano, mover a la media. Pero decisiones locales óptimas no garantizan óptimo global.

**Ejemplo clásico del fallo**:  
Imagina 4 puntos en línea: A(0), B(1), C(5), D(6), con $k=2$.  
Óptimo global: clusters {A,B} con centro en 0.5, y {C,D} con centro en 5.5. Inercia = 0.5²+0.5²+0.5²+0.5² = 1.0  

Pero si inicializas centroides en A(0) y C(5):  
Asignación: A,B → 0; C,D → 5  
Actualización: $c_1=0.5$, $c_2=5.5$. Converge. Tuviste suerte.  

Si inicializas en B(1) y D(6):  
Asignación: A,B → 1; C,D → 6  
Actualización: $c_1=0.5$, $c_2=5.5$. También llega al óptimo.

Pero si inicializas en A(0) y B(1):  
Asignación: A → 0; B,C,D → 1  
Actualización: $c_1=0$, $c_2=(1+5+6)/3=4$  
Siguiente asignación: A,B → 0; C,D → 4  
Actualización: $c_1=0.5$, $c_2=5.5$. Llega al óptimo.  

El malo: inicializa en A(0) y en el punto medio (3).  
Puede quedarse atascado en {A} y {B,C,D} con inercia = 0 + 1²+2²+3² = 14, que es mínimo local.

**Solución en la práctica**: 
1. **K-Means++** para inicialización inteligente
2. **Múltiples reinicios**: corres K-Means 10 veces con seeds distintas y te quedas con la corrida de menor inercia. `n_init=10` en sklearn.
3. Aceptar que es NP-hard. Encontrar el óptimo global para $k$ y $n$ grandes es intratable.

**Limitaciones extra**: K-Means asume clusters esféricos de tamaño similar. Falla con formas alargadas, densidades distintas, o clusters no convexos. Ahí usas DBSCAN o GMM.


---

# Detección de Anomalías

**Clustering para detectar anomalías/fraude = "lo raro es lo que no se parece a nada"**

La idea base: si juntas transacciones, usuarios o cuentas similares en grupos, las anomalías son los puntos que no encajan en ningún cluster, o que forman "clusters de 1". En fraude financiero eso funciona porque la mayoría de operaciones son normales y siguen patrones. El fraude rompe el patrón.

### Cómo se usa clustering para detectar anomalías en finanzas

1. **Definir el espacio de features**: Cada transacción o usuario se convierte en vector.  
   Ej: `[monto, hora_del_día, país_destino, #transacciones_ultima_hora, merchant_category, distancia_a_compra_anterior]`.  
   Normalizas todo porque clustering usa distancia.

2. **Agrupar comportamiento normal**: Corres clustering sobre datos históricos. El 99% de usuarios caerá en clusters grandes: "compras de supermercado los sábados", "pago de nómina mensual", "gastos de gasolina martes y jueves".

3. **Marcar lo que no encaja**: 
   - Puntos muy lejos del centroide de su cluster
   - Puntos asignados a clusters diminutos
   - Puntos que el algoritmo etiqueta como "ruido"

4. **Caso real**: Un usuario que siempre gasta $30-80 USD en CDMX, de día, en tiendas físicas. De repente hace 3 compras de $900 USD en Nigeria a las 3am. Ese punto va a quedar lejísimos de su cluster normal → alerta.

**Ventaja vs supervisado**: No necesitas ejemplos etiquetados de fraude. Funciona para "unknown unknowns". El fraude cambia cada mes; clustering detecta patrones nuevos sin reentrenar con labels.

### Limitaciones de K-Means para fraude/anomalías

K-Means es popular porque es rápido, pero tiene 4 problemas graves para este caso:

| **Limitación** | **Por qué mata a K-Means en fraude** |
| --- | --- |
| **1. Asume clusters esféricos del mismo tamaño** | El fraude no forma esferas bonitas. Puede ser una línea: "transferencias de $9,999 USD" justo bajo el límite de reporte. K-Means parte eso a la mitad y falla. |
| **2. Tienes que decirle K de antemano** | ¿Cuántos tipos de comportamiento normal hay? ¿5? ¿50? Si eliges mal, mezcla fraude con normal o crea clusters falsos. |
| **3. Sensible a outliers y todos los puntos deben ir a un cluster** | K-Means fuerza a asignar el fraude a algún cluster. El outlier mueve el centroide y contamina el cluster normal. No tiene concepto de "ruido". |
| **4. Solo usa distancia euclidiana, escala mal con alta dimensión** | Con 100 features, todo queda "lejos de todo" = curse of dimensionality. Y si no escalas bien, la variable "monto" domina a "hora_del_día". |

**Resultado**: K-Means da muchos falsos positivos. En bancos, eso significa bloquear tarjetas legítimas y clientes molestos.

### Algoritmos que usa la industria para superar eso

#### 1. DBSCAN: Density-Based Spatial Clustering of Applications with Noise
**Cómo funciona**: No usa centroides. Agrupa puntos que están "densamente empaquetados". Si un punto no tiene suficientes vecinos en radio `eps`, es ruido = anomalía.

**Por qué es mejor para fraude**:
- **Detecta formas arbitrarias**: Puede encontrar un "filo" de transacciones de lavado justo bajo $10k USD.
- **No requiere K**: Solo `eps` y `min_samples`. 
- **Marca outliers explícitamente**: Tiene etiqueta -1 para ruido. Eso es tu lista de sospechosos.
- **Robusto a ruido**: Los outliers no mueven clusters existentes.

**Limitación de DBSCAN**: Le cuesta con densidad variable. Si tienes clientes "ballena" que gastan mucho y clientes normales, `eps` fijo no sirve para ambos. Y en alta dimensión también sufre.

**Uso real**: PayPal y bancos lo usan para segmentar patrones de red. Si 200 cuentas nuevas todas mandan dinero al mismo destino en 1 hora → DBSCAN las agrupa aunque no sean esféricas.

#### 2. Isolation Forest
**Cómo funciona**: No es clustering, es específico para anomalías. Construye árboles aleatorios que "aíslan" puntos. La idea: las anomalías son pocas y diferentes, así que se aíslan en menos cortes.

**Por qué es el favorito en fraude 2026**:
1. **No asume forma de cluster**: Funciona con líneas, anillos, lo que sea.
2. **Muy rápido y escalable**: O(n) y funciona en 100+ dimensiones. Perfecto para streams de transacciones.
3. **Da un "anomaly score"**: No solo sí/no. Puedes poner threshold según tu tolerancia a falsos positivos.
4. **No usa distancia**: Evita el curse of dimensionality mejor que K-Means/DBSCAN.

**Uso real**: Stripe, Revolut, Nubank. Lo corren en tiempo real por transacción. Si `anomaly_score > 0.8`, manda a revisión manual o pide 2FA.

#### 3. Otros que se usan en producción

| **Algoritmo** | **Cuándo se usa** | **Ventaja** |
| --- | --- | --- |
| **LOF - Local Outlier Factor** | Cuando la densidad varía mucho por segmento de cliente | Detecta anomalía relativa a su vecindario local, no global |
| **Autoencoders** | Fraude complejo con muchas features | Aprende representación normal y marca errores de reconstrucción altos |
| **Gaussian Mixture Models** | Cuando sí esperas clusters pero elípticos | Da probabilidad de pertenencia, no asignación dura |

### Pipeline típico en un banco/fintech

1. **Features en tiempo real**: Monto, velocidad, geoloc, device fingerprint, graph features: "¿este IBAN recibió dinero de 50 cuentas nuevas hoy?"
2. **Modelo no supervisado para triage**: Isolation Forest o Autoencoder da score 0-1.
3. **Reglas + supervisado encima**: Si score > 0.9 → bloquear. Si 0.7-0.9 → mandar a modelo supervisado XGBoost entrenado con casos de fraude confirmados.
4. **Human-in-the-loop**: Analistas revisan casos medios. Su feedback se vuelve label para el supervisado.
5. **Reentrenamiento semanal**: Porque el fraude evoluciona. Data drift es la norma.

**Limitación general de clustering/anomalía**: Alto falso positivo. Decirle a un cliente "bloqueamos tu tarjeta" por error es caro. Por eso nunca se usa solo. Es la primera capa de un sistema multicapa.

**Regla práctica**: K-Means para segmentar clientes y entender comportamiento. Isolation Forest o DBSCAN para encontrar lo que no encaja. 


---
# Aprendizaje No Supervisado en la Industria

**Los 3 casos de uso más impactantes del aprendizaje no supervisado hoy**

El no supervisado brilla donde no hay etiquetas, donde el problema es "descubrir estructura" en vez de "predecir Y". En 2026 estos son los 3 que mueven más dinero:

### 1. Detección de Fraude y AML en Banca/Fintech
**Tipo de algoritmo**: **Detección de anomalías** + **Clustering**  
**Algoritmos reales**: Isolation Forest, Autoencoders, DBSCAN, LOF

**Cómo funciona**: 
Los bancos procesan millones de transacciones/día. El 99.98% son legítimas. No puedes etiquetar fraude a mano, y los defraudadores cambian de táctica cada mes. Entonces usas no supervisado para modelar "comportamiento normal" y disparas alertas cuando algo se sale del patrón.

- **Isolation Forest** aísla transacciones raras: una tarjeta que siempre compra en Puebla hace 4 cargos de $2,000 USD en Singapur a las 3am.
- **DBSCAN** encuentra redes: 200 cuentas nuevas mandando dinero al mismo IBAN en 2 horas = anillo de mulas.
- **Autoencoders** aprenden a reconstruir transacciones normales. Error de reconstrucción alto = posible lavado.

**Valor de negocio**:
1. **Reducción de pérdidas**: J.P. Morgan reportó que ML reduce fraude en tarjetas en >50%. Para un banco grande, eso son cientos de millones de USD/año.
2. **Cumplimiento regulatorio**: AML. Multas por no detectar lavado llegan a billones. Un buen sistema no supervisado detecta patrones nuevos antes que el regulador te multe.
3. **Menos fricción**: Detectas solo lo realmente sospechoso. Bajas falsos positivos → menos clientes bloqueados por error → menos churn.

**Ejemplo**: Stripe Radar usa ensembles donde Isolation Forest es la primera capa. Si pasa el filtro, no molesta al usuario. Si es raro, pide 3DS.

### 2. Segmentación de Clientes y Personalización en E-commerce/Streaming
**Tipo de algoritmo**: **Clustering** + **Reducción de dimensionalidad**  
**Algoritmos reales**: K-Means, GMM, HDBSCAN para cluster; UMAP/PCA para visualizar y preprocesar

**Cómo funciona**:
Netflix no te pregunta "¿eres tipo A, B o C?". Mira 300M de usuarios y sus vectores de comportamiento: `[géneros_vistos, hora_pico, dispositivo, %series_terminadas, búsquedas]`. Son 500 dimensiones.

1. **Reducción de dimensionalidad** con UMAP para poder visualizar y quitar ruido.
2. **Clustering** con HDBSCAN o K-Means para encontrar "tribus": 
   - Cluster 1: "Binge-watchers de k-dramas en móvil, noche"
   - Cluster 2: "Papás que ponen caricaturas en TV los sábados"
   - Cluster 3: "Cinéfilos que ven créditos completos, buscan directores"

**Valor de negocio**:
1. **Revenue por personalización**: McKinsey estima que personalización genera 5-15% más ingresos. Amazon atribuye 35% de ventas a su motor de recomendación, que arranca con segmentación no supervisada.
2. **CAC y retención**: Mandar el email correcto al segmento correcto. Spotify hace "Wrapped" segmentando por cluster. Resultado: viralidad gratis + retención.
3. **Desarrollo de producto**: Descubres segmentos que no sabías que existían. TikTok encontró el cluster "DIY carpintería" y duplicó contenido para ellos. Sin clustering, todos serían "usuarios promedio".

**Ejemplo**: Starbucks usa clustering para decidir dónde abrir tiendas y qué promociones mandar. Si tu cluster "oficinista matutino" está en tu zona, te llega push de "2x1 antes de 10am".

### 3. Mantenimiento Predictivo y Control de Calidad en Manufactura
**Tipo de algoritmo**: **Detección de anomalías** + **Reducción de dimensionalidad**  
**Algoritmos reales**: PCA, Autoencoders, One-Class SVM, T² Hotelling

**Cómo funciona**:
Una turbina eólica tiene 200 sensores: vibración, temperatura, presión, RPM. El 99.9% del tiempo opera "normal". No tienes suficientes fallas etiquetadas para hacer supervisado.

1. **Entrenas con datos normales**: PCA o Autoencoder aprende cómo se ve una turbina sana.
2. **En producción**: Cada segundo entra un vector de 200 sensores. Si la reconstrucción falla o la distancia de Mahalanobis se dispara → anomalía.
3. **Clustering temporal**: Agrupas secuencias de vibraciones. Si aparece un micro-cluster nuevo de "vibración a 45Hz", es un rodamiento empezando a fallar.

**Valor de negocio**:
1. **Evitar downtime**: 1 hora de paro en una planta automotriz = $1.3M USD. Siemens reporta 10-40% reducción en costos de mantenimiento.
2. **Seguridad**: Detectas falla antes de que explote. En aviones, refinerías, esto salva vidas.
3. **Optimizar garantía**: Si sabes que una pieza va a fallar en 30 días, haces mantenimiento programado vs correctivo. Correctivo es 3-5x más caro.

**Ejemplo**: GE usa Autoencoders en turbinas de avión. Detectan desviaciones 2 semanas antes de que el piloto vea una luz. Boeing hace lo mismo con datos de vuelo.

### Tabla resumen

| **Caso de uso** | **Algoritmo clave** | **Valor de negocio directo** |
| --- | --- | --- |
| **Fraude/AML** | Isolation Forest, DBSCAN | -$100M+ en pérdidas evitadas, evitar multas |
| **Segmentación clientes** | K-Means/HDBSCAN + UMAP | +5-15% revenue, -20% churn |
| **Mantenimiento predictivo** | PCA, Autoencoders | -30% downtime, -40% costos mantenimiento |

**Por qué no supervisado y no supervisado**: En los 3 casos, etiquetar es carísimo o imposible, y el problema real es "encuentra lo que no sé que existe". El supervisado predice lo que ya viste. El no supervisado te descubre oportunidades y riesgos nuevos.

