# El eje temporal sobre 54 años: la descorrelación era la ventana

Continuación de `ESTUDIO-EJE-TEMPORAL.md`. Scripts: `largo.py`, `ventanas.py`.
Datos: `nasdaq_febrero.csv` (^IXIC, último día de cotización ≤ 15 de febrero, 1971–2026, vía FMP).

## Resumen en una frase

**La regla es la misma; la muestra pasa de 17 a 54 decisiones. Y con 54 decisiones la
descorrelación que dábamos por establecida se cae: −0,221 (p = 0,013) se convierte en
−0,081 (p = 0,154).**

---

## 1. Validación de la señal

La señal larga usa ^IXIC; la del estudio anterior usaba el QQQ implícito del panel. Antes de
usarla hay que comprobar que son la misma señal:

**Reproduce 17 de 17 las decisiones del panel en 2007–2023.** Mismos años fuera: 2008, 2009,
2016, 2023. La extensión es legítima.

## 2. La regla sobre 54 decisiones (1972–2025)

Fuera en 12 de 54 años: 1974, 1975, 1982, 1984, 1988, 2001, 2002, 2003, 2008, 2009, 2016, 2023.

| efectivo al | overlay | índice | diferencia | t pareado | correlación |
|---|---|---|---|---|---|
| 0% | 8,35% | 10,14% | **−1,79 pp** | −1,30 | 0,773 |
| 2% | 8,83% | 10,14% | **−1,31 pp** | −1,10 | 0,780 |
| 5% | 9,53% | 10,14% | **−0,60 pp** | −0,79 | 0,790 |

*El tipo sin riesgo real fue del 8–15% en 1972–1990, así que el 2% plano **infravalora** la
regla en ese tramo: el test es conservador. Aun así el signo no cambia.*

Contra el null de permutación sobre los 54 años: p(CAGR) = 0,331, **p(correlación) = 0,154**,
descorrelación real **−0,081**.

## 3. Lo que mata el resultado anterior: las 38 ventanas de 17 años

Descorrelación real medida en cada ventana solapada de 17 años, con su propio null:

| | |
|---|---|
| mediana | **−0,065** |
| rango | **[−0,403, +0,096]** |
| ventanas con p < 0,05 | **10 de 38 (26%)** |
| ventanas más fuertes que −0,14 (el número de C7) | **11 de 38 (29%)** |
| nuestra ventana 2007–2023 | −0,188 (p = 0,009) |

Y el patrón no es aleatorio, es estructural:

- **1983–2002**: descorrelación real **positiva** (+0,10 a +0,04). La regla *empeoraba* la diversificación.
- **2000–2019**: −0,22 a −0,40, todas con p < 0,01.
- **1972–1998**: −0,04 a −0,19, ninguna significativa.

Las ventanas que "funcionan" son exactamente **las que contienen 2000–2002 y 2008**. Fuera de
ellas, la regla no descorrelaciona o descorrelaciona al revés.

**Nuestra ventana está en el cuartil superior de esa distribución.** Medir −0,19 en una
ventana que contiene 2008 no es evidencia de que la regla descorrelacione: es lo que se
espera de esa ventana.

## 4. El ΔCAGR también era la ventana

38 ventanas de 17 años: mediana **−1,13 pp**, rango **[−5,80, +4,50]** pp, y la regla mejora
el CAGR en solo **17 de 38 (45%)**.

Nuestra ventana dio −2,78 pp sobre el índice: **peor que la mediana, pero dentro del rango
normal**. No fue mala suerte. El coste es real y ronda 1–3 pp.

**El rango de 10 pp entre ventanas confirma empíricamente el ±11,5 pp que `poder.py` había
predicho por aritmética antes de mirar.** El análisis de potencia no era retórica.

## 5. El mecanismo, ahora visible

La regla solo se paga en ventanas que contienen un mercado bajista **sostenido y de varios
años** (2000–2002, 2008). En ventanas sin él cuesta 3–5 pp anuales, porque las salidas son
todas en falso: 1974, 1975, 1982, 1984, 1988 fueron salidas que no evitaron nada y se
perdieron el rebote.

Es el comportamiento conocido del seguimiento de tendencia: paga la prima de un seguro casi
todos los años y la cobra dos veces por siglo. **Con horizonte de años y una sola cartera,
no hay forma de saber si te toca la ventana que cobra.**

## 6. Qué queda en pie del estudio anterior

| afirmación de `ESTUDIO-EJE-TEMPORAL.md` | estado |
|---|---|
| La descorrelación es real y robusta (−0,221, p = 0,013) | **REVOCADA.** Era la ventana: −0,081, p = 0,154 sobre 54 años |
| Es robusta a *leave-one-year-out* | **cierta pero irrelevante.** Robusta dentro de la ventana, no a cambiar de ventana |
| El ΔCAGR es un artefacto de una observación | **confirmada y ampliada**: es un artefacto de la ventana entera |
| La rentabilidad no se puede establecer con n=17 | **confirmada**, y ahora medida: rango de 10 pp entre ventanas |
| El eje temporal es lo único prometedor que queda dentro de estos datos | **REVOCADA** |

## 7. La lección que se lleva por delante a C7

`ventanas.py` dice que **el 29% de las ventanas de 17 años dan descorrelación real más fuerte
que −0,14 con una regla que sobre 54 años no descorrelaciona nada.**

−0,14 es exactamente el número de C7 ("defensivos + momento", el único candidato honesto de
la sección cruzada). **Ese número tiene la misma fragilidad**: no se midió contra ventanas
alternativas porque el panel no da más de 17 años. No queda refutado — queda sin respaldo.

## 8. Qué haría falta ahora

Ya no es "precios mensuales". Es:

1. **Aplicar este mismo test de ventanas a C7 y a todo lo que se midió sobre 17 años.** Se
   puede hacer parcialmente hoy con el índice, sin datos nuevos.
2. **Un universo point-in-time con 50 años** (CRSP vía WRDS). Es lo único que permite medir
   una estrategia de cartera, no solo una señal de índice, sobre suficientes regímenes.
3. Los precios mensuales siguen siendo útiles, pero **ya no son el cuello de botella**: el
   problema no era la frecuencia de la señal, era el número de mercados bajistas observados.
   A frecuencia mensual seguiríamos teniendo dos.
