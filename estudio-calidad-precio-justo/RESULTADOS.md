# RESULTADOS — ¿Calidad a precio justo bate a barato y aburrido?

Estudio ejecutado el 2026-08-17 sobre `hypergrowth_panel` (Tryding AI).
Pre-registro congelado en `PREREGISTRO.md` **antes** de calcular ningún contraste.

---

## Resumen ejecutivo

**Munger tenía razón sobre la calidad, pero por un motivo distinto al que dice la tesis
— y "precio justo" no es la parte que funciona.**

1. **La sospecha de la vara de medir (H2) era correcta como mecanismo y falsa como
   conclusión.** El P/S sí descarta sistemáticamente el margen alto: solo el **9,8%** de
   las empresas con margen bruto >50% cae en el tercil barato por P/S, frente al **29,2%**
   por P/GP. El sesgo de selección es real y grande. Pero al corregirlo **el resultado no
   cambia**: el margen alto sigue rindiendo peor (−11,3% vs −5,0% a 3 años), incluso
   dentro del mismo tercil de P/GP. Era un artefacto de selección, no de resultado.

2. **La calidad paga muchísimo; el precio pagado por la calidad casi no importa.**
   A 5 años, dentro del grupo de calidad el tercil de valoración es irrelevante
   (−3,0% / −4,5% / +1,3% de barato a caro). Dentro del grupo mediocre es decisivo
   (−6,1% / −21,3% / **−29,3%**). El precio protege al mediocre; la calidad se paga sola.

3. **H3 tal y como se pre-registró FRACASA.** "Calidad a precio justo (T2) vs mediocre y
   barato (T1)" da +4,13 pp (t=0,85, 10/15 años) — dentro del ruido. La comparación
   pre-registrada enfrentaba el peor tercil de calidad contra el mejor de mediocre.

4. **El control negativo (H5) avisa de un problema real de significación.** La inicial del
   ticker (A–M vs N–Z), que no debería aportar nada, produce −5,3 pp. Un test de
   permutación con 300 particiones aleatorias por ticker (sección 6) fija la banda de ruido
   real en **5,77 pp al 95%**: el control quedó en el percentil 94, es decir, mala suerte y
   no un fallo estructural, pero **todo efecto por debajo de ~5,8 pp en este panel es
   indistinguible del ruido**. Eso invalida la H3 pre-registrada (+4,13 pp) y confirma la
   principal (+19,9 pp, que **ninguna de las 300 permutaciones alcanza**, p < 0,0033).

5. **El listón del estudio anterior no se replica.** Su perfil "barato y cíclico"
   (CAGR 18,15%, alfa +9,72%, Sharpe 0,60) se reconstruye aquí como CAGR 13,61%,
   **alfa +0,75%** y **Sharpe 0,28**. La calidad gana la comparación de riesgo
   (Sharpe 0,42, beta 1,05, volatilidad 21% frente a 41%) pero **no llega al 0,60**.

---

## 0. Calidad de datos: 6 defectos confirmados + 2 nuevos

Los seis del brief se confirmaron todos. Aparecieron **dos más, ambos existenciales**
para esta pregunta en concreto:

| # | Defecto nuevo | Evidencia | Impacto |
|---|---|---|---|
| **7** | `margen_bruto` fuera de [0,1] | máx. **64.984**, mín. **−15.422.466**; 8,2% de filas | `P/GP = multiplo_ps / margen_bruto` explota. Sin filtrar, la métrica central del estudio es basura |
| **8** | Reporte **semestral** en parte del panel | p95 del salto de 8 filas = **4,000 años exactos**; afecta al 15,8% | `lead(precio_post, 8)` mide 4 años en vez de 2. Encadenar por offset sin verificar fecha mezcla horizontes |

Además, la historia utilizable **empieza en 2005**, no en 1995: en 2001 hay 179 filas con
`fwd_4t`, en 2004 hay 1.690 y en 2006 ya 7.596. El estudio es 2005–2025; no cubre el
pinchazo puntocom.

## 1. Requisito previo: retornos a 8/12/20 trimestres

**Resuelto.** La reconstrucción limpia da medianas de **1,0977× a 2 años, 1,1447× a 3 y
1,2401× a 5**, monotónicas y creíbles — frente al **1,000× exacto a 5 años** que delató la
contaminación del estudio anterior. Procedimiento:

- descartar tramos con `precio_post = lag(precio_post)` en **cualquiera** de los dos extremos
  (28,3% de las filas del panel están forward-filled);
- exigir `(fecha_fin − fecha_ini)/365,25` dentro de ±0,25 años del objetivo (neutraliza el defecto 8);
- SPY encadenado geométricamente por tramos de 4T con `spy = fwd_4t − fwd_4t_rel_spy`.

Validación del benchmark contra la realidad: cohortes de 2007 → −14,3%, 2008 → −19,7%,
2009 → +29,4%, 2020 → +33,3%, 2021 → −1,1%. Correcto.

Cobertura: **52.425 eventos / 1.411 tickers**; 30.446 con retorno limpio a 5 años.

### El límite que no se puede arreglar: supervivencia

**La mortalidad a 5 años dentro del universo es 0,0% en todos los grupos y sectores.**
No es que el filtro la elimine: el panel sencillamente **no contiene empresas muertas** en
este tramo de capitalización (solo 25 tickers de 6.665 desaparecen antes de 2015). El
panel está construido desde un universo de tickers vivos hoy y rellenado hacia atrás.

Consecuencia honesta: **los niveles absolutos a 3–5 años están inflados** y no son
utilizables como expectativa de rentabilidad. La comparación **entre grupos** sí es
utilizable, y además el sesgo juega **en contra** de la conclusión: las quiebras que faltan
son desproporcionadamente del grupo mediocre, así que la ventaja real de la calidad es
probablemente **mayor** que la medida.

## 2. H1 — control de replicación: **PASA**

Barato bate a caro con `multiplo_ps`, en los dos periodos y en los dos horizontes.

| Periodo | Vara | T1 barato (4T) | T3 caro (4T) | T1 (12T) | T3 (12T) |
|---|---|---|---|---|---|
| 2005–2012 | P/S | +3,3% | −1,1% | +9,0% | −1,8% |
| 2013–2025 | P/S | −2,7% | −5,6% | −8,0% | −18,7% |

El pipeline reproduce el resultado conocido. Se puede seguir.

## 3. H2 — la vara de medir: **REFUTADA** (pero el mecanismo era real)

Criterio pre-registrado: con P/GP la ventaja del barato debía caer a **menos de la mitad**.

| Periodo | Vara | Spread T1−T3 a 4T | Spread T1−T3 a 12T |
|---|---|---|---|
| 2005–2012 | P/S | 4,4 pp | 10,8 pp |
| 2005–2012 | **P/GP** | 4,5 pp | **14,1 pp** (mayor) |
| 2013–2025 | P/S | 2,9 pp | 10,7 pp |
| 2013–2025 | **P/GP** | 3,7 pp | 8,4 pp |

No cae a la mitad: se mantiene o crece. **H2 refutada.**

Lo que sí se confirma es el mecanismo de selección que motivaba la sospecha:

| Grupo | % en tercil barato por **P/S** | % en tercil barato por **P/GP** | Mediana 12T |
|---|---|---|---|
| Margen bruto >50% | **9,8%** | **29,2%** | −11,3% |
| Margen bruto <30% | **65,5%** | 35,6% | −5,0% |

Filtrar `multiplo_ps < 3` **sí** expulsaba a los negocios de margen alto — el brief tenía
razón. Pero corregida la vara, el margen alto sigue rindiendo peor, también **dentro** del
tercil barato de P/GP (−4,5% vs +1,8%). El artefacto estaba en la selección, no en la conclusión.

## 4. H3 — la tesis de Munger: **matizada**

Mediana de retorno relativo al SPY, por grupo y tercil de P/GP (universo completo):

| Grupo | Tercil P/GP | P/GP mediano | 4T | 8T | 12T | 20T |
|---|---|---|---|---|---|---|
| CALIDAD | T1 barato | 2,16 | +0,2% | +2,3% | +2,7% | **−3,0%** |
| CALIDAD | T2 justo | 4,07 | −0,4% | −1,6% | −1,6% | **−4,5%** |
| CALIDAD | T3 caro | 7,22 | +0,8% | +0,3% | +2,4% | **+1,3%** |
| MEDIOCRE | T1 barato | 2,32 | −1,5% | −3,9% | −5,0% | **−6,1%** |
| MEDIOCRE | T2 | 5,32 | −5,0% | −10,7% | −14,6% | **−21,3%** |
| MEDIOCRE | T3 caro | 12,82 | −6,2% | −11,8% | −18,0% | **−29,3%** |

Dos lecturas, y la segunda es la importante:

- **Como se pre-registró (CALIDAD-T2 vs MEDIOCRE-T1): fracasa.** +4,13 pp de media anual,
  t=0,85, 10/15 cohortes, p=0,30. Y el signo a 4T ya era positivo, cuando se predijo ≤0.
- **Como fenómeno (CALIDAD vs MEDIOCRE): abrumador.** +19,86 pp, t=5,55,
  **15 de 15 cohortes positivas** (p=0,0001).

La forma correcta de enunciar el hallazgo no es "calidad a precio justo gana", sino:
**el precio importa casi solo cuando el negocio es mediocre.** En calidad, pasar del tercil
barato al caro cuesta ~0 pp a 5 años; en mediocre cuesta **23 pp**.

Estabilidad temporal (**H6: pasa**) — el patrón se repite en los dos periodos:

| Grupo · tercil | 2005–2012 | 2013–2025 |
|---|---|---|
| CALIDAD T1 / T2 / T3 | +13,8% / +18,9% / +19,1% | −11,5% / −16,5% / −8,3% |
| MEDIOCRE T1 / T2 / T3 | +9,8% / −11,6% / −15,9% | −15,9% / −26,3% / −34,8% |

Colas: la calidad tiene menos desastres (<−50%) en todos los cortes —
3,8–5,3% frente a 7,0–14,8% en 2005–2012; 10,9–12,7% frente a 13,7–19,0% en 2013–2025.

### Qué componente de "calidad" hace el trabajo

| Condición | n (sí) | Mediana sí | Mediana no | Diferencia |
|---|---|---|---|---|
| **E1 ESCALABLE** (lista sección 8) | 603 | +5,7% | −14,4% | **+20,2 pp** |
| Q5 crecimiento consistente | 3.739 | −6,6% | −18,8% | **+12,3 pp** |
| Q3 dilución < 2% | 5.117 | −9,3% | −20,0% | **+10,7 pp** |
| Q4 margen bruto estable | 3.739 | −7,5% | −17,9% | **+10,4 pp** |
| Q2 margen operativo mejora | 3.910 | −11,9% | −14,2% | +2,3 pp *(ruido)* |
| Q1 rentable sostenido | 5.488 | −13,9% | −9,7% | −4,2 pp *(ruido)* |

**La "calidad" que paga es previsibilidad y no diluir, no rentabilidad.** Ser rentable de
forma sostenida (Q1) no aporta nada — y mejorar el margen operativo (Q2) tampoco. Ambos
caen dentro de la banda de ruido de ±5,3 pp establecida por el control negativo.

Por sectores, la calidad gana en **7 de 9**. Falla justo donde el margen bruto no significa
nada: Financial Services (−27,3% vs −21,8%) y Real Estate (−46,4% vs −36,5%), más Consumer
Cyclical (−4,7% vs +2,8%). Neutralizando por sector el efecto baja de +19,9 a **~+12,5 pp**:
alrededor de un tercio era composición sectorial.

## 5. H4 — riesgo: la calidad gana la comparación, pero no llega al listón

Cartera anual equiponderada, ~60–90 nombres, neta de 0,60%/año de costes, 2007–2024 (18 años):

| Cartera | CAGR | Volatilidad | Sharpe(g) | Beta | Alfa Jensen | Peor año |
|---|---|---|---|---|---|---|
| **CALIDAD (todas)** | 10,91% | **21,0%** | **0,42** | **1,05** | +1,29% | −38,3% |
| CALIDAD T1+T2 | 10,71% | 23,0% | 0,38 | 1,12 | +0,79% | −40,1% |
| CALIDAD T2 "precio justo" | 8,19% | 19,8% | 0,31 | 0,84 | +0,16% | −32,8% |
| **MEDIOCRE T1 "barato"** | **13,61%** | **41,4%** | **0,28** | **1,78** | +0,75% | −39,9% |
| SPY | 9,46% | 18,9% | 0,39 | 1,00 | — | −39,1% |

- **La parte de H4 que se cumple:** la calidad da mejor Sharpe que el barato (0,42 vs 0,28)
  con **la mitad de volatilidad** y beta 1,05 frente a 1,78. Exactamente la forma de la
  hipótesis: menos retorno, mucho menos dolor.
- **La parte que no se cumple:** Sharpe 0,42 < **0,60**, y el peor año (−38,3%) no mejora
  el −39,4% del listón. En 2008 no protegió nada.
- **El listón no se replica.** Reconstruido con el mismo pipeline, el perfil barato da
  alfa **+0,75%**, no +9,72%. Un alfa de +9,72% con beta 1,25 sostenido era, como avisaba
  la regla 5, demasiado bonito. Aviso: aquel backtest usaba ~6 posiciones y este ~70, así
  que **el 0,60 no es directamente comparable**; la comparación válida es la interna
  (0,42 vs 0,28), que sí favorece a la calidad.
- Fuera de muestra (2017–2024) la calidad rinde 11,48% con **10,7%** de volatilidad frente
  al 13,01% del SPY con 12,1%: se queda por detrás del índice, con menos riesgo.

## 6. H5 — control negativo: **FALLA** (el resultado más valioso)

La inicial del ticker no debería predecir nada:

| Contraste | Media | t | Cohortes positivas | p (signos) |
|---|---|---|---|---|
| CALIDAD − MEDIOCRE | **+19,86 pp** | 5,55 | **15/15** | 0,0001 |
| CALIDAD-T2 − MEDIOCRE-T1 (H3 pre-registrada) | +4,13 pp | 0,85 | 10/15 | 0,30 |
| **A–M − N–Z (ruido puro)** | **−5,33 pp** | −1,82 | 3/15 | **0,0352** |

Una variable sin contenido económico alcanza p<0,05. La causa es que 15 cohortes anuales
solapadas y correlacionadas entre sí no son 15 observaciones independientes. **La lectura operativa:** en este panel,
**nada por debajo de ~5,8 pp debe creerse**. Eso descarta la H3 pre-registrada (+4,13) y
Q1/Q2 como componentes, y deja en pie el efecto principal y E1/Q3/Q4/Q5.

### Banda de ruido medida por permutación (300 particiones aleatorias por ticker)

El test de signos asume independencia que estos datos no tienen. Repitiendo el contraste
con 300 particiones aleatorias del universo **por ticker** (preserva el solapamiento y la
correlación entre cohortes) se obtiene la distribución nula real:

| Percentil del efecto espurio | pp |
|---|---|
| p50 | 1,99 |
| p90 | 4,90 |
| **p95** | **5,77** |
| p99 | 7,31 |
| máximo de 300 | 8,47 |

- Efecto principal (19,86 pp): **0 de 300** permutaciones lo alcanzan → **p < 0,0033**.
- Control A–M/N–Z (5,33 pp): lo superan el 6,3% → p ≈ 0,06. Estaba en el borde, no roto.
- H3 pre-registrada (4,13 pp): lo supera el 16% → **ruido**, confirmado.

## 7. Backtest ciego

Congelando el diseño con datos ≤2016 y evaluando en cohortes 2017–2021:

| | En muestra 2007–2016 | Fuera de muestra 2017–2021 |
|---|---|---|
| CALIDAD − MEDIOCRE | +23,11 pp | **+13,34 pp** |
| CALIDAD-T2 − MEDIOCRE-T1 | +4,61 pp | +3,16 pp |

El efecto principal se degrada un 42% pero sobrevive holgadamente por encima de la banda
de ruido. La versión pre-registrada sigue dentro del ruido dentro y fuera de muestra.

## 8. Veredicto

| Hipótesis | Resultado |
|---|---|
| H1 replicación | **PASA** |
| H2 la vara de medir | **REFUTADA** como conclusión; **confirmada** como sesgo de selección |
| H3 Munger, pre-registrada | **FALLA** (+4,13 pp, dentro del ruido) |
| H3 como fenómeno | **CONFIRMADA con fuerza** (+19,86 pp, 15/15, sobrevive fuera de muestra) |
| H4 riesgo | **PARCIAL**: gana al barato en Sharpe y beta; no alcanza el listón 0,60 |
| H5 control negativo | **FALLA** — banda de ruido ≈ 5 pp |
| H6 contaminación | **PASA** — efecto presente en los dos periodos |

**Respuesta a la pregunta del estudio:** en small caps de 300 M$–5.000 M$, "calidad a
precio justo" **no** bate a "mediocre y barato" de forma fiable — esa comparación concreta
(+4,1 pp) es indistinguible del ruido. Lo que sí bate, y por mucho, es **la calidad a
cualquier precio razonable** frente a la mediocridad a cualquier precio (+19,9 pp a 5 años).
Y el corolario práctico invierte la intuición de Munger: **el precio de entrada es una
protección que necesita el negocio mediocre y de la que el negocio de calidad puede
prescindir.** Pagar de más por un mediocre cuesta 23 pp a 5 años; pagar de más por uno
bueno, esencialmente nada.

Con dos límites que conviene no olvidar: los niveles absolutos están inflados por un panel
sin empresas muertas, y "calidad" aquí significa **consistencia y no dilución**, no
rentabilidad ni margen alto — el margen alto, medido correctamente con P/GP, **sigue
rindiendo peor**.

## 9. Aviso de seguridad (sin resolver)

RLS sigue desactivado en `hypergrowth_panel` y otras 8 tablas: cualquiera con la anon key
puede leer y escribir todo. No se ha tocado, según lo indicado. La remediación
(`ALTER TABLE ... ENABLE ROW LEVEL SECURITY` + políticas) es decisión del usuario;
activarla sin políticas bloquearía todo acceso.

## 10. Desviaciones del pre-registro

1. Los umbrales de Q4/Q5 se calculan como mediana **por año** en vez de mediana global,
   para eliminar look-ahead entre periodos. Es más estricto que lo pre-registrado.
2. Se añadió el filtro `margen_bruto ∈ [0,05, 0,95]` (defecto 7), imprescindible para que
   P/GP tenga sentido, y la verificación de distancia temporal (defecto 8).
3. El periodo 1995–2004 se descarta por falta de datos, no por decisión de diseño.


---

## 11. El perfil operativo (añadido tras los resultados, con prueba ciega)

La atribución por componentes dice que Q1 (rentable) y Q2 (margen op. mejorando) no aportan
nada, y que los sectores donde el margen bruto no significa nada (Financial Services, Real
Estate) rompen el efecto. El perfil que queda al quitar lo que no funciona:

```
PERFIL = dilucion_yoy < 2%
       Y desviacion de margen_bruto en 8T por debajo de la mediana del anio
       Y desviacion de crecimiento en 8T por debajo de la mediana del anio
       Y sector NOT IN ('Financial Services','Real Estate')
       (universo: 300 M$-5.000 M$, sector asignado, tickers limpios)
```

Es **más simple** que la definición pre-registrada (3 condiciones en vez de 5), da **más
nombres** (~90–143 al año frente a 35–80) y es **más robusto**:

| | Efecto 20T vs resto | Cohortes positivas |
|---|---|---|
| En muestra 2007–2016 | +19,25 pp | 10/10 |
| **Fuera de muestra 2017–2021** | **+18,72 pp** | **5/5** |
| Total | +19,07 pp (t=10,12) | **15/15** |

**Degradación fuera de muestra: 3%.** La definición pre-registrada de 5 condiciones se
degradaba un 42% (23,11 → 13,34 pp). Quitar los dos componentes que eran ruido no empeoró
el resultado: lo estabilizó. El efecto es **3,3× la banda de ruido** de 5,77 pp.

Como cartera anual equiponderada (2007–2024, neta de 0,60%/año):

| Cartera | CAGR | Vol. | Sharpe | Beta | Alfa | Peor año | % años > SPY |
|---|---|---|---|---|---|---|---|
| **PERFIL** | **12,91%** | 23,5% | **0,46** | 1,16 | **+2,97%** | **−36,2%** | 61,1% |
| CALIDAD 5/5 | 10,91% | 21,0% | 0,42 | 1,05 | +1,29% | −38,3% | 55,6% |
| MEDIOCRE-T1 "barato" | 13,61% | 41,4% | 0,28 | 1,78 | +0,75% | −39,9% | 44,4% |
| SPY | 9,13% | 18,7% | 0,38 | 1,00 | — | −41,1% | — |

Es la mejor variante del estudio: bate al SPY en CAGR (12,91% vs 9,13%), en Sharpe
(0,46 vs 0,38) y **en el peor año** (−36,2% vs −41,1%), con alfa +2,97%. Sigue **sin
alcanzar el 0,60** del listón previo — pero aquel se midió sobre ~6 posiciones y este sobre
~100, y el alfa de +9,72% de aquel no se replica en ninguna reconstrucción.

**Aviso de sobreajuste:** este perfil se define *después* de ver la atribución de
componentes, así que la prueba 2017–2021 es su única validación genuinamente ciega. Que
apenas se degrade (3%) es la mejor señal disponible, pero no sustituye a una validación
en datos nuevos.

Combinar el perfil con la lista ESCALABLE deja solo 3–11 nombres al año y el resultado se
vuelve errático (+175% en 2008, −41% en 2021): **muestra insuficiente, no usable**.

---

## 12. Los siete tests de seguimiento

Ejecutados en el orden propuesto. Banda de ruido de referencia: **5,77 pp** (sección 6).

### Test 1 — Descomposición del retorno a 5 años

`ln(P₂₀/P₀) = ln(Δmúltiplo) + ln(Δventas) − ln(Δacciones)`, medias de logaritmos
(descomponen exactamente), retorno absoluto:

| Grupo | Tercil P/GP | Total | por múltiplo | por ventas | **por acciones** |
|---|---|---|---|---|---|
| PERFIL | T1 barato | +61,7% | +33,2% | +25,9% | **−3,6%** |
| PERFIL | T2 | +60,8% | +18,2% | +38,4% | **−1,7%** |
| PERFIL | T3 caro | +70,0% | +8,7% | +58,9% | **−1,6%** |
| RESTO | T1 barato | +51,0% | +35,7% | +26,6% | **−12,1%** |
| RESTO | T2 | +31,7% | +2,2% | +47,6% | **−12,7%** |
| RESTO | T3 caro | +22,8% | **−19,5%** | +86,6% | **−18,3%** |

**Este es el mecanismo del estudio entero, y tiene tres piezas:**

1. **La dilución es el asesino.** El resto pierde 12–18 pp de retorno a 5 años emitiendo
   acciones; el perfil pierde 1,6–3,6 pp. Ahí está, casi entera, la diferencia entre ambos.
2. **Por qué la valoración no importa en el perfil:** al pagar más, la aportación del
   múltiplo cae (+33,2 → +8,7) pero el crecimiento de ventas sube (+25,9 → +58,9) y **se
   compensan casi exactamente**. Pagas múltiplo más alto a cambio de más crecimiento: es
   un intercambio justo.
3. **Por qué sí importa en el resto:** el mediocre caro **crece las ventas más rápido que
   el bueno caro** (+86,6% vs +58,9%) y aun así rinde un tercio. Ese crecimiento lo compra
   emitiendo acciones (−18,3%) y el mercado se lo des-valora encima (−19,5%).

El mediocre caro no fracasa por no crecer. Fracasa porque **paga su crecimiento con
acciones y el múltiplo se desinfla**.

### Test 2 — ¿Dónde está el techo de P/GP? No aparece

Deciles de P/GP **dentro del perfil**:

| Decil | P/GP mediano | P/S mediano | Mediana rel20 | Bate SPY | % desastre |
|---|---|---|---|---|---|
| 1 (más barato) | 1,10 | 0,31 | **+1,0%** | 50,9% | **21,1%** |
| 2 | 1,91 | 0,58 | −3,5% | 48,0% | 17,7% |
| 3 | 2,47 | 0,76 | −6,4% | 46,6% | 19,5% |
| 4 | 2,91 | 0,83 | +8,5% | 54,7% | 14,5% |
| 6 | 3,90 | 1,21 | +8,5% | 53,2% | 15,8% |
| 8 | 5,37 | 1,69 | +7,6% | 55,1% | 13,2% |
| 10 (más caro) | 10,33 | 3,69 | +5,4% | 55,6% | **12,3%** |

**No hay techo hasta P/GP ≈ 10.** Los deciles 4–10 rinden todos entre +5 y +8,5% sin
tendencia a empeorar. Lo que sí hay es un **suelo**: los deciles 1–3 (los más baratos) son
los peores, y la tasa de desastre cae monótonamente con el precio, de **21,1% a 12,3%**.
Dentro de la calidad, lo barato es trampa de valor.

Matiz de rigor: las diferencias de retorno entre deciles (4,4 pp entre D1 y D10) están
**dentro de la banda de ruido**. Lo robusto aquí es el gradiente de la tasa de desastre,
no el de la mediana.

### Test 3 — ¿Basta con la dilución sola? No, y sobra

| Definición | Efecto 20T | t | Cohortes | En muestra | Fuera | Nombres/año |
|---|---|---|---|---|---|---|
| A. Dilución <2% sola | +13,18 pp | 4,59 | 14/15 | +11,09 | +17,37 | 270 |
| **B. Estabilidad sola** (mb + crec.) | **+19,21 pp** | **9,29** | **15/15** | +20,76 | +16,13 | — |
| C. PERFIL completo (3 cond.) | +18,96 pp | 10,22 | 15/15 | +19,22 | +18,45 | 110 |
| D. PERFIL sin excluir Fin/RE | +15,84 pp | 7,69 | 15/15 | +17,45 | +12,63 | — |

**La dilución sola no basta (+13,2) pero el filtro de dilución tampoco aporta:** B (sin él)
da +19,21 y C (con él) +18,96. El motor es la **estabilidad** — margen bruto estable y
crecimiento consistente. Añadir dilución cuesta la mitad de los nombres (270→110) a cambio
de −0,25 pp. Excluir Financials/Real Estate aporta +3,12 pp, dentro del ruido.

**Simplificación recomendada: quedarse con las dos condiciones de estabilidad.**

### Test 4 — Concentración: no compensa, y explica el listón de 0,60

400 carteras aleatorias de N nombres extraídas del perfil, 2007–2024:

| N nombres | CAGR mediano | Vol. mediana | Sharpe p50 | p95 | p99 | máx. | **% que llega a 0,60** |
|---|---|---|---|---|---|---|---|
| 6 | 12,07% | 27,2% | **0,37** | 0,56 | 0,62 | 0,73 | **2,5%** |
| 15 | 12,52% | 25,0% | 0,42 | 0,55 | 0,61 | 0,76 | 1,3% |
| 30 | 12,75% | 24,2% | 0,44 | 0,55 | 0,59 | 0,63 | 0,5% |
| 60 | 12,89% | 23,8% | **0,45** | 0,52 | 0,55 | 0,56 | 0,0% |

Concentrar **empeora** el Sharpe mediano (0,45 → 0,37): añade riesgo idiosincrático sin
retorno que lo compense. Solo ensancha la cola derecha.

Y da la respuesta a la pregunta del listón: **el 2,5% de las carteras aleatorias de 6
nombres alcanza Sharpe ≥ 0,60 por puro azar.** Un 0,60 sobre ~6 posiciones es una tirada de
1 entre 40, no una evidencia de habilidad — y menos cuando el alfa asociado (+9,72%) no
replica (+0,75%) con el mismo pipeline.

### Test 5 — Persistencia y rotación

| Definición | Sigue a 1 año | 2 años | 3 años | 5 años | Rotación anual |
|---|---|---|---|---|---|
| PERFIL 3 condiciones | 58,8% | 48,9% | 43,0% | 37,4% | ~41% |
| Estabilidad 2 condiciones | **67,8%** | 55,7% | 49,0% | 42,6% | **~32%** |

Con 41% de rotación y 0,30%/lado, el coste real es **0,25%/año**, no el 0,60% que cobré en
el backtest: los CAGR reportados están **subestimados en ~0,35 pp**. La variante de dos
condiciones rota menos, así que es mejor también por este lado.

### Test 6 — Cruce con el detector de inflexión: no aporta, y son incompatibles

| Grupo | acc_seq ≥ +0,05 | n | Mediana rel20 | % desastre |
|---|---|---|---|---|
| PERFIL | sí acelera | 46 | +4,4% | 8,7% |
| PERFIL | no acelera | 1.656 | +3,1% | 15,0% |
| resto | sí acelera | 778 | −15,3% | 22,6% |
| resto | no acelera | 5.000 | −17,6% | 21,3% |

A 5 años el detector **no aporta nada** (+1,3 pp en el perfil, +2,3 pp en el resto: ruido).
Es coherente: es una señal de inflexión a un año, y a cinco se diluye.

Más importante: **son casi mutuamente excluyentes.** Solo el 2,7% del perfil acelera, frente
al 13,5% del resto — porque "crecimiento consistente" (baja desviación) excluye por
construcción a las empresas que aceleran. **No se pueden tener las dos cosas:** el detector
busca inflexión y el perfil busca lo contrario. Son dos estrategias, no una combinable.

### Test 7 — Supervivencia contra datos externos: sesgo confirmado y cuantificado

Muestra de 28 empresas reales que desaparecieron entre 2012 y 2020:

| Tipo de salida | Total | En el panel | **Ausentes** |
|---|---|---|---|
| Quiebra | 12 | 4 | **8 (67%)** |
| Adquisición | 15 | 6 | 9 (60%) |
| **Total** | **28** | **10** | **18 (64%)** |

**El 64% de las empresas que desaparecieron no está en el panel.** Las adquiridas que sí
están (BRCM, LLTC, ATML, MSCC, ILG, WFM) tienen la serie terminada correctamente en el año
de la operación, así que las salidas por compra —que suelen ser positivas, con prima— no
faltan sistemáticamente. Las que faltan son sobre todo **quiebras**, es decir, los peores
resultados. Confirma la dirección del sesgo: **infla los niveles absolutos y juega en
contra de la conclusión**, no a favor.

**Defecto 9 (nuevo):** las cuatro quiebras "presentes" lo están por **retroajuste de
contrasplit**, no por tener historia real. SUNE llega a un `precio_post` de **10.278.000** y
WLL de **17.494**. El ratio entre fechas se conserva, así que no falsea retornos, pero
**inutiliza el filtro `precio_post >= 1`**: un penny stock que luego hace un contrasplit
1:1000 aparece históricamente como una acción de miles de dólares y **entra** en universos
que pretendían excluirlo.

Comprobado que no contamina este estudio: dentro del universo final el precio máximo es
618 $ (perfil) y el retorno máximo a 1 año +508%, con un solo evento por encima de +500%.
Los filtros de capitalización lo bloquean. Pero cualquier estudio futuro que use
`precio_post >= 1` como filtro de calidad sobre el panel completo **está dejando entrar
justo lo que quería excluir**.

---

## 13. Nombres actuales, cara a cara con el perfil barato, y qué se puede esperar

### Cuántas empresas hoy

Sección transversal más reciente del panel (informes entre 2026-03 y 2026-08):

| | Empresas |
|---|---|
| Universo (300 M$–5.000 M$, sector asignado, tickers limpios) | **682** |
| **PERFIL estabilidad** (2 condiciones, sin Fin/RE) | **212** |
| Perfil de 3 condiciones (añadiendo dilución < 2%) | 172 |

212 nombres es una lista de trabajo, no una cartera. El test 4 dice que concentrarla al azar
**empeora** el Sharpe, así que reducirla exige un criterio con señal — y la sección siguiente
muestra que no lo hemos encontrado.

### Cara a cara con el perfil del estudio anterior

Distribución completa del retorno a 5 años relativo al SPY, misma construcción para los tres:

| | n | **Acierto 5a** | Acierto 1a | p10 | p25 | **p50** | p75 | **p90** | p95 | %>+100pp | %desastre |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **PERFIL estabilidad** | 2.162 | **30,6%** | 41,5% | −61,1 | −34,3 | **+2,5** | **+49,5** | **+112,9** | +168,0 | **7,1%** | **9,5%** |
| BARATO cíclico (estudio previo) | 1.338 | 27,5% | 41,4% | −60,5 | −37,7 | −9,7 | +33,5 | +91,8 | +158,1 | 5,8% | 10,2% |
| Universo entero | 7.492 | 24,4% | 37,3% | −66,6 | −43,7 | −13,2 | +31,8 | +97,9 | +157,9 | 5,7% | 11,7% |

**Sí, el perfil supera al del estudio anterior** — pero conviene ver *dónde*. La ventaja por
percentil frente al barato cíclico:

| Percentil | p10 | p25 | p50 | p75 | p90 | p95 |
|---|---|---|---|---|---|---|
| Ventaja del PERFIL | **−0,6** | +3,4 | **+12,2** | **+16,0** | **+21,1** | +9,9 |

**El perfil no mejora la cola izquierda.** En el p10 ambos pierden ~60%: da igual el perfil,
uno de cada diez es un desastre. Toda la ventaja está en el **cuerpo alto de la distribución
(p50–p90)**. Traducción operativa: el perfil sirve para **evitar la mediocridad, no para
evitar la ruina**. De la ruina solo protege la diversificación — lo que refuerza la
conclusión del test 4 contra concentrar.

### Qué porcentaje de acierto esperar

Hay que distinguir dos cosas que se confunden todo el rato:

| Medida | Valor |
|---|---|
| Posiciones individuales que baten al SPY a 5 años | **30,6%** |
| Posiciones individuales que baten al SPY a 1 año | 41,5% |
| Posiciones que hacen **más de +100 pp** sobre el SPY | 7,1% |
| Posiciones que son desastre (< −50%) | 9,5% |
| **Años en que la cartera bate al SPY** | **66,7%** |

Que solo el 30,6% de las posiciones bata al índice **no es un fallo del perfil**: es la
asimetría normal de las acciones. La mediana de una acción pierde contra el índice; el índice
lo sostienen unas pocas. Por eso el perfil gana **como cartera** (66,7% de los años) mientras
pierde en la mayoría de sus posiciones. Es un negocio de cola, como avisaba la regla 3.

### ¿Se puede concentrar con filtros de calidad? NO se ha validado

Ocho candidatos probados dentro del perfil, todos contra la banda de ruido de 5,77 pp:

| Filtro adicional | Diferencia | ¿Supera el ruido? |
|---|---|---|
| Sector Tech o Health | +15,4 pp | sí |
| Crecimiento alto | +7,7 pp | justo |
| Reinversión alta | +5,9 pp | en el límite |
| Margen operativo alto | +3,3 pp | no |
| Margen bruto alto | +2,4 pp | no |
| P/GP caro (mitad alta) | +1,9 pp | no |
| Racha positiva | −0,6 pp | no |
| Sorpresa positiva | −5,1 pp | no |

El único candidato claro daba unos números espectaculares:

| Cartera | n/año | CAGR | Vol. | Sharpe | Beta | Alfa | Peor año | % años > SPY |
|---|---|---|---|---|---|---|---|---|
| PERFIL estabilidad | 155 | 14,37% | 24,3% | 0,51 | 1,21 | +4,23% | −36,8% | 66,7% |
| PERFIL + Tech/Health | 48 | 18,26% | 27,5% | 0,59 | 1,29 | +7,83% | −33,2% | 77,8% |
| PERFIL + Tech/Health + crecimiento | 28 | **22,47%** | 28,7% | **0,71** | 1,32 | **+12,01%** | −32,4% | 88,9% |
| SPY | — | 9,11% | 18,6% | 0,38 | 1,00 | — | −40,9% | — |

**Y son falsos.** El filtro sectorial se eligió mirando toda la muestra. Repitiendo la
selección solo con cohortes 2007–2011 y comprobando qué pasó después:

| Ventana | Materiales | Healthcare | Cons. Cíclico | Technology | Industrials |
|---|---|---|---|---|---|
| Selección 2007–2011 | **+35,2%** | +32,2% | +25,0% | +22,9% | +14,9% |
| Posterior 2012–2021 | **−5,1%** | +24,3% | **−17,5%** | +3,6% | +2,3% |

Un analista situado en 2011 con estos datos habría elegido **Basic Materials** — el mejor de
su ventana — y habría cosechado −5,1%. Consumer Cyclical pasa de +25,0 a −17,5. El orden
sectorial **no es estable**, así que el alfa de +12% es selección con retrovisor, exactamente
el error contra el que avisa la regla 5. **Descartado.**

Solo Healthcare aguanta las dos ventanas (+32,2 → +24,3), pero es justo el sector donde el
sesgo de supervivencia del panel muerde más fuerte: las biotecnológicas pequeñas que fracasan
son las grandes ausentes del test 7. No es utilizable como filtro sin datos de delistings.

### Respuesta a "¿superaríamos al S&P 500?"

Con el perfil base, sin concentrar y sin filtros post-hoc:

**CAGR 14,37% frente a 9,11% del SPY · Sharpe 0,51 vs 0,38 · alfa +4,23% · peor año −36,8%
frente a −40,9% · bate al índice el 66,7% de los años.** Ventaja de 5,3 pp anuales con beta
1,21 y 24,3% de volatilidad.

Estos números son mejores que los de la sección 11 (CAGR 12,91%, Sharpe 0,46) por las dos
correcciones de los tests 3 y 5: se usa la variante de **dos** condiciones (quitar el filtro
de dilución no resta y duplica los nombres) y los costes bajan de 0,60% a **0,25%/año**, que
es la rotación real medida.

Tres avisos que no conviene olvidar al leer ese 14,37%:
1. Los niveles absolutos están inflados por el sesgo de supervivencia del panel (test 7:
   falta el 64% de las desaparecidas, sobre todo quiebras). La **ventaja relativa** aguanta
   mejor que el nivel.
2. Un alfa de +4,23% sobre 18 años anuales tiene un error estándar grande; es la magnitud
   creíble, no una cifra de precisión.
3. Con 212 candidatos y sin criterio validado para reducirlos, la implementación honesta es
   **diversificar mucho**, no elegir los diez mejores.

---

## 14. Contra el NASDAQ: bate al S&P 500, no al QQQ

El panel trae `fwd_4t_rel_qqq`, así que el NASDAQ 100 se despeja igual que el SPY
(`qqq = fwd_4t − fwd_4t_rel_qqq`). Misma cartera anual, mismos costes (0,25%/año):

| Cartera | CAGR | Volatilidad | Sharpe | Peor año | % años que baten |
|---|---|---|---|---|---|
| **PERFIL estabilidad** | 14,37% | 24,3% | 0,51 | −36,8% | — |
| **QQQ (NASDAQ 100)** | **14,51%** | **21,9%** | **0,57** | **−30,9%** | — |
| SPY | 9,11% | 18,6% | 0,38 | −40,9% | — |
| PERFIL vs SPY | | | | | **66,7%** |
| PERFIL vs QQQ | | | | | **44,4%** |

**El QQQ gana en las cuatro dimensiones:** más CAGR, menos volatilidad, mejor Sharpe y mejor
peor año. El alfa del perfil contra el QQQ es **+0,30%**, es decir, cero. Un dólar en 2007
son **11,22 $** con el perfil y **11,47 $** con el QQQ (4,81 $ con el SPY).

### ¿Estamos replicando el NASDAQ? No, pero da igual

| Correlación | valor |
|---|---|
| PERFIL – SPY | 0,92 |
| PERFIL – QQQ | 0,90 |
| QQQ – SPY | 0,95 |

El perfil se parece **más** al S&P que al NASDAQ. Y por composición es mucho más diversificado
que el QQQ: 11 sectores frente a la concentración del índice en tecnología y comunicación,
small caps de 300 M$–5.000 M$ en lugar de mega caps, y excluye Financials y Real Estate.
Es una cartera genuinamente distinta que **acaba en el mismo sitio con más riesgo**.

Mezclar tampoco resuelve nada: 25% perfil / 75% QQQ da Sharpe 0,57 — idéntico al QQQ solo.
Con correlación 0,90 no hay diversificación real que extraer.

### Lo único que sí aporta: gana en años distintos

| Mejores años del perfil vs QQQ | | Peores | |
|---|---|---|---|
| 2022 | **+21,7 pp** | 2019 | −17,0 pp |
| 2016 | +16,8 pp | 2023 | −15,2 pp |
| 2012 | +10,4 pp | 2015 | −11,0 pp |
| 2009 | +10,1 pp | 2007 | −6,7 pp |

El perfil gana cuando la mega-cap tecnológica sufre —**2022, el shock de tipos: +4,4% frente
al −17,5% del QQQ**— y pierde en los años en que el índice lo hace todo (2019, 2023). Es una
cobertura contra un régimen concreto, no una estrategia superior.

### Asimetría que agrava la comparación

Los 14,37% del perfil están **inflados por el sesgo de supervivencia** del panel (test 7:
falta el 64% de las empresas desaparecidas, sobre todo quiebras). Los 14,51% del QQQ son
retorno **real e invertible**. La comparación honesta es, por tanto, **peor** para el perfil
de lo que muestra la tabla.

**Conclusión:** el perfil es una estrategia legítima que bate al S&P 500 con holgura
(+5,3 pp anuales, mejor Sharpe, mejor peor año), pero **no bate al NASDAQ 100**, y quien
quisiera ese retorno podía comprar QQQ sin hacer nada de esto. Su valor diferencial está en
el comportamiento en 2022, no en el retorno agregado.

## 15. Delistings: no se pueden obtener con el plan actual de FMP

Intentado y **bloqueado**:

- `company/delisted-companies` con `page` ≥ 1 → `ACCESS DENIED ... requires a higher plan`
  (cuenta en plan **Starter**).
- Los filtros `from_date`/`to_date` se **ignoran silenciosamente**: pedir 2015 devuelve los
  mismos registros de agosto de 2026.
- Resultado: solo son accesibles los ~100 delistings más recientes, todos de las últimas dos
  semanas, y dominados por ETFs, OTC y bolsas extranjeras.

No sirve para medir la supervivencia de 2007–2021, que es lo que hace falta. Alternativas,
de menor a mayor coste:

1. **Arreglarlo aguas arriba.** El sesgo no lo introduce este estudio, sino el pipeline que
   construyó `hypergrowth_panel` a partir de un universo de tickers vivos. Si la fuente
   original conserva las empresas muertas, es ahí donde hay que capturarlas.
2. **Sharadar Core US Equities (Nasdaq Data Link)** — marca delistings y es de precio
   asequible; es la opción práctica habitual para backtests.
3. **Norgate Data** — pensado explícitamente para backtesting con valores delistados.
4. **FMP Premium** — desbloquea la paginación del endpoint ya integrado, que es el camino de
   menor fricción dado que el MCP ya está conectado.
5. **CRSP** — el estándar académico, y el más caro.

---

## 16. ¿Tenemos "lo mejor de los dos índices"? Un test lo responde

La hipótesis: si tenemos diversificación tipo S&P con retornos tipo NASDAQ, estamos
capturando la fuerza de ambos. Es una idea con fundamento y merece un contraste directo,
no una opinión.

**El motor del NASDAQ es fabricar gigantes:** su retorno viene de un puñado de empresas que
pasaron de pequeñas a enormes. Si el perfil capturase esa fuerza, debería seleccionar
—cuando aún eran pequeñas— a las que después se hicieron gigantes. Test: de las empresas que
estuvieron en el tramo 300 M$–5.000 M$ entre 2007 y 2016, ¿qué porcentaje pasó el perfil,
según en qué se convirtieron?

| Destino hoy | Tickers | % que pasó el perfil | % de años dentro |
|---|---|---|---|
| Mega (> 50.000 M$) | 68 | **41,2%** | 30,4% |
| Grande (20–50.000 M$) | 110 | 43,6% | 28,7% |
| Media (5–20.000 M$) | 337 | 44,2% | 24,8% |
| Siguió pequeña (< 5.000 M$) | 408 | **41,9%** | 22,4% |

**Completamente plano.** El perfil no distingue en absoluto quién se convertirá en gigante:
selecciona al 41–44% en los cuatro grupos por igual. **No tenemos el motor del NASDAQ.**

Esto encaja con la sección 13: la ventaja del perfil está en los percentiles p50–p90 y es
nula en las colas. Fabricar gigantes es un fenómeno de cola derecha extrema, exactamente
donde el perfil no aporta nada.

**Veredicto matizado.** La parte correcta de la hipótesis es que dos carteras con el mismo
CAGR realizado **no son equivalentes** si una llegó por una apuesta concentrada que salió
bien y la otra por una base diversificada: *ex ante*, la segunda es más robusta si uno no
cree que el régimen de la mega-cap tecnológica se repita. Y el +21,7 pp de 2022 demuestra
que el motor es genuinamente distinto, no una réplica.

La parte incorrecta es "capturamos la fuerza de ambos". No la capturamos: **igualamos al QQQ
en la mejor época del QQQ, con más volatilidad y peor drawdown, por una vía distinta** — y
sin su capacidad de generar gigantes. Es un motor diferente que produjo un número parecido
en esta ventana, no una síntesis superior. Súmese que el 14,37% del perfil está inflado por
supervivencia y el 14,51% del QQQ no.

## 17. Qué hizo caer a los que cayeron (versión ejecutable de la idea)

No hacen falta las listas de índices: el propio panel permite definir a los caídos. Empresas
que llegaron a valer **más de 10.000 M$** y hoy valen **menos del 40%** de su pico, frente a
las que conservan el 90% o más. Se miden sus características en los **3 años anteriores al
pico**, es decir, antes de la caída:

| | **CAYÓ** (69 empresas) | **SE MANTUVO** (502) |
|---|---|---|
| **% de trimestres diluyendo ≥ 2%** | **48,7%** | **23,0%** |
| Dilución mediana | 1,84% | **0,00%** |
| Crecimiento mediano | 24,2% | 10,7% |
| Desviación del crecimiento | 0,212 | **0,125** |
| Desviación del margen bruto | 0,0304 | **0,0254** |
| Reinversión | 0,190 | **0,129** |
| Margen bruto | 48,4% | 45,4% |
| Margen operativo | 14,4% | 15,8% |
| P/GP | 9,30 | 8,61 |

**Las tres señales del perfil apuntan todas en la dirección correcta, en una población
completamente distinta**: grandes cayendo en vez de pequeñas subiendo. Diluían el doble de
trimestres, crecían más rápido y de forma más errática, con margen menos estable y más
reinversión. Es el mismo mecanismo del test 1 —comprar crecimiento con acciones— visto desde
el otro extremo del ciclo de vida.

Y el margen bruto y el múltiplo **no separan nada** (48,4 vs 45,4; 9,30 vs 8,61): ni la
calidad aparente del negocio ni lo que pagabas por él avisaron de la caída. Lo que avisó fue
cómo se financiaba el crecimiento.

*Nota de rigor:* este contraste es descriptivo y no estaba pre-registrado; sirve como
validación del mecanismo, no como evidencia independiente de la magnitud. La media de
dilución (16,34% vs 45,17%) está contaminada por outliers y no debe usarse: valen la mediana
y el porcentaje de trimestres.

## 18. El agujero que esto destapa: la deuda

El perfil premia **no diluir**. Pero una empresa puede evitar la dilución **endeudándose en
lugar de emitir acciones** — y el perfil, tal y como está, puntuaría como "calidad" a un
roll-up financiado con deuda. Es un fallo estructural, no un detalle.

El caso de manual está en el propio panel: **TEVA** — deuda neta 13.826 M$, fondos propios
7.910 M$, fondo de comercio 15.999 M$ y beneficios retenidos **−13.762 M$**. Crecimiento
comprado con deuda y adquisiciones, sin dilución que lo delate.

**Comprobado: los balances de FMP sí funcionan con el plan Starter** (a diferencia de
`delisted-companies` y `indexes`, ambos bloqueados). El endpoint
`statements/balance-sheet-statement` devuelve `totalDebt`, `netDebt`, `goodwill` y
`totalStockholdersEquity`. La extensión natural del estudio es:

1. Añadir **deuda neta / EBITDA** y **fondo de comercio / activos** al perfil.
2. Contrastar la hipótesis gemela: *si no diluir predice, apalancarse debería predecir a la
   inversa*. Si se confirma, el perfil pasa de "no emite acciones" a "no financia el
   crecimiento con capital ajeno de nadie", que es una idea económicamente más completa.
3. Coste realista: no hace falta el panel entero. Con los **69 caídos + una muestra de los
   que se mantuvieron**, y con los **212 nombres actuales**, la pregunta queda resuelta con
   unos cientos de llamadas.

### Causas de caída conocidas, y cuáles son testables aquí

| Causa | ¿Se puede medir con el panel? |
|---|---|
| Crecimiento comprado con acciones | **Sí** — `dilucion_yoy`, ya validado |
| Crecimiento comprado con deuda | **Sí, añadiendo balances de FMP** ← la extensión |
| Roll-up de adquisiciones | **Sí** — fondo de comercio / activos (FMP) |
| Erosión secular del negocio | Parcial — caída sostenida del margen bruto |
| Ciclo de materias primas | Parcial — vía sector |
| Concentración en un producto / caída de patente | **No** — no hay datos de producto |
| Fraude contable o reformulación | **No** |
| Dependencia de un cliente o plataforma | **No** |

Las tres primeras cubren la mayoría de las caídas documentadas y **dos ya están al alcance**.
Las otras exigen datos que no están en el panel ni en el plan actual de FMP.

## 19. Interactive Brokers: no sirve para el backtest, sí para otra cosa

El MCP de IBKR **no tiene motor de backtesting**. Lo que ofrece es `get_price_history`
(limitado a periodos de hasta cinco años por contrato), `get_price_snapshot`,
`search_contracts`, watchlists y datos de cuenta. Reconstruir 18 años y miles de tickers
exigiría una llamada por contrato: no es la herramienta.

Para lo que **sí** sirve, y es relevante:

1. **Comprobar que los 212 nombres son operables.** El campo `avg_90d_usd_volume` de
   `get_price_snapshot` da el volumen medio en dólares a 90 días. El backtest asume
   entrada y salida al precio del cierre con 0,30%/lado, y en small caps de 300 M$ eso es
   una suposición, no un hecho. **Es el hueco de implementación más grande que queda.**
2. **Validar los precios del panel** contra una fuente independiente — útil sabiendo lo del
   retroajuste de contrasplits (defecto 9).
3. **Materializar la lista** como watchlist con `create_watchlist`.

Lo que IBKR **no** resuelve es el problema de los delistings: una vez muerto el contrato,
no devuelve histórico.
