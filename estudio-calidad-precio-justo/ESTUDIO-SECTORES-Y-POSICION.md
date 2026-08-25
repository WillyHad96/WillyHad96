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

---

## 3. El momentum por tamaño: el efecto es de las pequeñas

**Aclaración previa:** los dos estudios anteriores ya usaban el panel **completo**, sin filtro
de capitalización — a diferencia del estudio de calidad, que sí estaba acotado a 300 M$–5.000 M$.
Aun así, el agregado escondía una diferencia grande por tamaño.

Momentum a 12 meses, rentabilidad futura a 4 trimestres relativa al SPY, quintiles calculados
**dentro de cada tramo de capitalización** y por año:

| Tamaño | n | Tickers | Q1 (perdedoras) | Q3 | Q5 (ganadoras) | Spread Q5−Q1 | % bate SPY |
|---|---|---|---|---|---|---|---|
| micro < 300 M$ | 1.345 | 369 | +1,57% | +1,94% | **+9,41%** | **+7,84 pp** | 55,3% |
| small 300 M–2.000 M$ | 6.427 | 1.055 | −4,27% | −4,55% | −0,45% | **+3,82 pp** | 46,3% |
| mid 2.000–10.000 M$ | 7.169 | 1.158 | −5,63% | −4,44% | −2,96% | **+2,67 pp** | 44,2% |
| large 10.000–50.000 M$ | 4.031 | 638 | −8,08% | −4,31% | −6,17% | +1,91 pp | 40,9% |
| mega > 50.000 M$ | 1.432 | 210 | −4,48% | −6,15% | −2,36% | +2,12 pp | 41,4% |

Banda de ruido a 4 trimestres: **1,37 pp**.

### Lectura

**El momentum decae monótonamente con el tamaño**: +7,84 → +3,82 → +2,67 → +1,91 → +2,12.
En micro, small y mid es inequívoco (5,7× / 2,8× / 1,9× la banda). En large y mega queda en
1,4–1,5× la banda, al borde.

**Y en los tramos grandes ni siquiera es monótono**, que es lo que decide el asunto:

- large: Q1 −8,08 → **Q3 −4,31** → Q5 −6,17. El del medio es el mejor.
- mega: Q1 −4,48 → **Q3 −6,15** → Q5 −2,36. El del medio es el peor.

Sin progresión ordenada, un spread entre extremos de ~2 pp no es una señal: es ruido en las
puntas. En el agregado la progresión sí era monótona en los cinco quintiles, pero ese orden
lo aportaban las pequeñas.

### Consecuencia práctica

**La regla "deja correr lo que sube, no promedies a la baja" está sostenida por datos en
micro, small y mid. En large y mega, este panel no la sostiene.**

Quien opere mayoritariamente en compañías grandes no debería aplicar la regla como si
estuviera demostrada: en ese tramo el comportamiento pasado a 12 meses no ordena el futuro.

### Alcance del "universo completo"

Conviene ser preciso con qué significa aquí "todo el universo". El panel tiene 6.967 tickers,
de los cuales en este contraste aparecen 210 mega caps y 638 large caps. Es cobertura
suficiente para medir, pero **no es el mercado estadounidense entero**: el panel se construyó
alrededor de un cribado de crecimiento, así que sobrerrepresenta compañías en crecimiento e
infrarrepresenta las maduras y de valor. Para large y mega, además, se suma el problema ya
conocido de supervivencia.
