# Cómo está hecho exactamente, y qué queda por optimizar

## PARTE 1 — La mecánica, sin adornos

### 1.1 De dónde sale cada fila

El panel tiene **una fila por empresa y trimestre**, fechada en el **día de presentación de
resultados** (`fecha`). No hay precios diarios: solo `precio_post`, el precio en esa fecha.
Todo lo demás se deriva de ahí.

### 1.2 Cuándo se compra — y aquí hay algo que no sabía hasta ahora

```sql
row_number() over (partition by ticker, date_trunc('year',fecha) order by fecha) = 1
```

Es decir: **la primera presentación de resultados de cada empresa en cada año natural.**

Comprobado empíricamente sobre las selecciones históricas:

| Mes de entrada | n | Retorno medio | Mediana vs SPY | Bate al SPY |
|---|---|---|---|---|
| Enero | 90 | 29,10% | +4,16% | 51,1% |
| **Febrero** | **378 (65%)** | 21,99% | **+4,26%** | **55,8%** |
| Marzo | 105 | 19,99% | −0,25% | 48,6% |
| Abril–junio | 6 | — | — | — |

**El 99% de las entradas ocurre entre enero y marzo, y dos tercios en febrero.** El motivo es
que la primera presentación del año es, para la mayoría de compañías estadounidenses, el
informe del cuarto trimestre y del año completo, que sale en febrero.

**Consecuencia: en la práctica esto es una estrategia de rebalanceo en febrero.** No es
escalonada, como yo suponía. Y eso significa que **nunca se ha probado otro mes**: el diseño
lo impedía. Es una vulnerabilidad — si febrero tiene alguna particularidad (efecto enero
residual, temporada de resultados), estaría dentro del resultado sin que lo sepamos.

Marzo sale claramente peor (−0,25% frente a +4,26% de febrero), aunque probablemente sea un
efecto de composición: quien reporta tarde es un tipo distinto de compañía, no un peor mes.

### 1.3 Cómo se calcula el momentum, exactamente

```sql
m12 = precio_post / lag(precio_post, 4) − 1
```

Precio en la presentación de hoy dividido entre el precio en la presentación de hace cuatro
trimestres. Salvaguardas aplicadas:

- La distancia real entre ambas fechas debe estar entre **0,75 y 1,25 años**
- El precio actual **no** puede ser un forward-fill (`precio_post = lag(precio_post)`)

Tres características que conviene tener presentes, porque son decisiones que no se probaron:

1. **Es de presentación a presentación**, no de fecha natural a fecha natural.
2. **No se salta el último periodo.** El momentum académico estándar es "12−1": se mide de
   hace 12 meses a hace 1 mes, saltándose el mes más reciente para evitar la reversión de corto
   plazo. Aquí se incluye entero, **reacción al último resultado incluida**.
3. **Es solo precio**, sin dividendos.

*Nota de rigor:* no comprobé si el precio **retrasado** (el de hace 4 trimestres) era un
forward-fill. Solo verifiqué el actual. Es un hueco pequeño pero real.

### 1.4 El filtro de perfil, exactamente

```sql
sd_mb = stddev_samp(margen_bruto) sobre los 8 trimestres previos (incluido el actual)
sd_cr = stddev_samp(crecimiento)  sobre los 8 trimestres previos
perfil = sd_mb < mediana del año  Y  sd_cr < mediana del año
         Y sector no en ('Financial Services','Real Estate')
```

Requisitos adicionales: al menos 6 trimestres con dato válido en la ventana; margen bruto
dentro de [0,05, 0,95]; crecimiento dentro de [−0,99, 3,0].

### 1.5 La selección y los pesos

```sql
pm = percent_rank() sobre m12, dentro del año   -- calculado SOLO sobre filas con m12
selección: perfil = true  Y  pm >= 0.80
peso:      proporcional al ORDEN (rank) de m12 dentro del grupo seleccionado
```

### 1.6 La regla completa, en lenguaje llano

> Cada febrero, cuando las compañías publican su informe anual: de todas las cotizadas
> estadounidenses que valen entre 300 y 5.000 millones, quédate con las que hayan tenido el
> margen bruto y el crecimiento **más regulares de los dos últimos años** (por debajo de la
> mediana en ambas cosas), descarta bancos, aseguradoras e inmobiliarias, ordénalas por lo que
> haya subido su acción en los últimos doce meses, coge el **20% que más ha subido**, pondera
> dando más peso a las que más subieron, y **véndelo todo doce meses después.**

### 1.7 Los dos sesgos de look-ahead que quedan

1. **Los umbrales son del año en curso.** La mediana de estabilidad y el percentil 80 de
   momentum se calculan con todas las empresas del año, incluidas las que reportan después.
   Medido: **94,09% de las decisiones coinciden** al usar el umbral del año anterior, con un
   solape de listas del 81%. Pequeño, pero presente.
2. **El universo son tickers vivos hoy.** El sesgo de supervivencia, ya conocido.

---

## PARTE 2 — Factor por factor: qué se probó y qué falta

### Factor 1 · Rango de capitalización

Actual: **300 M$ – 5.000 M$ absolutos**. Probado: solo desglose por tramos, nunca como
parámetro de la estrategia.

| Prueba | Hipótesis | Prioridad |
|---|---|---|
| **Banda por percentiles en vez de dólares** | 300 M$ de 2008 no son 300 M$ de 2024: el umbral absoluto se desplaza con la inflación y con el crecimiento del mercado, así que **la estrategia está cambiando de universo sola a lo largo del tiempo** | **Alta** |
| Bandas alternativas (100M–2B, 500M–10B, 1B–20B) | ¿Dónde está el óptimo? Sabemos que el momentum decae con el tamaño, así que puede convenir bajar el techo | Alta |
| Sin techo superior | ¿Cuánto se pierde por excluir las grandes? | Media |

### Factor 2 · El filtro de estabilidad

Actual: desviación típica de margen bruto y de crecimiento en 8 trimestres, ambas bajo la mediana.

| Prueba | Hipótesis | Prioridad |
|---|---|---|
| **Desviación respecto a una TENDENCIA, no a la media** | La desviación típica penaliza a una empresa cuyos márgenes **suben de forma sostenida**, que es justo lo que queremos. Medir el residuo alrededor de una recta separaría "mejora ordenada" de "ruido" | **Alta** |
| Coeficiente de variación en vez de desviación | La desviación del margen depende del nivel del margen: un 40% de margen tiene más recorrido absoluto que un 10%. Podría estar sesgando hacia márgenes bajos | **Alta** |
| Ventanas de 4, 12 y 16 trimestres | 8 fue una elección heredada, nunca optimizada | Media |
| Umbral al 40% / 60% en vez de la mediana | ¿Más estricto es mejor? | Media |
| Solo una de las dos condiciones | Ya se vio que la estabilidad sola ≈ perfil completo; falta separar cuál de las dos manda | Media |

### Factor 3 · El momentum

Actual: 12 meses, de presentación a presentación, sin saltar periodo, solo precio.

| Prueba | Hipótesis | Prioridad |
|---|---|---|
| **Momentum "12−1"** (saltando el trimestre más reciente) | Estándar académico: evita la reversión de corto plazo. Nuestro dato de que el momentum a 3 meses también funciona sugiere que aquí quizá NO ayude, y eso ya sería informativo | **Alta** |
| **Consistencia del momentum** (*frog-in-the-pan*) | Subir un 60% en doce pasos pequeños predice mejor que subir un 60% de golpe. **Encaja exactamente con nuestro mecanismo**: si la ventaja viene de información que se difunde despacio, la subida gradual es la firma de esa difusión | **Muy alta** |
| Momentum ajustado por volatilidad (retorno / volatilidad) | Documentado como mejora sobre el momentum bruto | Alta |
| Momentum relativo al sector | La cartera tiene un 44% apostado al ciclo industrial. Medir el momentum *dentro* de cada sector eliminaría esa apuesta implícita | **Alta** |
| Ventanas de 6, 9 y 18 meses | 12 fue elección de partida | Media |
| Momentum de retorno total (con dividendos) | Requiere datos que no están en el panel | Baja |

### Factor 4 · El corte de selección

Actual: top 20%. **Bien probado** (10/15/20/30/50% + permutación a dos anchuras).

| Prueba | Hipótesis | Prioridad |
|---|---|---|
| Número fijo (25 nombres) en vez de porcentaje | El universo crece con los años: 26 nombres en 2016 y 61 en 2024. Un número fijo da una cartera de tamaño estable | Media |

### Factor 5 · La ponderación

Actual: por orden de momentum. Probadas: equiponderada, capitalización, inversa, momentum.

| Prueba | Hipótesis | Prioridad |
|---|---|---|
| Peso máximo por posición (tope del 5–8%) | Limita la concentración que ahora infla el resultado | Media |
| Ponderación por volatilidad inversa | Reduciría el peor año, que es el punto débil (−36%) | Media |

### Factor 6 · El calendario — el hueco descubierto hoy

Actual: **febrero de facto**, sin haberlo elegido.

| Prueba | Hipótesis | Prioridad |
|---|---|---|
| **Rebalanceo en otros meses** | Es el único factor de la lista **sin probar en absoluto**. Si el resultado depende de febrero, es frágil | **Muy alta** |
| **Entrada en cuatro tramos trimestrales** | Elimina la suerte de la fecha concreta y reparte el riesgo de sincronización. Es lo que haría cualquier gestor real | **Alta** |

### Factor 7 · El horizonte

Actual: 12 meses. **Bien probado** (3/6/12, con descomposición coste-señal).

| Prueba | Hipótesis | Prioridad |
|---|---|---|
| 18 y 24 meses | El análisis por evento sugería que el año 2 aún aporta, pero el backtest de cartera lo desmintió. Falta cerrarlo bien | Baja |

### Factor 8 · Exclusiones y filtros de higiene

| Prueba | Hipótesis | Prioridad |
|---|---|---|
| **Filtro de liquidez** | **Nunca se ha aplicado ninguno.** Es el mayor hueco de implementabilidad: no sabemos si estos 43 nombres se pueden comprar y vender a los costes supuestos | **Muy alta** |
| Incluir Financials y Real Estate | Se excluyeron porque el margen bruto no significa nada ahí, pero la aportación medida (+3,12 pp) estaba dentro del ruido | Media |
| Revisar `precio_post >= 1` | Sabemos que el retroajuste de contrasplit lo inutiliza: deja entrar justo lo que pretendía excluir | Media |

### Factor 9 · Verificaciones de datos pendientes

| Prueba | Hipótesis | Prioridad |
|---|---|---|
| **¿`precio_post` incluye dividendos?** | Si no, la ventaja frente al SPY está inflada en ~0,9 pp anuales. Barato de comprobar comparando una compañía de dividendo alto contra su retorno total conocido | **Alta** |
| Rehacer todo con umbrales del año anterior | El look-ahead mueve el 6% de las decisiones; conviene cerrarlo | Media |
| Comprobar el forward-fill del precio retrasado del momentum | Hueco menor de rigor detectado hoy | Media |

---

## Las cuatro que yo haría primero

1. **Filtro de liquidez** — sin esto no sabemos si la estrategia es ejecutable, y todo lo demás da igual si no lo es.
2. **Rebalanceo en otros meses y en tramos** — es el único factor sin probar, y descubrirlo hoy ha sido casualidad.
3. **Consistencia del momentum** (*frog-in-the-pan*) — es la única prueba que podría **aumentar** la ventaja, y encaja con el mecanismo que creemos que está operando.
4. **Banda de capitalización por percentiles** — corrige una deriva silenciosa que lleva diecisiete años actuando.
