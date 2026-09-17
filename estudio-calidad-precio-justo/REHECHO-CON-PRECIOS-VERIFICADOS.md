# Rehecho — toda la serie que pesaba, con retornos verificados

**Fecha:** 2026-09-17
**Motivo:** el hallazgo A9 (`AUDITORIA-COLUMNA-RETORNOS.md`) demostró que `fwd_4t`, la columna
de retorno usada en **todos** los estudios anteriores, no cuadra con los precios del propio
panel. Todo lo que pesaba se vuelve a medir desde cero.
**Scripts:** `rehacer_c4.py`, `rehacer_valor.py`, `rehacer_valor_controles.py`,
`rehacer_combinada.py`, `rehacer_honesto.py`, `rehacer_resto.py`, `rehacer_factores.py`
**Base de datos nueva:** `base_corregida.csv` (13.775 decisiones, 2007–2023)

---

## 0. Qué se ha arreglado, exactamente

Tres cosas, no una:

1. **El retorno de cada acción** se recalcula como `p4/precio_post − 1`. `precio_post` está
   verificado contra FMP con error de 0,03 pp; `fwd_4t` fallaba 2,31 pp de mediana.
2. **El índice** ya no sale del panel. La columna `qqq` del panel derivaba de `fwd_4t` y
   heredaba su corrupción: la "rentabilidad del Nasdaq" implícita variaba **40 puntos entre
   acciones del mismo año**, cuando debería ser casi constante. Ahora se usan series diarias
   de **QQQ y ^IXIC** descargadas de FMP y validadas contra `nasdaq_febrero.csv` (20 de 20
   años exactos al céntimo).
3. **El índice se mide en las fechas exactas de cada posición**, no feb–feb aproximado. Cada
   acción entra un día distinto; ahora su referencia entra y sale el mismo día que ella.

Nota de comparabilidad: acciones e índices van **a precio, sin dividendos**, en ambos lados.

**Aviso importante sobre el índice.** El "Nasdaq" de los estudios viejos era el **Composite**
(^IXIC). El que se compra de verdad es el **Nasdaq-100 (QQQ)**, que en 2007–2023 rindió
**~2,9 pp anuales más**. Todo lo que sigue usa **QQQ**, que es el listón duro y honesto. Contra
el Composite, cada cifra de exceso sube ~2,9 pp.

---

## 1. La estrategia original (C4)

| | con la columna corrupta | **con precios verificados** |
|---|---|---|
| CAGR C4 | 14,16% | **16,28%** |
| CAGR del índice | 13,89% (Composite) | **13,56% (QQQ)** / 10,70% (Composite) |
| exceso sobre el índice | +0,27 pp (t=0,05) | **+2,72 pp (t=1,22)** |
| alfa de Jensen | — | **+3,41% (t=1,05)** |
| beta | — | 0,99 |
| correlación | 0,918 | **0,894** |
| alfa interno (pasa vs no pasa) | +2,98 pp (t=1,86) | **+3,73 pp (t=3,86)** |

**Lo que cambia:** el alfa interno pasa de dudoso a **claramente significativo** (t=3,86).
El filtro C4 **sí elige bien** dentro del universo: quien lo pasa rinde 10,89% y quien no,
7,16%. Eso ya no es discutible.

**Lo que no cambia:** contra el Nasdaq sigue sin establecerse (t=1,22 en exceso, t=1,05 en
alfa de Jensen). Y **la mitad impar casi no aporta** (+6,34 pp en pares, +0,49 pp en impares).

**Controles:** estable al quitar cualquier año (+1,00 pp en el peor caso, sin 2022). Y la
descorrelación es **negativa**: 0,894 observada contra 0,796 de carteras aleatorias del mismo
tamaño → C4 correlaciona **más** que el azar, no menos.

---

## 2. El efecto valor por sector — aquí está el cambio grande

Cuartil más barato por P/S dentro de cada sector, contra su propio sector (alfa interno):

| sector | n/año | CAGR | su sector | alfa interno | t | pares | impares | corr QQQ |
|---|---|---|---|---|---|---|---|---|
| **Basic Materials** | 11 | **22,36%** | 10,22% | **+12,14 pp** | **4,24** | +10,6 | +13,5 | 0,649 |
| **Financial Services** | 22 | 12,68% | 5,81% | **+6,87 pp** | **5,13** | +7,1 | +6,6 | 0,835 |
| **Industrials** | 23 | 15,15% | 11,31% | **+3,85 pp** | **2,20** | +4,8 | +3,0 | 0,742 |
| Technology | 19 | 15,23% | 17,00% | −1,77 pp | −0,77 | −4,3 | +0,4 | 0,812 |
| Consumer Cyclical | 15 | 14,25% | 15,91% | −1,66 pp | −0,70 | −1,5 | −1,8 | 0,906 |
| Healthcare | 10 | 13,39% | 16,74% | −3,35 pp | −1,03 | −7,3 | 0,0 | 0,725 |
| Energy | 8 | 5,67% | 5,50% | +0,17 pp | 0,05 | +8,0 | −5,9 | 0,460 |
| Real Estate | 8 | 2,64% | 1,04% | +1,60 pp | 0,67 | −2,1 | +5,1 | 0,746 |
| Consumer Defensive | 5 | 10,35% | 12,93% | −2,58 pp | −0,63 | −4,4 | −1,0 | 0,605 |
| Communication Services | 5 | 8,19% | 7,34% | +0,86 pp | 0,18 | −2,5 | +4,0 | 0,645 |
| Utilities | 3 | 9,30% | 6,07% | +3,23 pp | 0,83 | +7,4 | +0,2 | 0,503 |

**Corrección a C23:** el efecto valor **no es un efecto de Industrials**. Industrials es el
**tercero**, y el más flojo de los tres. Con la columna corrupta, Basic Materials y Financial
Services quedaban escondidos.

### Controles completos de los tres

**Basic Materials.** Monotonía perfecta por cuartil de P/S: 20,8% / 10,2% / 3,3% / 3,4%.
Estable quitando cualquier año (+8,62 pp en el peor caso). **Pero volatilidad 74,9% y beta
2,11.** Su +7,71 pp de CAGR sobre QQQ es **todo beta**: el alfa de Jensen es +2,35% con
**t = 0,14**. Es C22 otra vez: el CAGR ordena por beta, el alfa no.

**Financial Services.** El más consistente de toda la serie: +7,13 en pares, +6,63 en impares.
Monotonía 12,5% / 5,0% / 3,2% / 1,5%. Beta 0,91. **Pero su CAGR (12,68%) está por debajo del
QQQ (14,70%)**: elige muy bien dentro de una familia que rinde mal.

**Industrials.** La monotonía más limpia: 15,3% / 13,1% / 10,3% / 5,2%. Estable. Alfa de
Jensen +1,91% con **t = 0,30**.

**Ninguno de los tres descorrelaciona.** Descorrelación real: +0,020 (BM), +0,086 (Fin),
−0,047 (Indu). Todas dentro del ruido.

---

## 3. El test que mata la tentación de elegir sectores

Elegir "los 3 sectores buenos" mirando los 17 años es hacer trampa. El protocolo honesto:
elegir con **años pares** y medir en **impares**.

- Elegidos en pares: **Basic Materials, Energy, Utilities**.
  Medidos en impares: alfa interno **+5,50 pp, t=1,77 → no confirma**. Y **−8,13 pp contra QQQ**.
- Al revés, elegidos en impares: **Basic Materials, Financial Services, Real Estate**.
  Medidos en pares: +7,41 pp; +3,41 pp contra QQQ.
- **Coincidencia entre las dos elecciones: 1 de 3.** Solo **Basic Materials**.

**Conclusión:** el efecto valor *dentro de un sector* replica. **Cuál es el mejor sector, no.**
Lo único que eligen las dos mitades por separado es Basic Materials.

---

## 4. La configuración sin trampa: valor neutral por sector

El cuartil barato de **todos** los sectores, sin elegir ninguno:

| | n/año | CAGR | beta | alfa Jensen | alfa interno | t | pares | impares |
|---|---|---|---|---|---|---|---|---|
| barato 25% de cada sector | **130** | 14,47% | 1,25 | −1,58% | **+2,85 pp** | **3,36** | +2,44 | +3,22 |
| todos los sectores | — | 11,62% | 0,94 | −1,79% | — | — | — | — |
| QQQ | — | **14,81%** | 1,00 | 0,00% | — | — | — | — |

**Y aquí está el dato que más importa de todo el rehecho:** con **130 nombres**, el ruido de
medición baja a **SE = 0,85 pp**, o sea un **suelo de detección de 1,7 pp**. Con ese
instrumento **sí vemos** un efecto de 2,85 pp con t=3,36, replicado en ambas mitades.

Eso **corrige C31**: el suelo no es fijo en 4,5 pp. Depende de cuántos nombres lleves.

| nombres en cartera | suelo de detección |
|---|---|
| 11 | 4,5 pp |
| 20 | ~3,6 pp |
| **130** | **1,7 pp** |

**Pero no bate al Nasdaq:** −0,34 pp de CAGR, alfa de Jensen −1,58%. La beta de 1,25 se come
toda la ventaja de selección.

---

## 5. Los factores de la literatura, rehechos (C29, C30)

Sobre 60 Industrials con key-metrics y 782 decisiones verificadas:

| variable | AUC pares | AUC impares | ¿replica? | alfa interno del cuartil bajo |
|---|---|---|---|---|
| crec. capital invertido 1 año | 0,483 | 0,531 | NO | +2,47 pp (3,9 / 1,1) |
| crec. capital invertido 2 años | 0,554 | 0,463 | NO | — |
| capex / depreciación | 0,625 | 0,528 | signo ok | **−4,71 pp** (−5,2 / −4,3) |
| capex / ventas | 0,574 | 0,559 | replica, **signo contrario** | — |
| **ROIC (nivel)** | 0,408 | 0,445 | replica | **+0,29 pp** (3,3 / **−2,3**) |
| **(control) P/S** | 0,448 | 0,409 | replica | **+5,59 pp** (5,1 / 6,0) |

- **C29 se confirma**: el crecimiento de activos no aparece aquí. La explicación sigue en pie
  (faltan los 596 tickers muertos que sobreinvirtieron).
- **C30 se confirma y se refuerza**: el ROIC replica en AUC (0,408/0,445) y en dinero da
  **+0,29 pp**, con las mitades en signos opuestos (3,3 / −2,3). **AUC no es dinero.**
- **Curiosidad con signo contrario a la literatura**: capex/depreciación **bajo** pierde 4,71 pp
  en ambas mitades (−5,2 / −4,3). O sea, dentro de Industrials, **invertir poco predice mal**,
  justo lo contrario del ciclo del capital. No lo doy por hallazgo: es un solo sector y choca
  con lo documentado; lo dejo anotado.

---

## 6. Lo que sigue siendo verdad de los datos

**El centinela `'desconocido'` sigue contaminando (A4).** Con precios verificados: rinde
**1,52%** frente al **11,60%** de los sectores conocidos, **−10,08 pp anuales**. Sigue sin
poder mezclarse. Todos los análisis de este documento lo excluyen.

**Subtipos cíclicos (C20), rehechos:**

| sector | n/año | CAGR | corr QQQ | beta | alfa Jensen |
|---|---|---|---|---|---|
| Consumer Cyclical | 62 | 15,91% | 0,884 | 1,32 | −1,03% |
| Industrials | 92 | 11,31% | 0,835 | 0,79 | −0,30% |
| Basic Materials | 43 | 10,22% | 0,662 | 1,17 | −3,47% |
| Energy | 33 | 5,50% | 0,485 | 0,73 | −1,52% |

Se mantiene el patrón que el usuario detectó: **más CAGR viene con más correlación.** Energy
sigue siendo la única baja de verdad (0,485) y sigue rindiendo mal (5,50%).

---

## 7. Resumen honesto: qué ha cambiado y qué no

**Ha cambiado, y a mejor:**
1. El alfa interno de C4 pasa de t=1,86 a **t=3,86**. El filtro funciona.
2. El efecto valor es **más grande y está en otro sitio**: Basic Materials (+12,14, t=4,24) y
   Financial Services (+6,87, t=5,13) por delante de Industrials (+3,85, t=2,20).
3. El suelo de detección **no es fijo**: con 130 nombres baja a 1,7 pp y entonces sí se ven
   efectos de 3 pp.
4. La correlación de C4 baja de 0,918 a 0,894.

**No ha cambiado:**
1. **Nada bate al Nasdaq con significación estadística.** Ni una sola configuración:
   C4 (t=1,05), Basic Materials (t=0,14), Industrials (t=0,30), valor neutral (alfa negativo).
2. **Nada descorrelaciona.** Todas las descorrelaciones reales están dentro del ruido.
3. El `'desconocido'` sigue contaminando.
4. El crecimiento de activos sigue sin aparecer; el ROIC sigue sin dar dinero.

**El diagnóstico, corregido:** antes decía "no hay alfa". Con datos buenos la frase correcta
es: **hay un alfa de selección grande, real y replicado —elegir barato dentro del sector—,
pero llega acompañado de una beta de 1,2 a 2,1 que se come toda la ventaja frente al Nasdaq.**
El problema ya no es encontrar señal. Es que la señal viene envuelta en riesgo de mercado.

Eso cambia la pregunta siguiente: no "¿qué otro filtro busco?", sino **"¿cómo me quedo con la
selección sin la beta?"**.
