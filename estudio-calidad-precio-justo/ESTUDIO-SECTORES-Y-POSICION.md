# Dos estudios con los datos que ya había

Universo: panel completo 2006–2024, tickers limpios, sector asignado, `ingresos_ttm >= 1e7`,
`precio_post >= 1`, márgenes saneados. Sin restricción de capitalización (a diferencia del
estudio anterior): ~850 empresas al año en 11 sectores. Un evento por empresa y año.

---

## 1. El mito de la diversificación sectorial

### Diseño

El error habitual al medir esto es variar el número de sectores **y** el de acciones a la vez,
con lo que se acaba midiendo el efecto de tener más nombres. Aquí el número de acciones queda
**fijo en 30** y solo cambia de cuántos sectores se extraen. 120 simulaciones por cada valor
de N, sectores elegidos al azar, cartera anual equiponderada, neta de 0,60%/año.

### Resultado

| Sectores | CAGR mediano | Vol. mediana | **Sharpe mediano** | Sharpe p10 | Sharpe p90 | Peor año mediano |
|---|---|---|---|---|---|---|
| 1 | 10,74% | 26,3% | **0,328** | **0,127** | **0,618** | −40,8% |
| 2 | 10,94% | 25,1% | 0,343 | 0,192 | 0,460 | −38,2% |
| 3 | 10,71% | 24,8% | 0,351 | 0,239 | 0,473 | −38,7% |
| **4** | 11,04% | 24,8% | **0,355** | 0,237 | 0,465 | −38,2% |
| 5 | 10,66% | 25,0% | 0,356 | 0,237 | 0,467 | −38,0% |
| 6 | 10,50% | 24,9% | 0,338 | 0,223 | 0,440 | −38,0% |
| 7 | 10,82% | 25,2% | 0,344 | 0,240 | 0,463 | −37,7% |
| 8 | 10,63% | 23,8% | 0,362 | 0,265 | 0,469 | −36,7% |
| **9** | 10,91% | 24,0% | **0,366** | 0,267 | 0,463 | −37,6% |

### Lectura

**La intuición era correcta: 4 sectores dan prácticamente lo mismo que 9.** Sharpe mediano
0,355 frente a 0,366 — una diferencia de 0,011 que no significa nada. El CAGR es plano en
todo el rango (10,5%–11,0%) y el peor año apenas mejora (−38,2% frente a −37,6%).

**Pero la diversificación sectorial no hace lo que la gente cree que hace.** No sube el
retorno esperado: **reduce la dispersión del resultado**. Con un solo sector el Sharpe va de
**0,127 (p10) a 0,618 (p90)**; con nueve va de 0,267 a 0,463. El rango se estrecha de 0,49 a
0,20. Es decir, diversificar por sectores **no te hace más rico, te hace más predecible**.

Puesto de otra forma: con un sector puedes acabar con un Sharpe magnífico o con uno pésimo, y
no sabes cuál de antemano. Con muchos sectores acabas con ~0,37 casi con seguridad.

**La consecuencia práctica se combina con lo de la sección 13 de `RESULTADOS.md`:** el orden
de rentabilidad de los sectores **no persiste** (Basic Materials +35,2% → −5,1%; Consumer
Cyclical +25,0% → −17,5% entre 2007–2011 y 2012–2021). Es decir, no se puede elegir de
antemano *qué* 4 sectores. Concentrar en 4 sectores no cuesta retorno esperado, pero es
apostar a que tu elección concreta no sea de las malas — y no hay evidencia de que esa
elección se pueda hacer con criterio.

Los datos apoyan concentrar en 4–5 sectores. Lo que no apoyan es creer que se sabe cuáles.

---

## 2. ¿Añadir a lo que sube o a lo que baja?

Quintiles de rentabilidad **pasada** por año, midiendo la rentabilidad **futura** a 4
trimestres relativa al SPY. Quintiles de tamaño igual (~4.000 eventos cada uno).

**Banda de ruido a 4 trimestres: 1,37 pp** (p95, 200 permutaciones aleatorias por ticker).
Este número no existía en el estudio y hacía falta para juzgar magnitudes a este horizonte.

| Ventana previa | Q1 (peor) | Q2 | Q3 | Q4 | Q5 (mejor) | Spread Q5−Q1 |
|---|---|---|---|---|---|---|
| **Último trimestre** | −4,68% | −4,43% | −3,89% | −3,50% | **−2,05%** | **+2,64 pp** |
| **Último año** | −4,77% | −4,14% | −4,04% | −3,02% | **−2,41%** | **+2,36 pp** |
| **Últimos 2 años** | −3,71% | −3,70% | −3,34% | **−2,84%** | **−4,83%** | −1,12 pp |

### Lectura

**A 3 y 12 meses, añadir a lo que sube funciona.** Los spreads (+2,64 y +2,36 pp) son ~1,8×
la banda de ruido, y la progresión es **monótona** en los cinco quintiles, que es la señal de
que hay estructura y no una casualidad en los extremos.

**A 2 años se rompe, y de una forma más interesante que una simple reversión.** El spread
Q5−Q1 (−1,12 pp) queda **por debajo de la banda**, así que no hay reversión general que
sostener. Lo que sí ocurre es que la progresión sube hasta Q4 (−2,84%) y **se desploma justo
en Q5 (−4,83%)**. No es que los ganadores a largo reviertan: es que **los ganadores extremos
tras dos años son donde deja de pagar**.

### Respuesta operativa

Añadir a lo que sube es correcto en horizontes de 3 a 12 meses. El sitio donde conviene
recortar no es "cuando ha subido", sino **el 20% más extremo después de dos años de subida**.
"Dejar correr a los ganadores" y "rebalancear" no se contradicen: son horizontes distintos.

Aviso de tamaño: hablamos de 2,4–2,6 pp anuales sobre una banda de 1,37. Es real, pero no es
una estrategia por sí sola — es un criterio de gestión de posición, no una fuente de alfa.

---

## Nota metodológica

En la primera versión del test 2 los quintiles salían de tamaños distintos (2.475 frente a
4.486). Causa: `ntile()` coloca los NULL al final en Postgres, de modo que el quintil 5
mezclaba los valores más altos con los nulos, y al filtrarlos después quedaba un quintil
parcial. Corregido calculando `ntile` solo sobre filas no nulas. Las cifras de arriba son las
de la versión corregida.
