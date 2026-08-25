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

### Aviso sobre el tramo micro: es el número menos fiable de la tabla, no el mejor

El +7,84 pp de las micro caps es el resultado más llamativo y **el que menos hay que creerse**.
Tres indicios, todos en la misma dirección:

| Tamaño | Tickers | % "muere" en 3 años | Mediana vs SPY | % bate SPY | Ingresos medianos |
|---|---|---|---|---|---|
| micro < 300 M$ | **480** | **8,69%** | **+4,30%** | **55,1%** | 168 M$ |
| small | 1.205 | 19,80% | −2,12% | 47,0% | 551 M$ |
| mid | 1.273 | 23,97% | −3,96% | 43,9% | 2.011 M$ |
| large | 710 | 24,98% | −5,07% | 41,3% | 7.913 M$ |
| mega | 246 | 28,17% | −4,27% | 42,0% | 35.854 M$ |

1. **Es el único tramo que bate al índice** (+4,30% de mediana, 55,1% de acierto). Las micro
   caps como clase **no** baten al S&P 500. Un tramo entero por encima del índice es firma de
   selección, no un hallazgo.
2. **Solo 480 tickers para 6.389 eventos.** Un universo micro real tiene miles de compañías con
   rotación altísima. Aquí son 480 empresas que se mantuvieron cotizando años por debajo de
   300 M$ y que siguen en un panel construido desde el universo de tickers vivos hoy. Las que
   murieron no están.
3. **La "mortalidad" va al revés**: 8,69% en micro frente a 28,17% en mega. Es imposible como
   mortalidad real — las grandes sobreviven más, no menos. Lo que mide en realidad es dónde se
   acaba la cobertura del panel para cada ticker, y confirma que el segmento micro es un
   conjunto curado de supervivientes.

A eso se suma lo obvio: con precio mediano de 8,86 $ y capitalización por debajo de 300 M$, el
supuesto de entrar y salir a 0,30% por lado no se sostiene. Aunque el efecto fuera real, no
sería capturable.

**Conclusión: el gradiente por tamaño (el momentum decae al crecer la compañía) se sostiene,
pero la magnitud concreta del tramo micro no debe usarse como estimación de nada.** El tramo
donde el efecto es a la vez creíble y operable es small–mid: +3,82 y +2,67 pp.

---

## 4. Aplicar el momentum al perfil: el primer filtro de concentración que sobrevive

El perfil opera en 300 M$–5.000 M$, justo el tramo small/mid donde el momentum es creíble
(+3,82 y +2,67 pp). La pregunta: ¿sirve para ordenar los ~212 nombres del perfil, que es
exactamente lo que no se había conseguido?

**Procedencia, que es lo que distingue esto del fracaso de Tech/Health:** el momentum no se
eligió de un menú mirando resultados sobre el perfil. Salió de un contraste independiente
sobre el universo completo, y es una de las anomalías mejor documentadas de la literatura.
Tech/Health se eligió al revés — mirando cuál de ocho candidatos puntuaba mejor — y por eso
se desmoronó al rehacer la selección con datos anteriores.

### A nivel de evento (deciles de momentum a 12 meses dentro del perfil)

| Decil | n | Mediana vs SPY | Acierto | En muestra ≤2015 | Fuera ≥2016 |
|---|---|---|---|---|---|
| 1–7 | 2.012 | −0,79% | 49,0% | +2,27 | **−3,71** |
| 8 | 279 | +1,17% | 51,3% | +1,22 | +1,17 |
| 9 | 276 | +1,31% | 52,5% | +1,93 | +0,61 |
| **10** | 275 | **+7,49%** | **57,8%** | **+7,10** | **+8,71** |

No es monótono: los deciles 1–7 están planos y **cambian de signo** entre periodos. Lo que
distingue a los tres deciles altos es que **mantienen el signo en ambas ventanas**, y el
decil 10 lo hace con una estabilidad notable (+7,10 → +8,71). Contra la banda de ruido para
submuestras de ese tamaño dentro del perfil (**2,89 pp**), el decil 10 es **2,6×**.

### A nivel de cartera (anual, neta de costes)

| Cartera | n/año | CAGR | Vol. | Sharpe | Beta | Alfa | Peor año | % años > SPY |
|---|---|---|---|---|---|---|---|---|
| PERFIL completo | 151 | 13,59% | 23,5% | 0,49 | 1,18 | +3,74% | −36,9% | 66,7% |
| **PERFIL + top 30% momentum** | 44 | 15,37% | 22,2% | **0,60** | 1,04 | +6,66% | −37,9% | 72,2% |
| **PERFIL + top 10% momentum** | 15 | **22,12%** | 26,2% | **0,77** | 1,11 | **+13,38%** | −33,4% | 77,8% |
| SPY | — | 8,98% | 18,5% | 0,38 | 1,00 | — | −41,0% | — |

Costes: 0,25%/año el perfil (rotación medida del 41%), 0,60% el top 30% y **0,90% el top 10%**
— este último equivale a 150% de rotación anual, deliberadamente conservador.

### Prueba ciega

| | PERFIL | top 30% | top 10% | SPY |
|---|---|---|---|---|
| 2007–2015 | 8,73% | **8,60%** | **12,65%** | 4,10% |
| 2016–2024 | 18,67% | 22,56% | **32,38%** | 14,09% |

**El top 10% bate al perfil en las dos ventanas; el top 30% solo en la reciente** (en la
primera queda igualado, 8,60 frente a 8,73). Eso es coherente con lo que se ve a nivel de
evento: la señal está concentrada en el decil 10, y diluirla con los deciles 8 y 9 —que solo
aportan ~+1,2 pp— la debilita.

### Veredicto, con los descuentos aplicados

**Es el primer filtro de concentración del estudio que sobrevive a la prueba ciega.** Todos
los anteriores (ocho candidatos, incluido Tech/Health con su alfa de +12%) fallaban al
rehacer la selección o al cambiar de ventana. Este no.

Pero el 22,12% de CAGR y el alfa de +13,38% **no deben tomarse como expectativa**:

1. **La ventana reciente hace casi todo el trabajo**: +3,9 pp sobre el perfil en 2007–2015
   frente a +13,7 pp en 2016–2024. La segunda mitad fue excepcionalmente favorable al
   momentum en compañías de crecimiento.
2. **15 nombres al año es poco.** El test 4 de `RESULTADOS.md` mostró que con carteras
   pequeñas la dispersión de resultados se dispara. Parte de ese 0,77 de Sharpe es
   concentración, no habilidad.
3. **El efecto es de umbral, no de gradiente.** Depende de un decil concreto, lo que es
   intrínsecamente más frágil que una señal que ordena toda la distribución.

**Uso recomendado: sobreponderar el decil superior dentro del perfil, no construir una cartera
de 15 nombres con él.** El resultado defendible es que ordenar el perfil por momentum a 12
meses aporta, no que se pueda extraer un 22% anual.

### Lo que NO se puede usar del trabajo de hoy

- **El gradiente sectorial**: ya se sabía que no persiste. Concentrar en 4–5 sectores no
  cuesta retorno, pero elegir *cuáles* no tiene apoyo empírico. Sirve como regla de
  construcción (no forzar 9 sectores), no como criterio de selección.
- **La regla de los 2 años** (recortar ganadores extremos): medida sobre el universo, no sobre
  el perfil, y con un spread por debajo de la banda de ruido. Es disciplina de cartera
  razonable, no un hallazgo.

---

## 5. Las dos pruebas que sí se podían hacer: ambas a favor

### Test A — Permutación: ¿es suerte por llevar pocos nombres?

500 carteras de **15 nombres elegidos al azar** dentro del perfil, mismo periodo (2007–2024),
mismos costes (0,90%/año), misma construcción anual equiponderada:

| | CAGR | Sharpe |
|---|---|---|
| Mediana de las 500 aleatorias | 12,70% | 0,42 |
| p90 | 15,61% | — |
| p99 | 18,73% | 0,65 |
| **Máximo de las 500** | **19,81%** | **0,72** |
| **Momentum top 10% (real)** | **21,64%** | **0,75** |
| % de aleatorias que lo igualan | **0,00%** | **0,00%** |

**Ninguna de las 500 llega.** La objeción "con 15 nombres cualquier cosa parece buena" queda
respondida: el azar con 15 nombres tocaba techo en 19,81% de CAGR y 0,72 de Sharpe, y
seleccionar por momentum lo supera. Probabilidad por debajo de 1/500.

### Test B — Ensanchar: ¿aguanta con más nombres?

| Top % por momentum | n/año | CAGR | Vol. | Sharpe | Beta | Alfa | Peor año | 2007–15 | 2016–24 |
|---|---|---|---|---|---|---|---|---|---|
| top 10% | 15 | 21,64% | 26,1% | 0,75 | 1,13 | +12,83% | −36,1% | 12,32% | 31,74% |
| top 15% | 22 | 17,96% | 23,9% | 0,67 | 1,04 | +9,45% | −34,6% | 10,72% | 25,68% |
| top 20% | 29 | 17,63% | 24,5% | 0,64 | 1,10 | +8,71% | −36,2% | 11,37% | 24,25% |
| top 30% | 43 | 14,88% | 22,1% | 0,58 | 1,04 | +6,12% | −37,8% | 8,22% | 21,96% |
| top 50% | 72 | 13,17% | 20,1% | 0,55 | 0,98 | +4,55% | −34,8% | 8,32% | 18,25% |
| SPY | — | 8,98% | 18,5% | 0,38 | 1,00 | — | −41,0% | 4,10% | 14,09% |

**Decae de forma perfectamente ordenada**: CAGR 21,64 → 17,96 → 17,63 → 14,88 → 13,17;
Sharpe 0,75 → 0,67 → 0,64 → 0,58 → 0,55; alfa 12,83 → 9,45 → 8,71 → 6,12 → 4,55.

Esa respuesta gradual es **mejor evidencia que el resultado puntual**. Si el efecto fuera
suerte concentrada en tres nombres, al ensanchar se desplomaría de golpe; aquí baja poco a
poco, que es lo que hace una señal real cuando se diluye. Y **todas las anchuras baten al SPY
en las dos ventanas**, incluida la de 72 nombres (8,32% vs 4,10% y 18,25% vs 14,09%).

Esto **corrige el diagnóstico de "umbral y no gradiente"** de la sección 4: a nivel de mediana
por decil parecía un umbral, pero a nivel de cartera la respuesta es un gradiente limpio. La
diferencia es que la cartera usa medias, y el decil superior concentra la cola derecha que la
mediana no ve.

### Qué queda en pie y qué no, tras estas dos pruebas

**Objeciones respondidas:**
- *"Es suerte por llevar 15 nombres"* → refutada por el test A.
- *"Es un umbral frágil que depende de un decil"* → refutada por el test B: hay dosis-respuesta.
- *"Solo funciona en la ventana reciente"* → **parcialmente** refutada. El top 10% bate al SPY
  por +8,2 pp en 2007–2015 y por +17,7 pp en 2016–2024. Es mejor recientemente, pero la
  ventaja existe en ambas.

**Objeciones que siguen intactas, y no se pueden tocar con estos datos:**
1. **Supervivencia.** Falta el 64% de las empresas desaparecidas, y una estrategia que compra
   lo que más ha subido es precisamente la que más se beneficia de que las burbujas que
   reventaron no estén en la muestra. Sigue siendo el problema número uno.
2. **El panel está sesgado a crecimiento**, y el momentum funciona especialmente bien ahí.
   Posible circularidad.
3. **El alfa de +12,83% del top 10% sigue siendo implausible** por sí solo. La regla 5 del
   estudio dice tratar cualquier alfa por encima del 15% como un error hasta prueba en
   contra; 12,83% está lo bastante cerca como para no celebrarlo.

**Uso defendible tras las dos pruebas: top 20–30% (29–43 nombres), con Sharpe 0,64–0,58 y alfa
entre +6% y +9%.** Conserva la mayor parte del efecto, con suficientes nombres para que el
azar no mande y sin apoyarse en la cola extrema. El top 10% es real pero su magnitud no debe
usarse como expectativa.
