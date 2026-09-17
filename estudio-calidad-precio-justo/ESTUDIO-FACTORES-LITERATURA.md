# Estudio — qué dice la literatura sobre cíclicas, y por qué casi nada de eso se puede ver aquí

**Fecha:** 2026-09-17
**Scripts:** `factor_inversion.py`, `combinada.py`, `suelo_deteccion.py`
**Datos:** 60 Industrials con key-metrics trimestrales de FMP, 772 decisiones, 17 años (2007–2023),
universo `ciclicas_ampliado.csv` + `universo_sectorizado.csv` + `fmp_raw/`.
**Mitades:** pares = descubrimiento, impares = confirmación (regla de siempre).

---

## 0. Por qué este estudio

Petición literal del usuario: *"ponte a buscar en todas tus fuentes, libros y descubrimientos
de cosas cíclicas para ver cómo podemos subir esto ya"*. La frustración es legítima: llevamos
28 hallazgos y solo uno (C23) tiene |t| > 2.

Así que hice lo contrario de lo habitual: en vez de inventar un filtro, fui a buscar los
**efectos ya documentados y replicados por terceros** en acciones cíclicas y de capital
intensivo, y los probé uno a uno sobre nuestros datos.

El resultado tiene dos partes. La primera es que **falla el factor más prometedor**. La
segunda —y es la importante— es que descubrí **por qué tenía que fallar**, y eso reordena
toda la serie.

---

## 1. Lo que dice la literatura

### 1.1 El ciclo del capital (Marathon Asset Management / Edward Chancellor, *Capital Returns*)

La tesis, en una frase: **en los sectores intensivos en capital, la rentabilidad futura la
determina la oferta, no la demanda.** Donde entró mucho capital y se construyó capacidad,
los márgenes se hunden; donde el capital huyó y se cerró capacidad, los márgenes se recuperan.
Es exactamente la lógica de una cíclica, y es comprobable con datos contables: crecimiento del
capital invertido, capex sobre depreciación, emisión neta de acciones.

### 1.2 El anomalía de crecimiento de activos (Cooper, Gulen & Schill, 2008, *Journal of Finance*)

Es la versión académica del mismo fenómeno, y es la más fuerte que he encontrado:

- Ordenando empresas por **crecimiento total del activo del año anterior**, el decil que menos
  creció bate al que más creció por un margen del orden de **20 puntos anuales** en ponderación
  equiponderada, sobre ~40 años de datos estadounidenses.
- Funciona en grandes y en pequeñas.
- El efecto **persiste hasta cinco años** después de la medición.
- Y un detalle que encaja con nosotros: **la prima empieza en el enero siguiente al año de
  medición**, que es justo donde nosotros rebalanceamos (febrero).

Si algo tenía que funcionar en nuestro panel de cíclicas, era esto.

### 1.3 Por qué no probé más cosas

Momentum (UMD), valor (HML), inversión (CMA) y rentabilidad (RMW) ya están medidos o son
redundantes con lo que tenemos. Lo nuevo aquí era el eje de **inversión / crecimiento de
activos**, que nunca habíamos tocado.

---

## 2. El test: ¿aparece el factor de inversión en nuestros Industrials?

`factor_inversion.py`. Nueve variables construidas desde el último trimestre cerrado antes
del **15 de noviembre del año anterior** (la junta anti-look-ahead de siempre). AUC contra el
decil superior de rentabilidad. **AUC < 0,5 = crecer poco predice acabar arriba**, que es lo
que la literatura predice.

| variable | pares | impares | veredicto |
|---|---|---|---|
| crec. capital invertido 1 año | 0,504 | 0,533 | signo ok, tamaño nulo |
| crec. capital invertido 2 años (anualiz.) | 0,538 | 0,439 | **NO — cambia de signo** |
| crec. activos tangibles 1 año | 0,487 | 0,421 | signo ok, tamaño insuficiente |
| crec. activos tangibles 2 años (anualiz.) | 0,576 | 0,516 | signo **contrario** |
| crec. circulante 1 año | 0,499 | 0,495 | nada |
| capex / ventas | 0,532 | 0,570 | signo contrario |
| capex / depreciación | 0,585 | 0,541 | signo contrario |
| **ROIC (nivel)** | **0,413** | **0,445** | **replica** |
| dilución yoy (emisión neta) | 0,517 | 0,467 | **NO — cambia de signo** |
| **(control) P/S del panel** | **0,437** | **0,424** | **replica** |

**Ninguna variable de crecimiento de activos replica.** Las dos únicas que replican con tamaño
(|desviación| ≥ 0,05 en ambas mitades) son el P/S —lo que ya sabíamos, C23— y el **ROIC bajo**,
que es nuevo.

### 2.1 Por qué creo que falla el crecimiento de activos

No es que Cooper-Gulen-Schill esté mal. Es que **nuestro universo no contiene la mitad del
efecto**. La anomalía funciona en buena medida porque las empresas que se endeudan y
sobreinvierten *acaban mal* — y nuestro panel no tiene esas empresas: son parte de los **596
tickers elegibles muertos** que C25 documentó y que no están en la muestra. Medimos el factor
de inversión solo entre los que sobrevivieron a haber sobreinvertido, y entre esos el factor
no distingue nada.

Esto es una predicción comprobable, no una excusa: con un universo point-in-time que incluya
los muertos, el crecimiento de activos debería reaparecer. No lo puedo comprobar hoy.

---

## 3. El hallazgo negativo que más enseña: AUC ≠ dinero

El ROIC bajo replicaba en las dos mitades con el mismo tamaño que el P/S. Parecía un segundo
factor. `combinada.py` lo llevó a cartera:

| variante | n/año | CAGR | beta | alfa Jensen | **alfa interno** | t | pares | impares |
|---|---|---|---|---|---|---|---|---|
| **P/S bajo 25% (base, C23)** | 11 | **16,55%** | 0,99 | 4,96% | **+7,31 pp** | **2,17** | 7,9 | 6,8 |
| ROIC bajo 25% | 11 | 8,88% | 0,68 | 1,10% | **−0,55 pp** | −0,21 | 2,5 | −3,2 |
| COMBO barato + ROIC bajo 25% | 11 | 14,06% | 1,14 | 1,51% | +5,80 pp | 1,79 | 4,5 | 6,9 |
| COMBO 15% (más estrecho) | 7 | 15,09% | 1,24 | 2,23% | +7,82 pp | 1,76 | 7,6 | 8,0 |
| (familia Industrials) | 45 | 10,75% | 0,69 | — | — | — | — | — |
| (Nasdaq) | — | 12,69% | 1,00 | — | — | — | — | — |

**El ROIC bajo tiene señal de AUC y alfa interno NEGATIVO.** No es una contradicción: son dos
cosas distintas y yo las había tratado como si fueran la misma.

- **AUC contra el decil superior** mide *¿acierto la cola derecha?*
- **Alfa interno** mide *¿gano dinero de media?*

Una variable puede cargar la cola derecha **y a la vez** cargar la izquierda. El ROIC bajo hace
exactamente eso: entre las empresas poco rentables hay más multibaggers **y** más ruinas, y en
media las ruinas ganan. Por eso el CAGR del ROIC bajo (8,88%) está por debajo de su propia
familia (10,75%).

**Consecuencia de método, y va a HALLAZGOS:** el AUC contra el decil superior no vale como
criterio de selección de variables si lo que quieres es rentabilidad media. Varios barridos de
la serie (`auc_barrido.py`, `auc_ciclo.py`) usaron AUC como criterio. **Ninguna variable debería
darse por buena sin pasar por alfa interno.**

Y combinar no suma: el COMBO empeora al P/S solo, tanto en alfa Jensen (1,51% vs 4,96%) como en
beta (1,14 vs 0,99). El COMBO 15% tiene alfa interno parecido pero con 7 nombres y beta 1,24 —
más riesgo por el mismo dinero.

---

## 4. El suelo de detección — por qué "no sale nada" era el resultado esperado

`suelo_deteccion.py`. Esta es la parte que reordena toda la serie.

Pregunta: **¿cuál es el efecto anual más pequeño que este conjunto de datos puede distinguir
del ruido?** Se responde con un bootstrap: carteras **aleatorias** de n nombres/año dentro de
Industrials. Su alfa interno es cero por construcción; su desviación típica es el ruido de
medición. Con t = 2, el mínimo detectable es 2 × SE.

Dispersión transversal media dentro del año: **34,0 pp**. Es enorme, y es la causa de todo lo
que sigue.

| n/año | SE del alfa interno | mínimo detectable (t=2) |
|---|---|---|
| 7 | 2,89 pp | **5,8 pp anuales** |
| 11 | 2,21 pp | **4,4 pp anuales** |
| 22 | 1,24 pp | 2,5 pp anuales* |
| 45 | 0,31 pp | 0,6 pp anuales* |

\* Estas dos filas están infladas por **corrección de población finita**: con 45 nombres la
"cartera" *es* la familia entera, y el ruido cae a cero artificialmente. No son alcanzables.

Repitiendo con la misma dispersión pero suponiendo un universo point-in-time más ancho:

| universo N/año | n=11 | n=20 | n=45 |
|---|---|---|---|
| 45 (lo que tenemos) | 4,4 | 2,8* | — |
| 150 | 4,8 | 3,4 | 2,1 |
| 300 | 4,9 | 3,6 | 2,3 |
| 1000 | 4,9 | 3,7 | 2,4 |

**Ampliar el universo casi no ayuda.** Con 11 nombres el suelo se estanca en ~4,9 pp por muchos
nombres que haya donde elegir. Lo que manda es cuántos nombres *llevas*, no entre cuántos eliges.

Y el cuello de botella real son los **años**:

| efecto real | años de historia necesarios (con 20 nombres/año) |
|---|---|
| 3,0 pp | **26** |
| 3,5 pp | **19** |
| 5,0 pp | 9 |
| 7,3 pp | 4 |
| 10,0 pp | 2 |

Tenemos **17**.

### 4.1 Lo que esto significa, comparado con la literatura

| efecto documentado | magnitud típica | ¿visible con 17 años y 11–20 nombres? |
|---|---|---|
| valor / HML | ~3,5 pp | **no** |
| inversión / CMA | ~3,5 pp | **no** |
| rentabilidad / RMW | ~3,0 pp | **no** |
| momentum / UMD | ~7,5 pp | al límite |
| **nuestro P/S bajo en Industrials (C23)** | **7,31 pp** | **sí — por eso es lo único que vemos** |

**Este es el resultado del estudio.** Durante 28 hallazgos he ido diciendo "no sale nada". La
frase correcta es distinta: **casi todo lo que la literatura documenta está por debajo del
suelo de detección de este instrumento.** No estamos midiendo que los factores no funcionen.
Estamos midiendo que no podemos verlos.

Y explica por qué el P/S es lo único que sobrevive: no es que sea el mejor factor del mundo. Es
que es **el único lo bastante grande para asomar por encima del ruido**. Lo cual, dicho sea de
paso, también es un aviso: un efecto de 7,3 pp medido con un suelo de 4,4 pp puede ser un efecto
de 4 pp que tuvo suerte.

---

## 5. Qué hago con esto (y qué no)

**No se puede:** encontrar nuevos factores de 3–4 pp con estos datos. No es cuestión de probar
más ideas ni de ser más listo con los filtros; es aritmética del tamaño de muestra. Cualquier
variable que "aparezca" con 17 años y 11 nombres y mida menos de ~4,5 pp es ruido con buena
presentación, venga de donde venga.

**Sí se puede, y son las tres únicas salidas reales:**

1. **Aceptar C23 tal cual está** (P/S bajo dentro de Industrials) sabiendo que su alfa interno
   es sólido (+7,31 pp, t=2,17, replicado en ambas mitades) pero **su alfa contra el Nasdaq no
   lo es** (C24: t=0,48) y **no descorrelaciona**. Es un selector de acciones dentro de un
   sector, no un compartimento descorrelacionado. Sirve para elegir *qué* Industrials comprar
   si ya has decidido comprar Industrials; no sirve como argumento para no comprar Nasdaq.
2. **Llevar más nombres.** Pasar de 11 a 20 baja el suelo de 4,4 a ~3,6 pp. Va justo en contra
   del instinto de concentrar, pero es la única palanca que tenemos hoy sin comprar datos.
3. **Comprar historia con universo point-in-time** (CRSP vía WRDS, Sharadar, Norgate). Con 40
   años y muertos incluidos, el suelo baja a ~2,4 pp y **entonces sí** se podrían probar el
   crecimiento de activos, HML, CMA y RMW — y comprobar la predicción de §2.1.

---

## 6. Honestidad sobre este estudio

- El suelo de detección se calcula con la dispersión *observada* de nuestros 60 Industrials. Un
  universo distinto tendría otra dispersión y otro suelo. La magnitud (unidades de pp, no
  décimas) es robusta; el decimal no.
- Las magnitudes de la literatura (3–3,5 pp para HML/CMA/RMW, 7,5 para UMD) son órdenes de
  magnitud de primas de factor a largo plazo en EE.UU., no estimaciones de nuestro periodo.
  Sirven para situar el suelo, no como valores exactos.
- El fallo del crecimiento de activos es un **hallazgo negativo con explicación**, no un
  refutación de Cooper-Gulen-Schill. La explicación (§2.1) es comprobable y no la he comprobado.
- El ROIC quedó fuera por alfa interno negativo, no por AUC. Si alguien vuelve sobre él, que
  mire el alfa, no el AUC.
