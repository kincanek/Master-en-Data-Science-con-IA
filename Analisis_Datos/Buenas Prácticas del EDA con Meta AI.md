# Reproducibilidad en Data Science

**Reproducibilidad = "si yo corro tu código en 6 meses, obtengo el mismo resultado"**

En ciencia de datos profesional no basta con que "te funcione a ti hoy". Si otro no puede replicar tu análisis, no es ciencia, es anécdota. Y en empresas, una anécdota no justifica invertir $2M.

### ¿Por qué es un pilar fundamental?

1. **Confianza y auditoría**: Si tu modelo rechaza un crédito, reguladores o legal van a pedir reproducir la decisión. En pharma, FDA exige reproducir todo el análisis antes de aprobar un fármaco. Sin reproducibilidad, no hay compliance.

2. **Debugging y mantenimiento**: Modelo en producción falla 3 meses después. Si no puedes reproducir qué datos usaste para entrenarlo, no sabes si el bug es de datos, código o concepto. Vas a ciegas.

3. **Colaboración**: Tu colega retoma tu proyecto cuando estás de vacaciones. Si tu notebook dice `df = pd.read_csv('datos_final_v3_FINAL.csv')` y ese archivo no existe, el equipo se para.

4. **Iteración científica**: La ciencia avanza porque otros construyen sobre tu trabajo. Si publicas un paper con AUC=0.98 pero nadie lo reproduce, tu resultado vale cero. Crisis de reproducibilidad en ML es real.

5. **Negocio**: CEO pregunta "¿por qué el forecast de Q4 cambió 30% vs el mes pasado?". Si no reproduces el run anterior, no puedes explicar la diferencia. Pierdes credibilidad y budget.

### Prácticas clave para garantizar reproducibilidad en Colab/Jupyter

Los notebooks son enemigos de la reproducibilidad por defecto. Ejecución fuera de orden, variables globales, estado oculto. Hay que disciplinarlos:

#### 1. Fija el entorno
**Problema**: "En mi máquina funciona". `pandas 1.5` vs `2.0` cambian `groupby`.  
**Solución en Colab**:
```python
!pip freeze > requirements.txt  # Guarda versiones exactas
!pip install pandas==2.1.1 scikit-learn==1.3.2  # Fija versiones al inicio
```
Mejor: Usa `conda env` o `Docker` si sales de Colab. En Colab, mínimo fija versiones críticas en la primera celda.

#### 2. Fija las semillas aleatorias
**Problema**: Train/test split, inicialización de pesos, KMeans dan resultados distintos cada vez.  
**Solución**:
```python
import numpy as np, random, tensorflow as tf
SEED = 42
random.seed(SEED)
np.random.seed(SEED)
tf.random.set_seed(SEED)
# Para sklearn:
train_test_split(..., random_state=SEED)
RandomForest(random_state=SEED)
```
Sin esto, tu accuracy baila ±3% entre runs y no sabes si mejoraste el modelo o tuviste suerte.

#### 3. Controla los datos
**Problema**: `pd.read_csv('/content/drive/datos.csv')`. En 2 meses borraste el archivo o lo editaste.  
**Solución**:
1. **Versiona datos**: Usa DVC, o mínimo guarda snapshot: `df.to_parquet('gs://bucket/data_v2026_06_21.parquet')`
2. **No edites datos in-place**: Nunca `df.dropna(inplace=True)`. Siempre crea copia y guarda el pipeline.
3. **Documenta origen**: Primera celda: `# Datos de BigQuery: SELECT * FROM sales WHERE date < '2026-06-01'`

#### 4. Haz el notebook lineal y ejecutable de arriba a abajo
**Problema**: Ejecutas celda 5, luego 2, luego 8. Estado depende del orden.  
**Solución**: 
1. `Kernel > Restart & Run All` debe funcionar sin errores.
2. No reuses nombres de variables: `df` → `df_raw` → `df_clean` → `df_features`.
3. Evita celdas que solo tú puedes correr: `files.upload()` interactivo. Mejor carga de GCS/S3.

#### 5. Registra parámetros y resultados
**Problema**: "Usé learning_rate=0.01... creo".  
**Solución**: MLflow, Weights & Biases, o mínimo un dict:
```python
params = {'n_estimators': 100, 'max_depth': 5, 'seed': 42}
model = RandomForestClassifier(**params)
# Guarda:
json.dump({'params': params, 'auc': 0.91, 'fecha': '2026-06-21'}, open('run.json','w'))
```

#### 6. Versiona el código
**Problema**: Notebook `analisis_final_FINAL_ahora_si.ipynb`.  
**Solución**: Git. Aunque Colab no es ideal, usa `File > Save a copy in GitHub`. O exporta `.py` con `jupytext` y versiona eso. Commits atómicos: "Agrega feature de recency".

### Consecuencias cuando un análisis NO es reproducible

**Para el equipo:**

1. **Tiempo perdido exponencial**: Caso real: Data scientist se va, deja notebook. Equipo tarda 3 semanas en “ingeniería inversa” para entender por qué el modelo da 70% recall. Cuesta $30k en sueldos solo para recuperar conocimiento.

2. **Imposible auditar o debuggear**: Modelo en prod baja performance 15%. ¿Fue cambio de datos? ¿Deploy de versión vieja? Si no reproduces el baseline, no sabes. Decisión: rollback a ciegas, pierdes mejoras.

3. **Desconfianza cross-funcional**: PM, Legal, Business te piden rehacer análisis "para confirmar". Si tardas 2 días porque no corre, asumen que tu trabajo era frágil. Próximo proyecto no te lo dan a ti.

4. **Riesgo legal/financiero**: Banco no puede explicar a CNBV por qué negó crédito. Multa. Pharma no pasa auditoría FDA. Fármaco se retrasa 1 año = $500M perdidos.

5. **Bloquea CI/CD y MLOps**: No puedes automatizar reentrenamiento si el training es “arte manual”. Te quedas en notebooks ad-hoc forever. No escalas.

**Regla de oro**: Si no puedes `Restart & Run All` en una máquina limpia y obtener el mismo `.csv` de resultados, no está listo para producción.

En resumen: Reproducibilidad = profesionalismo. Es la diferencia entre "hice un análisis" y "construí un asset de datos". 

---
# Documentación de Decisiones Analíticas

**Documentar el "qué" vs el "por qué"** es la diferencia entre escribir un recetario y escribir un paper científico.

- **Documentar el QUÉ**: Describe la acción. Qué código corre, qué transformación hiciste. Responde "¿qué está pasando?".  
  Es útil, pero si solo tienes esto, en 2 meses no recuerdas si esa decisión fue arbitraria o crítica.

- **Documentar el POR QUÉ**: Describe el razonamiento. Qué alternativas consideraste, qué problema resuelve, qué asunciones haces. Responde "¿por qué esta acción y no otra?".  
  Esto es lo que permite que tú futuro o tu colega entienda, debata, o cambie la decisión sin romper todo.

**Regla**: El código ya muestra el "qué". Los comentarios y Markdown deben agregar el "por qué". Si tu comentario solo repite el código, bórralo.

---

### Ejemplo concreto: Imputar valores nulos con media vs mediana

**Contexto del problema**: Tienes la columna `ingreso_mensual` con 8% de nulos. Hay que imputar antes de entrenar un modelo de riesgo crediticio.

#### MAL: Solo documentar el qué

**Celda Markdown**:
```
## Imputación de valores nulos
```

**Celda de código**:
```python
# Reemplaza nulos con la mediana
df['ingreso_mensual'] = df['ingreso_mensual'].fillna(df['ingreso_mensual'].median())
```

**Problema**: ¿Por qué mediana y no media? ¿Por qué no dropear? ¿Qué pasa si la distribución cambia? En 3 meses nadie sabe si esto fue pensado o fue copy-paste de StackOverflow.

---

#### BIEN: Documentar qué + por qué

**Celda Markdown**: Aquí va el contexto de negocio y la decisión de alto nivel
```markdown
### 3.2 Imputación de `ingreso_mensual`

**Decisión**: Imputamos los valores nulos usando la mediana, no la media.

**Justificación**:
1. **Distribución sesgada**: `ingreso_mensual` tiene cola derecha larga por outliers >$200k MXN. La media=$45k está inflada; la mediana=$32k representa mejor al cliente típico. Usar media metería sesgo al alza en 8% de los clientes.
2. **Impacto en modelo**: El modelo de riesgo es sensible a ingresos altos. Imputar con media haría que clientes sin dato parezcan más solventes de lo real → subestima riesgo.
3. **Alternativas descartadas**: 
   - Dropear filas: Perderíamos 8% de datos = 40k clientes. Inaceptable para negocio.
   - KNN Imputer: Probado, pero aumenta tiempo de training 10x y ganancia en AUC <0.005. No vale el costo.
   
**Asunción**: Asumimos que los nulos son MAR (Missing At Random) y no clientes que ocultan ingreso. Validar con equipo de negocio en Q3.

**Riesgo**: Si la proporción de nulos sube >15%, re-evaluar estrategia. Monitorear en pipeline.
```

**Celda de código**: Aquí va el "por qué" específico de implementación
```python
# Usamos mediana en lugar de media porque ingreso tiene outliers de >3 desviaciones estándar
# que sesgarían la imputación al alza. Mediana es robusta a cola derecha.
# Validado en EDA: skew=4.2. Ver celda 2.1 para histograma.
mediana_ingreso = df['ingreso_mensual'].median()  # 32,000 MXN en train
df['ingreso_mensual'] = df['ingreso_mensual'].fillna(mediana_ingreso)

# IMPORTANTE: Fijar el valor de mediana del train para usarlo en test/producción
# y evitar data leakage. No recalcular mediana en test.
```
---

### Guía rápida: Dónde poner qué

| **Dónde** | **Qué va** | **Ejemplo** |
| --- | --- | --- |
| **Celda Markdown antes del código** | Contexto, trade-offs, alternativas, impacto en negocio, asunciones, links a EDA | "Elegimos mediana porque skew=4.2. Alternativas: media, KNN. Media sesga..." |
| **Comentario en código** | Justificación de línea específica, warnings, TODOs, referencia a otras celdas | `# Evita data leakage: usar mediana de train` |
| **Docstring de función** | Qué hace, qué asume, qué retorna, ejemplo | `"""Imputa con mediana de train. Asume MAR."""` |

**Anti-patrones a evitar**:
1. `# Suma 1 a x`: El código ya dice `x + 1`. No aporta nada.
2. `# Magia`: Si no puedes explicar el por qué, quizá no deberías hacerlo.
3. Solo documentar en Markdown o solo en código. Usa ambos: Markdown para estrategia, código para táctica.

**Beneficio real**: Cuando en 6 meses auditoría pregunte "¿por qué imputaron así?", abres el notebook y la respuesta está ahí. No dependes de tu memoria.


---
# EDA en la Industria

**Un EDA profesional no es "hacer unos `.describe()` y graficar"**. Es una fase estructurada que responde 3 preguntas: ¿Puedo confiar en estos datos? ¿Qué patrones hay? ¿Qué le voy a decir al modelo que aprenda?

En equipos serios, EDA tiene dueño, checklist, y entregables formales. Porque un mal EDA te hace perder 3 meses modelando sobre datos rotos.

### Cómo se estructura un EDA en un equipo profesional

**Fase 0: Definir la pregunta de negocio**  
Antes de tocar pandas. Data Scientist + PM + Stakeholder definen: "¿Qué queremos predecir/decidir?". Sin esto, EDA es fishing expedition.

**Fase 1: Auditoría de datos - "¿Puedo confiar?"**  
**Objetivo**: Encontrar problemas que rompen modelos.  
**Tareas**:
1. **Inventario**: #filas, #columnas, tipos, cardinalidad. Tabla de metadatos.
2. **Calidad**: %nulos por columna, duplicados, outliers, fechas fuera de rango, violaciones de negocio: `edad < 0`, `fecha_fin < fecha_inicio`.
3. **Data leakage**: ¿Hay columnas del futuro? `target` construido con info post-evento.
4. **Drift inicial**: Distribución train vs test vs prod. Si ya son distintas, para todo.

**Fase 2: Univariado - "¿Cómo se comporta cada variable sola?"**  
**Objetivo**: Entender distribuciones, decidir transformaciones.  
**Tareas**: Histograma, boxplot, skew, kurtosis. Para categóricas: frecuencia, cardinalidad alta. Decides: log-transform, binning, rare encoding.

**Fase 3: Bivariado/Multivariado - "¿Qué relaciones hay?"**  
**Objetivo**: Encontrar features útiles y redundantes.  
**Tareas**: 
1. **Target vs feature**: ¿`ingreso` separa bien a `defaulters`? Boxplot, barplot con target rate.
2. **Feature vs feature**: Matriz de correlación, VIF para multicolinealidad. Scatter de variables clave.
3. **Segmentos**: ¿El patrón cambia por país, por canal? `groupby` + visual.

**Fase 4: Hipótesis y hallazgos para modelado**  
**Objetivo**: Traducir EDA a decisiones.  
**Tareas**: Lista de features a crear, a descartar, imputaciones, encoding. Ejemplo: "Crear `ratio_deuda_ingreso`. `codigo_postal` tiene 50k categorías → usar target encoding".

**Fase 5: Validación con negocio**  
**Objetivo**: Sanity check. Enseñas hallazgos raros al experto de dominio.  
Ejemplo: "El 20% de clientes tiene ingreso=0. ¿Es real o error de captura?". Si negocio dice "es real, son becarios", cambias cómo imputas.

### Entregables esperados antes de modelar

Un EDA no termina cuando cierras el notebook. Termina cuando entregas 4 artefactos:

| **Entregable** | **Qué contiene** | **Para quién** |
| --- | --- | --- |
| **1. Data Dictionary + Data Quality Report** | Tabla: columna, tipo, %nulos, min/max, #únicos, definición de negocio, problemas detectados. | Ingenieros ML, para hacer pipeline. Auditoría. |
| **2. EDA Notebook limpio** | Solo celdas ejecutadas en orden, con Markdown explicando hallazgos. Sin código exploratorio basura. Versionado en Git. | Otros Data Scientists. Para reproducir y extender. |
| **3. Feature Proposal Doc** | Lista de features: nombre, fórmula, justificación basada en EDA, cómo tratar nulos/outliers. "Aprobado/Rechazado" por DS Lead. | Tú futuro + equipo. Es el contrato antes de modelar. |
| **4. Resumen ejecutivo para stakeholders** | 1-2 páginas o 5 slides: 3 insights clave, 2 riesgos de datos, decisión: "Sí podemos modelar" o "Bloqueado por X". Sin jerga. | PM, Director, Negocio. |

**Criterio de "Definition of Done"**: Si no puedes responder "¿qué features vas a usar y por qué?" con un doc, el EDA no terminó.

### Herramientas y formatos para comunicar a no técnicos

A stakeholders no les mandas un notebook de 200 celdas. Les traduces.

**1. Reportes automatizados: `ydata-profiling`, `Sweetviz`, `DataPrep`**  
Generas HTML interactivo en 2 líneas. Muestra nulos, correlaciones, distribuciones.  
**Cuándo**: Para kick-off técnico rápido. Mandas link: "Aquí está el perfil de datos".  
**Límite**: No cuenta la historia. Es solo el "qué", no el "entonces qué".

**2. Slides / Memo - El estándar oro**  
**Formato**: 5-7 slides o 1 página escrita.  
**Estructura**:
1. **Contexto 1 slide**: "Queremos predecir churn. Datos: 2M usuarios, 6 meses".
2. **3 Hallazgos clave con gráfico**: "Hallazgo 1: 30% de churn ocurre en día 7. Oportunidad de intervención". Gráfico simple, anotado.
3. **Riesgos/Datos**: "Riesgo: `ultimo_login` tiene 40% nulos en iOS. Pedir fix a ingeniería".
4. **Recomendación**: "Go/No-go para modelado. Siguiente paso: crear feature `dias_desde_login`."

**Herramientas**: Google Slides, Notion, Quip. Gráficos de Matplotlib/Seaborn pero curados. Sin código.

**3. Dashboard interactivo: Streamlit, Dash, Looker, Tableau**  
**Cuándo**: Stakeholder quiere explorar solo. "Déjame filtrar por país y ver churn".  
**Qué lleva**: KPIs clave, filtros, drill-down. No 50 gráficos. 3 vistas máximo.  
**Ventaja**: Self-service, reduce preguntas ad-hoc.  
**Costo**: Toma 2-3 días construir. Solo si el proyecto es largo.

**4. Notebook curado para PMs técnicos**  
Jupyter/Colab pero solo con Markdown + gráficos + 1 línea de conclusión por sección. Esconde código con `# @title`.  
**Cuándo**: PM entiende datos pero no Python. Quiere ver números sin correr nada.

### Reglas para comunicar a no técnicos

1. **Empieza por la conclusión**: "El 80% del fraude viene de 3 países. Recomendamos reglas nuevas". Luego el gráfico.
2. **1 insight por gráfico**: Si tienes que explicar 5 cosas de un gráfico, está mal.
3. **Traduce métricas**: No "skew=4.2". Di "Ingreso está muy concentrado: 90% gana <50k, pero hay casos de 500k que mueven el promedio".
4. **Habla de $ y riesgo**: "Esta variable predice default" → "Esta variable nos puede ahorrar $2M/año en pérdidas".
5. **Sé honesto con límites**: "Con estos datos no podemos predecir X. Necesitamos Y". Mejor parar ahora que entregar modelo inútil.

**Flujo típico en equipo pro, 2 semanas**:
Día 1-2: Auditoría + Data Quality Report → "¿Los datos sirven?".  
Día 3-7: EDA profundo → Notebook + Feature Proposal.  
Día 8: Review con negocio → "¿Esto tiene sentido?".  
Día 9-10: Resumen ejecutivo + Slides → Alineación con stakeholders.  
Go/No-Go: Si "Go", pasas a modelado con feature store ya definido.

Si te saltas EDA o lo haces mal, el costo es modelar 1 mes para descubrir que la columna `user_id` estaba duplicada. 
