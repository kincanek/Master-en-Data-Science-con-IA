# Sesgo algorítmico

**Sesgo algorítmico en Machine Learning** es cuando un modelo de ML produce resultados sistemáticamente injustos o discriminatorios hacia ciertos grupos de personas. No es que el algoritmo "tenga maldad", sino que aprende patrones de los datos con los que se entrena, y si esos datos reflejan prejuicios históricos, el modelo los reproduce y amplifica a escala.

### Cómo los datos de entrenamiento introducen discriminación sistémica

1. **Sesgo de muestreo/subrepresentación**: Si los datos sobrerrepresentan a un grupo y subrepresentan a otro, el modelo aprende peor para el grupo minoritario. Ejemplo: un dataset de reconocimiento facial con 80% caras blancas falla más con personas de color.

2. **Sesgo histórico**: Los datos reflejan decisiones humanas pasadas que ya eran discriminatorias. Si la policía arrestaba más en barrios negros, los datos dirán que hay más crimen ahí, aunque sea por vigilancia excesiva. El modelo aprende "barrio negro = riesgo alto" y crea un ciclo de retroalimentación.

3. **Sesgo de etiquetado**: Si quienes etiquetan los datos aplican criterios inconsistentes o estereotipos, el modelo aprende eso. En contratación, si históricamente se descartaba más a mujeres para puestos técnicos, etiquetar esos CVs como "rechazo" enseña al modelo a hacer lo mismo.

4. **Proxy discriminatorio**: Aunque quites variables como raza o género, el modelo usa variables correlacionadas: código postal, tipo de escuela, vocabulario. Así discrimina sin "decirlo" explícitamente.

### Ejemplo real documentado: COMPAS en justicia penal de EE.UU.

**Qué pasó**: Los tribunales de varios estados de EE.UU. usan COMPAS, una herramienta de evaluación de riesgo de reincidencia para decidir fianzas y sentencias.

**Daño concreto**: Un estudio de ProPublica en 2016 encontró que COMPAS clasificaba erróneamente a acusados negros como de "alto riesgo de reincidencia violenta" con el doble de frecuencia que a acusados blancos. Esto llevó a negar fianzas, sentencias más duras y más tiempo en prisión preventiva para personas que no reincidían.

**Tipo de sesgo**:
- **Sesgo histórico/de datos**: El modelo se entrenó con datos de arrestos y condenas pasadas, que ya reflejaban prácticas policiales con prejuicios raciales.
- **Sesgo de proxy**: Usaba variables como historial de arrestos, vecindario y situación socioeconómica, que están correlacionadas con raza por discriminación previa.
- **Falta de transparencia**: Northpointe, la empresa, no reveló el método para calcular las puntuaciones, lo que impidió auditarlo.

**Cómo podría haberse mitigado**:

1. **Auditoría de datos antes de entrenar**: Revisar si los datos de entrenamiento sobrerrepresentan ciertos grupos y si reflejan sesgos policiales previos. Usar datos de arresto es problemático porque miden actividad policial, no crimen real.

2. **Métricas de equidad por grupo**: No basta con medir precisión global. Hay que medir tasas de falsos positivos/negativos por raza, género, etc. COMPAS tenía precisión similar global, pero diferente distribución de errores.

3. **Intervención humana significativa**: Usar el modelo solo como apoyo, no como decisión final. Explicar por qué dio esa puntuación y permitir impugnarla.

4. **Rediseñar la variable objetivo**: Predecir "reincidencia verificada" con datos de seguimiento, no "arresto futuro". Y auditar qué variables son proxies de raza.

5. **Diversidad en el equipo y transparencia**: Equipos diversos detectan sesgos que otros no ven. Y sin transparencia, no hay rendición de cuentas.

### Otro caso breve: Contratación

Un estudio de Stanford encontró que herramientas de IA para contratación de un solo proveedor generaban "rechazo sistémico". Candidatos que aplicaban a varios puestos evaluados por el mismo algoritmo tenían más probabilidad de ser rechazados en todos, aunque fueran cualificados. El sesgo se ocultaba al agregar datos de todos los puestos juntos, pero aparecía al analizar puesto por puesto.



---

# Data Leakage

**Data leakage**, o fuga de datos, es cuando tu modelo "ve" información durante el entrenamiento que no debería tener disponible en producción. Es como darle las respuestas del examen al estudiante antes de evaluarlo. 

Por eso es tan común y peligroso: te da métricas espectaculares en validación, tipo 99% accuracy, pero en producción el modelo colapsa. Y lo peor es que el error es silencioso. Crees que tienes un gran modelo hasta que sale al mundo real y falla.

### Por qué es tan común
Porque casi siempre ocurre en pasos que parecen inocentes del pipeline. No es un bug de código obvio. Es un error de orden temporal: usar el futuro para predecir el pasado.

### Los 2 tipos principales de fuga

#### 1. Fuga de preprocesamiento / "leakage de datos"
Ocurre cuando usas información de todo el dataset, incluyendo test, para calcular transformaciones que se aplican antes de entrenar.

**Ejemplo clásico: escalar con StandardScaler**
```python
# MAL - fuga de datos
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)  # fit ve train + test
X_train, X_test = train_test_split(X_scaled)

# BIEN - sin fuga
X_train, X_test = train_test_split(X)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)  # fit solo ve train
X_test = scaler.transform(X_test)         # test solo se transforma
```

**Por qué es fuga**: Al hacer `fit` en todo X, el scaler calcula media y desviación usando el set de test. Luego cuando evalúas en test, ese set ya "contaminó" los parámetros del scaler. El modelo indirectamente vio la distribución de test. En datasets pequeños el impacto puede ser de 5-10 puntos de accuracy falsos.

**Otros casos**: Imputar valores faltantes con la media de todo el dataset, hacer selección de variables usando correlación con la etiqueta en todo el dataset, o aplicar PCA en train+test antes del split.

#### 2. Fuga conceptual / "target leakage"
Ocurre cuando incluyes como feature una variable que contiene información del target, pero que en el momento de hacer la predicción real no existiría.

**Ejemplo en predicción de crédito**: 
Si quieres predecir si un cliente hará default en 12 meses, y metes como feature `cantidad_pagada_en_mes_6`, esa variable es del futuro. En producción, cuando un cliente nuevo pide crédito, no sabes cuánto va a pagar en 6 meses. El modelo aprende: "si pagó mucho en mes 6, no hizo default". Obvio, pero inútil.

**Ejemplo en medicina**: Predecir si un paciente será hospitalizado, pero incluir como feature `dosis_de_medicamento_hospitalario`. Si ya le dieron ese medicamento, es porque ya estaba hospitalizado. Estás prediciendo el pasado.

**Ejemplo en series temporales**: Usar datos de mañana para predecir hoy. Si predices ventas del lunes e incluyes como feature el tráfico web del martes, hay fuga temporal.

### Tabla comparativa rápida

| | **Fuga de preprocesamiento** | **Fuga conceptual** |
| --- | --- | --- |
| **Qué es** | Info de test/val se filtra al entrenar | Feature usa info del futuro o del target |
| **Cuándo ocurre** | Antes del split train/test | Al diseñar las features |
| **Síntoma** | Métricas demasiado buenas en CV, mal en prod | Modelo perfecto con 1 sola variable |
| **Causa** | Orden incorrecto en pipeline | No pensar en "qué sabría en t=0" |

### Cómo prevenirlos

**Para fuga de preprocesamiento: usa Pipelines**

La regla de oro es: todo lo que aprende de los datos debe ir dentro de un pipeline y ajustarse solo en train.

```python
from sklearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

pipe = Pipeline([
    ('imputer', SimpleImputer()),
    ('scaler', StandardScaler()),
    ('model', LogisticRegression())
])

# cross_val_score hace el split antes de cada fit
cross_val_score(pipe, X, y, cv=5)  # Sin fuga
```

Así, en cada fold de validación cruzada, el scaler y el imputer solo ven el train de ese fold.

**Reglas prácticas**:
1. Split train/test/val *antes* de cualquier transformación.
2. `fit` solo en train. `transform` en train y test.
3. Para series temporales usa `TimeSeriesSplit`, nunca `KFold` aleatorio.

**Para fuga conceptual: auditoría temporal**

1. **Regla del "momento de predicción"**: Para cada feature, pregúntate: "Si este modelo estuviera en producción hoy, ¿tendría este dato disponible para este usuario?" Si la respuesta es no, hay fuga.

2. **Feature audit con timestamps**: Si tus datos tienen fechas, asegúrate que para predecir en tiempo T solo uses datos generados antes de T. Herramientas como `featuretools` o `tsfresh` tienen modos de "cutoff_time".

3. **Feature importance absurda**: Si una variable tiene 99% de importancia y es obvia, sospecha. "ID de cliente" no debería predecir churn. Si lo hace, hay fuga.

4. **Quitar IDs y proxies del target**: Códigos post-proceso, montos de pago final, diagnósticos posteriores. Todo lo que ocurra después de que el evento se define.

### Señales de alerta de que tienes fuga

1. Accuracy >95% en problemas difíciles. Casi siempre es fuga.
2. El modelo funciona perfecto en validación pero horrible en el primer día en producción.
3. Al eliminar una sola columna el modelo pasa de 99% a 60%.
4. El modelo aprende patrones que ningún humano podría: "si el ID termina en 7, es fraude".

El data leakage es el bug de un millón de dólares. Kaggle ha visto ganadores descalificados por esto. En empresas, significa lanzar un modelo a producción que no sirve.


---

# MLOps y el Modelo en Producción

**MLOps = Machine Learning + DevOps + DataOps**.

En corto: es el conjunto de prácticas, herramientas y cultura para que un modelo de ML no se quede en un Jupyter notebook, sino que llegue a producción, se mantenga vivo, y genere valor sin romperse a los 3 días.

### ¿Por qué es fundamental para pasar de investigación a producción?

En investigación tu objetivo es: "¿Este modelo puede aprender algo interesante?"
En producción tu objetivo es: "¿Este modelo puede dar predicciones correctas, rápidas, baratas, 24/7, durante meses, y si falla me entero antes que el usuario?"

La diferencia es brutal:

| **Investigación** | **Producción** |
| --- | --- |
| Dataset fijo, limpio | Datos nuevos, sucios, cambian cada día |
| 1 persona ejecuta el código | Miles de requests/seg en servidores |
| Si falla, reinicio el kernel | Si falla, pierdes dinero y confianza |
| Versiono código en mi laptop | Necesitas versionar código + datos + modelo + features |
| Evalúo 1 vez con test set | Necesitas monitorear 24/7 porque el mundo cambia |

MLOps te da el "sistema operativo" para cerrar esa brecha: CI/CD para modelos, reproducibilidad, pruebas automatizadas, deployment, monitoreo, reentrenamiento y gobernanza.

### Los 3 conceptos clave del monitoreo

#### 1. Data Drift / Covariate Shift
**Qué es**: La distribución de los datos de entrada X en producción ya no se parece a la de entrenamiento.

**Ejemplo**: Entrenaste un modelo de detección de fraude con transacciones de 2020-2022, donde el ticket promedio era $40 USD. En 2024 hay inflación y el ticket promedio sube a $80. Tu modelo nunca vio tickets de $80. Aunque la relación X→y siga igual, el modelo está operando fuera de su zona conocida.

**Por qué importa**: El modelo extrapola mal. Las predicciones se vuelven inestables.

#### 2. Model Drift / Concept Drift
**Qué es**: La relación entre X e y cambió. Los mismos inputs ahora deberían dar otro output.

**Ejemplo**: Modelo que aprueba créditos. En 2022, "tener 2 años en el empleo actual" era fuerte señal de bajo riesgo. En 2024, con layoffs masivos en tech, esa variable ya no predice igual. La regla cambió.

**Tipos**:
- **Gradual**: Cambios lentos, como preferencias de usuario
- **Sudden**: COVID, cambio de ley, campaña de marketing
- **Recurrent**: Estacionalidad, navidad vs verano

#### 3. Model Monitoring
Es el sistema que vigila 24/7 si hay data drift, model drift, o degradación de performance. No puedes esperar a que un cliente se queje. Tienes que saberlo antes.

### Estrategias que usa la industria para detectar y responder

#### A. Cómo detectar que el modelo se degrada

1. **Monitoreo de performance con ground truth retrasado**
   Es el estándar de oro, pero lento. Si predices "default en 12 meses", tienes que esperar 12 meses para saber si acertaste. Se usa para modelos de crédito, churn, etc. Calculas accuracy, precision, recall en producción con ventanas móviles. Si cae 10%, alerta.

2. **Monitoreo sin ground truth: data drift detection**
   Cuando no tienes la etiqueta rápido, monitoreas la distribución de inputs y predicciones.

   **Técnicas estadísticas**:
   - **KS Test / PSI**: Comparan distribución de cada feature en train vs prod. PSI > 0.2 = drift fuerte.
   - **Jensen-Shannon divergence**: Para distribuciones categóricas.
   - **Embedding drift**: Para texto/imágenes, comparas embeddings con distancia euclidiana.

   **Herramientas**: Evidently AI, WhyLabs, Arize, Fiddler. Te dan dashboards con alertas.

3. **Monitoreo de predicciones**
   Si tu modelo de fraude pasa de marcar 1% a 15% de transacciones como fraude de golpe, algo cambió. Monitoreas: distribución de scores, % de cada clase, latencia, tasa de nulls, volumen de requests.

4. **Shadow testing / Champion-Challenger**
   Corres el modelo nuevo "challenger" en paralelo al actual "champion" sin mostrar resultados al usuario. Comparas métricas. Si el challenger es mejor, lo promueves.

#### B. Cómo responder cuando hay degradación

1. **Alertas + Playbooks**
   Define SLOs: "Si PSI > 0.25 por 3 días, PagerDuty al equipo". El playbook dice qué hacer: investigar, reentrenar, rollback.

2. **Reentrenamiento automático**
   Pipeline que cada semana toma datos nuevos, reentrena, evalúa vs modelo actual, y si gana lo despliega. Muy común en ads, recomendaciones. Usas MLflow, Kubeflow, Tecton para orquestar.

3. **Rollback rápido**
   Si despliegas v2 y las métricas caen, tienes que volver a v1 en minutos. Por eso se versiona todo: código, datos, modelo. Blue-green deployment o canary releases.

4. **Recalibración**
   A veces no necesitas reentrenar todo. Si solo cambió la tasa base, ajustas el threshold de decisión. Platt scaling o isotonic regression.

5. **Feature Store + Data Quality**
   El 70% de los incidentes vienen de datos rotos, no del modelo. Un feature store centralizado + pruebas de calidad tipo "great expectations" detecta: "esta columna llegó con 80% nulls", antes de que mate al modelo.

### Stack MLOps típico en 2026

| **Fase** | **Herramientas comunes** |
| --- | --- |
| **Experimentación** | MLflow, Weights & Biases, Jupyter |
| **Versionado** | DVC para datos, Git para código, Model Registry |
| **CI/CD** | GitHub Actions, Jenkins → entrena + test + despliega |
| **Serving** | Seldon, KServe, Triton, endpoints de AWS/GCP |
| **Monitoring** | Evidently, Arize, WhyLabs, Prometheus + Grafana |
| **Feature Store** | Feast, Tecton, Vertex FS |

**Regla de oro de MLOps**: Si no lo puedes monitorear, no lo pongas en producción. Y si no lo puedes reentrenar en <1 día, eventualmente va a morir.

Un modelo sin MLOps es como un coche sin aceite: funciona un rato, luego se funde.
