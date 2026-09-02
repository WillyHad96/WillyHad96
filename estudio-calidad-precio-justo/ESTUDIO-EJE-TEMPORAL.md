# Estudio del eje temporal: modular la exposición por régimen

**Pre-registrado en `PREREGISTRO-EJE-TEMPORAL.md`, comiteado antes de calcular nada.**
Scripts: `poder.py`, `eje_temporal.py`, `robustez.py`, `parcial.py`. Datos: `senal_regimen.csv`.

## Resumen en una frase

**El eje temporal es lo primero de toda la serie que descorrelaciona de verdad — y lo
consigue de forma robusta y significativa — pero no llega al listón de rentabilidad, y su
efecto sobre la rentabilidad vive en una sola observación: 2008.**

---

## 1. Por qué este estudio existía

HALLAZGOS D dejaba dos caminos, y este era el único que quedaba **dentro** de estos datos:
todo lo probado antes era sección cruzada (qué comprar); faltaba probar serie temporal
(cuánto estar expuesto). C7 dejaba el listón: "defensivos + momento" era el único candidato
honesto, con descorrelación real **−0,14**.

## 2. Las reglas (cerradas por escrito, sin parámetros libres)

Cada febrero del año Y, con información disponible en ese momento:

- **R1 — momento del índice.** Dentro si el Nasdaq subió en los 12 meses previos.
- **R2 — momento del universo.** Dentro si la mediana de `mom12` del universo filtrado es > 0.

Umbral 0 en ambas, fijado por adelantado. **Una regla sin parámetros libres no necesita
muestra de descubrimiento**, así que recupera la potencia que el split pares/impares
destruiría. Fuera del mercado, efectivo al 2%.

## 3. El null correcto: permutar el vector de exposición

Éste es el punto metodológico del estudio. `poder.py` establece primero el listón del azar
en el eje temporal, que es el análogo de B2:

| p(dentro) | corr media al azar | % con corr < 0,80 |
|---|---|---|
| 0,5 | 0,587 | 93,7% |
| 0,7 | 0,726 | 70,4% |
| 0,9 | 0,856 | 23,1% |

**El 70% de los overlays aleatorios con p=0,7 bajan la correlación por debajo de 0,80, y el
8,3% cumplen a la vez correlación < 0,80 y CAGR > Nasdaq.** Probar 15 variantes y quedarse
con la mejor da éxito aparente con probabilidad **~73% sin ninguna señal**.

Por tanto el null no es "siempre invertido", sino **permutar el propio vector de exposición
entre los años**: fija *cuántas* veces sale y pregunta solo si acierta *cuándo*.

## 4. Resultados

| | base | R1 índice | R2 universo |
|---|---|---|---|
| CAGR | 14,16% | **12,01%** | 7,18% |
| correlación | 0,918 | **0,549** | 0,283 |
| beta | 1,00 | 0,43 | 0,16 |
| volatilidad | 24,1% | 17,3% | 12,6% |
| peor año | −42,5% | **−7,3%** | −7,3% |
| años dentro | 17/17 | 13/17 | 9/17 |
| **descorrelación real** | — | **−0,221** | **−0,326** |
| p(correlación) | — | **0,0130** | 0,0157 |
| p conjunta | — | **0,0049** | 0,0087 |

Nasdaq: CAGR 13,89%, peor año −28,8%.

R1 sale en **2008, 2009, 2016 y 2023**.

### El criterio pre-registrado, aplicado

| condición | R1 | R2 |
|---|---|---|
| 1. p conjunta < 0,025 | **SÍ** (0,0049) | **SÍ** (0,0087) |
| 2. CAGR ≥ Nasdaq | NO (12,01%) | NO (7,18%) |
| 3. mismo signo pares/impares | NO (+4,2 / −7,8 pp) | SÍ (−3,0 / −10,7) |
| **veredicto** | **no superviviente** | **no superviviente** |

Ninguna sobrevive. Pero *cómo* fallan importa, y no es lo mismo en las dos mitades.

## 5. Lo que sí queda establecido: la descorrelación

La descorrelación **no** depende de ningún año concreto. Leave-one-year-out sobre R1:

- rango de Δcorrelación: **[−0,473, −0,251]** — siempre fuertemente negativa, nunca cerca de cero.
- p(correlación) = 0,0130 contra el null de permutación, que ya descuenta el efecto de salir.

**−0,221 de descorrelación real frente a −0,14 del mejor candidato de sección cruzada (C7),
y con p significativa, que C7 nunca tuvo.** Es el mejor resultado de descorrelación de toda
la serie, y el único con un contraste que lo respalde.

## 6. Lo que NO queda establecido: la rentabilidad

Leave-one-year-out sobre el ΔCAGR de R1:

| se quita | ΔCAGR |
|---|---|
| — (completo) | −2,14 pp |
| **2008** | **−6,48 pp** |
| **2023** | **+0,54 pp** |
| cualquier otro | ≈ −2,3 pp |

**El signo cambia al quitar un solo año.** El efecto sobre la rentabilidad es un artefacto de
una observación, en las dos direcciones.

Y el contraste pareado (regla B4, el alfa interno e inmune) lo confirma: **−3,71 pp/año con
t = −0,79**. El coste en rentabilidad tampoco es distinguible de cero. No es que hayamos
probado que la regla pierde: es que **no se puede saber**.

## 7. Por qué la correlación se puede medir y la rentabilidad no

Es la lección que ordena todo el estudio, y se ve en un solo cálculo. Un oráculo que
esquivara **únicamente 2008**, con información perfecta:

- CAGR 14,16% → **18,07%** (**+3,91 pp**)
- correlación 0,918 → 0,861 (**−0,058**)

**Acertar una sola observación mueve la rentabilidad 3,9 pp y la correlación 0,06.** La
rentabilidad de 17 años es, en la práctica, un juego de una o dos observaciones; la
correlación es un estadístico de las 17. Por eso con n=17 la correlación es medible
(p = 0,013) y la rentabilidad no lo es (SE 5,85 pp, t = −0,79).

Esto **generaliza más allá de este estudio**: cualquier resultado de rentabilidad de esta
serie, incluidos los que salieron a favor, está a un año de distancia de cambiar de signo.

## 8. Exploratorio (NO pre-registrado): exposición parcial

Salir solo parcialmente. **No prueba nada**; dibuja el intercambio:

| exposición al salir | CAGR | corr | beta | peor año |
|---|---|---|---|---|
| siempre dentro | 14,16% | 0,918 | 1,00 | −42,5% |
| 75% | 14,01% | 0,903 | 0,86 | −31,4% |
| 50% | 13,58% | 0,848 | 0,72 | −20,2% |
| 25% | 12,92% | 0,730 | 0,57 | −9,1% |
| 0% (R1) | 12,01% | 0,549 | 0,43 | −7,3% |

Monótona, sin comida gratis. Y su pendiente **también** depende de 2008: sin ese año, salir
del todo cuesta 19,15% → 12,67% para la misma caída de correlación.

## 9. Respuesta a la pregunta del usuario

Pedías correlación baja **y** rentabilidad capaz de competir. Con estos datos:

- **La correlación baja: sí, y es lo primero de la serie que lo consigue de verdad.** 0,918 → 0,549, descorrelación real −0,22, robusta a quitar cualquier año, p = 0,013.
- **La rentabilidad que compite: no se puede establecer.** Punto estimado −2,1 pp frente a la base y −1,9 pp frente al Nasdaq, pero con un intervalo que cruza el cero de sobra y un signo que depende de 2008.

**Con 17 observaciones anuales esta pregunta no se puede cerrar**, y no por falta de ideas:
por aritmética. Ya estaba dicho en el pre-registro (§6) antes de mirar.

## 10. Qué datos harían falta

Por orden de lo que más desbloquea:

1. **Precios mensuales o diarios del universo y del índice.** Es lo que más cambia. Con
   decisiones mensuales, 2007–2023 pasa de 17 a ~200 observaciones, y una regla de tendencia
   se vuelve evaluable de verdad. Además permite medir la correlación a frecuencia mensual,
   donde B5 deja de aplicar (a frecuencia anual todo lo USA correlaciona 0,8–0,95). **Sin
   esto, ningún estudio de eje temporal puede concluir nada.**
2. **Historia anterior a 2007 con precios reales.** El panel no la tiene (§ `NOTA-PRECIOS-PLANOS-PRE-2007.md`). Añadir 1995–2006 con precios que se muevan casi duplicaría la muestra y metería dos recesiones más (2000–2002).
3. **Universo point-in-time** (Sharadar, Norgate, CRSP vía WRDS). Resuelve A1–A4 de raíz.

Fuentes 1 y 2 son baratas para el índice (cualquier serie de QQQ/^IXIC) y caras para el
universo. **Y el índice solo ya sirve para el 80% de esto**: la señal de R1 es del índice,
no del universo.

## 11. Qué haría después

1. **Bajar la señal a frecuencia mensual usando solo el índice** — barato, no exige tocar el
   panel, y multiplica por ~12 las observaciones de la señal.
2. **Medir si el ~8% del universo con `mom12 = 0` exacto rinde distinto.** Es un sesgo de
   selección con la misma forma que el centinela `'desconocido'` de A4, y está sin medir.
3. **No** probar más variantes de sección cruzada. C5, C6 y este estudio apuntan a lo mismo:
   dentro de este universo no hay colores, solo tonos.
