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

4. **El control negativo (H5) FALLA**, y es el hallazgo más útil del estudio: la inicial
   del ticker (A–M vs N–Z), que no debería aportar nada, produce −5,3 pp con
   **p = 0,035**. Con 15 cohortes anuales correlacionadas se fabrican efectos de ~5 pp
   con significación nominal. **Todo efecto por debajo de ~10 pp en este panel es ruido**,
   lo que invalida la H3 pre-registrada y confirma la principal (19,9 pp, t=5,55, 15/15).

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
solapadas y correlacionadas entre sí no son 15 observaciones independientes. **La lectura
operativa:** en este panel, **nada por debajo de ~10 pp debe creerse**. Eso descarta la H3
pre-registrada (+4,13) y Q1/Q2 como componentes, y deja en pie el efecto principal
(+19,86 pp, 4× la banda de ruido) y E1/Q3/Q4/Q5.

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
