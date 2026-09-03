# Hallazgos que sobreviven

## ESTADO ACTUAL — dónde estamos, en dos cifras

**Alfa: cero en la estrategia original — pero C21 encontró uno que sí sobrevive.**

| medida | valor | t | qué es |
|---|---|---|---|
| C4 vs Nasdaq (2007–2023) | +0,27 pp de CAGR | 0,05 | la estrategia original: nada |
| Pasar el filtro vs no pasarlo | +2,98 pp | 1,86 | el filtro elige bien dentro del universo |
| Barato en Industrials+Materials (C21) | +6,76 pp vs su pool | +2,38 | pasa los cinco controles, **pero beta 1,46 y alfa Jensen solo +0,87%** |
| **Barato en INDUSTRIALS, alfa INTERNO (C23)** | **+6,73 pp** | **+2,31** | **lo único con \|t\|>2: elige bien dentro del sector** |
| Barato en Industrials vs Nasdaq (C24) | alfa Jensen +2,86% | **+0,48** | **no establecido; Sharpe 0,423 vs 0,512 — pierde ajustado por riesgo** |
| Overlay de tendencia | −1,31 pp | −1,10 | cuesta |

**C21 es lo único de la serie con |t| > 2**, replicado en ambas mitades, monótono entre
cuartiles y estable al quitar cualquier año. **Pero no descorrelaciona** (0,785).

**Correlación: 0,918, sin ninguna forma establecida de bajarla.**

| vía | correlación | descorrelación real | estado |
|---|---|---|---|
| C4 tal cual | 0,918 | — | punto de partida |
| 7 variantes cíclicas | ~0,90 | ±0,03 | nada (C5) |
| Cíclicas con filtros invertidos | 0,29–0,78 | −0,34 a +0,30 | fallan las 4 en confirmación (C13) |
| Defensivos + momento | 0,62 | −0,14 | sin respaldo: 29% de ventanas lo dan por azar (B8) |
| Overlay de tendencia | 0,78 | −0,081 (p=0,15) | no significativo (C10) |

La distinción que lo ordena todo: **la correlación bruta sí baja, la descorrelación real no.**
Estar fuera del mercado el 22% de los años baja la correlación sola, se elijan los años que
se elijan — el efectivo no correlaciona con nada. Bajar la correlación es gratis y trivial:
basta con tener menos dinero invertido. **Lo que no hay evidencia de que nadie pueda hacer es
bajarla eligiendo el momento.**

**Consecuencia práctica:** con lo que sabemos hoy, este compartimento no se justifica frente
a comprar más Nasdaq. No aporta rentabilidad ni diversificación, y cuesta trabajo, comisiones
e impuestos que el ETF no cuesta. Eso no prueba que la estrategia sea mala: prueba que **con
17 años de un panel roto no se puede demostrar que sea buena**, y el listón para meter dinero
propio es demostrarlo.

**Lo siguiente, y es barato:** pasar el test de ventanas (B8) a todo lo medido sobre 17 años,
empezando por C7. Se hace hoy, solo con el índice. Lo que sobreviva a eso será lo primero de
la serie con derecho a llevar dinero encima.

---

Resumen de lo que hemos establecido en esta serie de estudios, separando lo que aguanta un
control de lo que no. Ordenado por importancia práctica.

---

## A. Sobre los datos (lo más importante, y lo que menos esperábamos)

**A1. El panel no registra muertes antes de 2015.** De 0 a 5 bajas al año hasta 2014,
cuando la tasa real son 200–400. Empieza a registrarlas en 2015–2016 (18 y 58) y solo llega
a ser realista hacia 2021–2023 (1,6% → 3,8%). Además, **0 altas nuevas en 2024 y 2025**.

| tramo | estado como universo |
|---|---|
| antes de 2002 | inservible (~700 tickers) |
| 2002–2014 | **ficción**: cero muertes |
| 2015–2020 | contaminado, mejorando |
| 2021–2023 | aceptable con reservas |

**A2. La supervivencia es imposible.** El porcentaje de tickers de un año que siguen vivos
en 2025 se queda **plano en 82–85% desde 2002 hasta 2020**. Una cohorte de 2002 y una de
2020 no pueden coincidir. Y el número de tickers crece de 366 (1998) a 6.604 (2022) cuando
el mercado real encogió (8.025 cotizadas en 1996 → 4.102 en 2012, Doidge/Karolyi/Stulz).
Firma inequívoca de un panel construido desde una lista actual con historia hacia atrás.

**A3. `sector` no es nulo: es el centinela `'desconocido'`**, que cubre 5.105 de 6.967
tickers (73%). **Ver A7: ese centinela es el marcador de muerte.**

**A4. Ese centinela predice el retorno.** Dentro del **mismo año y el mismo sector**, las
empresas sin clasificar rinden **−8,98 pp (p = 0,064)**, o −12,63 pp ponderado
(**p = 0,008**). Test de permutación estratificado, 81 celdas, 520 eventos.
**El predictor más fuerte de toda la serie no es un factor: es si a la empresa le
rellenaron un campo de metadatos.** Es la firma del sesgo de supervivencia.

**A5. Trece eventos son la misma empresa bajo dos o tres tickers.** LNW/LNWO/SGMS (en 2018
Light & Wonder entra tres veces, 15% de la cartera de ese año), IRBT/IRBTQ, REV/REVRQ,
UPBD/RCII, CSWI/CSW, BRKS/AZTA, CSU/SNDA, AXL/DCH. Deduplicar vale **+0,71 pp** de CAGR.

**A6. Los precios del panel están planos antes de 2007.** El 91,7% de los tickers tienen
`mom12` **exactamente 0** en 2004 (88,7% en 2005, 83,6% en 2006): el precio de hace cuatro
trimestres es idéntico al actual. Antes de 2007 el panel no tiene precios, tiene un
forward-fill. **Es un defecto distinto y anterior al de A1**, que hablaba solo de muertes.
El arranque en 2007 de `c4_base.sql` no era conservadurismo, era el primer año utilizable.
Queda un **~8% residual entre 2007 y 2020** que sí afecta a producción: `mom12` es la
variable de selección, así que ese 8% del universo está **excluido en silencio del top 20%**
por un defecto de datos. Sin medir si rinde distinto. Ver `NOTA-PRECIOS-PLANOS-PRE-2007.md`.

**A7. Las muertes están en el panel: son el cubo `'desconocido'`.** El 33,7% de los tickers
sin sector (1.619 de 4.808) desaparecen del panel, frente al **0,4%** de los cíclicos (3 de
704) y el 0,3% del resto de sectores. **Ochenta veces más mortalidad en el cubo sin sector.**
`'desconocido'` no es "falta el dato": es el marcador de muerte, porque el panel se construyó
desde una lista de vivos y las bajas quedaron sin clasificar. **Esto explica A4 entero**: el
centinela predecía −9 a −12,6 pp porque *es* la tasa de mortalidad colándose por la puerta de
atrás. Y significa que **todo el análisis sectorial de la serie (C2, C12, C13, C14, colas,
piloto) ha corrido sobre un universo con 0,4% de mortalidad**. Pero las bajas son
recuperables: en 2021–2023 hay **126 balas reales** (retorno del último año < −25%) y 182
compras con prima — SIVB, SBNY, FRC, RAD, ENDP, MNK, YELL, WPG, AMRS, CANO y una docena con
sufijo Q. Ver `NOTA-DONDE-ESTAN-LAS-MUERTES.md`.

**A8. `AGENDA-ESTUDIOS.md` daba por bloqueadas dos cosas que no lo están.** En plan Premium
funcionan **los trimestrales de `statements`** (80 trimestres hasta 2006) y
**`company/delisted-companies`** con paginación. Ambas se daban por imposibles y ambas son la
llave de los dos estudios que quedaban. **Reverificar el plan antes de dar nada por
bloqueado.**

---

## B. Sobre el método (reglas que hemos pagado por aprender)

**B1. Partir en descubrimiento (años pares) y confirmación (impares) mata casi todo.**
Han caído así: el efecto de la deuda, ROIC, FCF yield, y el alfa de "defensivos + momento"
(+7,9 → +2,3). **Seis efectos aparentes deshechos bajo control.** Cerrar la regla por
escrito ANTES de mirar la confirmación es lo que ha hecho que no costaran nada.

**B2. La correlación baja sola al reducir nombres.** Carteras **aleatorias** del universo
filtrado (300 simulaciones por tamaño):

| nombres | correlación con el Nasdaq **al azar** |
|---|---|
| 3 | 0,654 |
| 5 | 0,735 |
| 12 | 0,825 |
| 40 | 0,883 |

Cualquier variante estrecha "parece" descorrelacionada. La métrica válida es la
**descorrelación real** = observada − la del azar con ese mismo tamaño y pool.

**B3. Beta ≠ correlación.** Beta = correlación × volatilidad relativa. "ConsDef+Utilities"
tenía beta 0,45 y correlación 0,79: su beta baja era volatilidad baja, no diversificación.

**B4. Hay dos alfas y solo uno está contaminado.**

| medida | media | t | años positivos |
|---|---|---|---|
| contra el Nasdaq | +0,83 pp | +0,36 | 9/17 |
| **pasar el filtro vs no pasarlo** | **+2,98 pp** | **+1,86** | **12/17** |

La comparación interna es inmune al sesgo de supervivencia porque **falta lo mismo en los
dos brazos**. La comparación contra un índice real, no. **La tesis hay que construirla
sobre la medida interna.**

**B5. A frecuencia anual, cualquier cesta de acciones USA correlaciona 0,8–0,95 con
cualquier índice USA.** El S&P y el Nasdaq dan 0,94 entre sí. La correlación anual mide
"¿es bolsa de EE.UU.?", no "¿es distinto?".

**B6. La correlación es medible con n=17; la rentabilidad no.** Un oráculo que esquivara
**solo 2008** con información perfecta subiría el CAGR de 14,16% a 18,07% (**+3,91 pp**) y
bajaría la correlación solo de 0,918 a 0,861 (**−0,058**). Acertar **una** observación mueve
la rentabilidad 3,9 pp y la correlación 0,06. La rentabilidad de 17 años es un juego de una o
dos observaciones; la correlación es un estadístico de las diecisiete. **Cualquier resultado
de rentabilidad de esta serie está a un año de distancia de cambiar de signo** — incluidos
los que salieron a favor.

**B7. En el eje temporal, el null no es "siempre invertido": es permutar la exposición.**
El 70% de los overlays **aleatorios** que salen del mercado 5 de 17 años bajan la correlación
por debajo de 0,80, y el 8,3% cumplen a la vez correlación < 0,80 y CAGR > Nasdaq. Probar 15
variantes y quedarse con la mejor da éxito aparente con probabilidad **~73% sin señal
alguna**. Permutar el vector de exposición fija *cuántas* veces se sale y aísla la única
pregunta que importa: si acierta *cuándo*.

**B8. Una ventana de 17 años fabrica descorrelación por sí sola, igual que un tamaño de
cartera pequeño.** Misma regla, 38 ventanas solapadas de 17 años: la descorrelación real va
de **−0,403 a +0,096**, con mediana −0,065, y solo el 26% de las ventanas alcanza p < 0,05 —
cuando sobre los 54 años la regla **no descorrelaciona** (−0,081, p = 0,154). Y el ΔCAGR va
de **−5,80 a +4,50 pp** entre ventanas, un rango de 10 pp que confirma empíricamente el
±11,5 pp que la aritmética predecía (B6). **B2 decía que hay que comparar contra carteras
aleatorias del mismo tamaño; B8 añade que hay que comparar contra ventanas alternativas del
mismo largo.** Sin eso, cualquier número medido sobre 17 años —incluido el −0,14 de C7, que
el 29% de las ventanas supera— está sin respaldo, aunque no esté refutado.

**B9. La diferencia de medias miente en distribuciones con cola; el AUC no.** El momento medio
del decil superior cíclico es **30,59%** frente al **17,29%** del resto — parece una señal
enorme. Su **AUC es 0,482**: ninguna capacidad de distinguir. La diferencia de medias la
producen los mismos valores extremos que se intentan predecir. Con asimetría 3,46, **toda
comparación de medias entre grupos hay que acompañarla del AUC**, y manda el AUC.

---

## C. Sobre la estrategia

**C1. C4 no es "las cíclicas".** C4 = universo USA 300M–5.000M$, **sin filtro de sector**,
filtros de estabilidad + regla 40 + capitalización, top 20% por momento. "Las cíclicas" es
un **subconjunto** de 194 eventos usado en los estudios de deuda y ROIC/FCF. Las
conclusiones de esos estudios aplican a la rebanada, no al todo.

**C2. Los filtros seleccionan a los miembros MENOS cíclicos de los sectores cíclicos.**
Los que pasan tienen 1,41 pp de desviación del margen bruto; los que fallan, 4,76 pp.
**3,4 veces menos.** Etiqueta cíclica, economía de compounder: Ross, Tractor Supply, Ulta,
Pool, Middleby, TransDigm, Watsco.

**C3. C4 no diversifica del Nasdaq.** Correlación 0,918, R² 84%. Añadirlo a una posición de
Nasdaq no reduce el riesgo (desviación 22,6 vs 22,1) y **empeora el peor año** (−36,3 vs
−30,1).

**C4. Pero sus dos mitades correlacionan solo 0,68 entre sí.** La mitad cíclica: −49,9% en
2008 y **+15,6% en 2022 con el Nasdaq a −19,9%**. Ahí sí hay comportamiento cíclico.

**C5. Ninguna variante cíclica descorrelaciona.** Las siete probadas están en ±0,03 de lo
aleatorio. Quitar la estabilidad, invertir el momento, añadir value: nada mueve la
correlación, solo sube la beta.

**C6. Lo que más rinde, rinde por beta.** "Cíclicos + value" da +1,26 pp en mezcla, pero su
descorrelación real es +0,02 y su beta 1,14. **El Nasdaq escalado ×1,07 da 14,66% frente a
15,08% de la mezcla**: casi todo se replica comprando más Nasdaq, con menos trabajo,
comisiones e impuestos.

**C7. El único candidato honesto: defensivos + momento** (12 nombres, descorrelación real
−0,14, el único con tamaño operable). Rinde 11,50% (2,3 pp menos que el Nasdaq) pero en
2008 hace −18,3 frente a −30,1, y en 2022 +8,5 frente a −14,8. **El momento es lo que
descorrelaciona**: sin él, la correlación sube de 0,62 a 0,82. Su alfa no sobrevivió al
control; su descorrelación sí.

**C8. Concentrar en 15–20 nombres no rompe la estrategia.** Viable con 10.000 €
(~500 €/posición). Las diferencias entre 10, 15 y 20 no son significativas.

**C9. Cifras de referencia de C4** (feb–feb 2007–2023, reconstrucción):
14,16% base → **15,19%** quitando duplicados y financieras/inmobiliarias, frente al 15,42%
documentado. Nasdaq 13,82%. Palancas medidas: precio de salida **−0,05 pp**, umbrales del
año anterior **+0,07 pp**, sector **+0,31 pp**, duplicados **+0,71 pp**.

**C10. El eje temporal descorrelaciona en la ventana, no en la regla.** Regla pre-registrada
sin parámetros libres (dentro si el Nasdaq subió los 12 meses previos). Sobre 2007–2023
parecía el mejor resultado de la serie: correlación 0,918 → 0,549, descorrelación real
−0,221 (p = 0,013). **Sobre 54 decisiones (1972–2025) se cae a −0,081 con p = 0,154.** La
señal larga está validada: reproduce 17/17 las decisiones del panel en 2007–2023.
En ΔCAGR: −1,31 pp anuales con t = −1,10 (−0,60 pp con efectivo al 5%, más realista para
1972–1990). **La descorrelación queda revocada; el coste en rentabilidad queda confirmado
como real y pequeño.** Ver `ESTUDIO-EJE-TEMPORAL-LARGO.md`.

**C11. La regla de tendencia solo se paga en ventanas con un bajista sostenido.** Fuera en
1974, 1975, 1982, 1984, 1988, 2001, 2002, 2003, 2008, 2009, 2016 y 2023. Las ventanas de 17
años que la favorecen son exactamente las que contienen 2000–2002 y 2008; en 1983–2002 la
descorrelación real es **positiva** (+0,10), es decir, empeoraba la diversificación. Paga
prima casi todos los años y cobra dos veces por siglo. **Con una sola cartera y horizonte de
años, no hay forma de saber si te toca la ventana que cobra.**

**C12. El universo cíclico entero rinde menos que el Nasdaq.** Las 231 cíclicas de cada año,
equiponderadas y **sin ninguno de nuestros filtros**: **11,83% frente al 14,33% del Nasdaq
(−2,50 pp), con correlación 0,862.** El techo del compartimento cíclico está por debajo del
índice, así que ningún ajuste de filtros dentro de ese pool puede dar rentabilidad y
descorrelación a la vez. **El problema nunca fueron los filtros: es el charco.** Y entre
mitades el dato se columpia +2,38 pp (pares) / −7,09 pp (impares), 9,5 pp de diferencia.

**C13. Las dos palancas que funcionan se anulan entre sí.** Medido y replicado en las dos
mitades: invertir el filtro de **estabilidad** compra descorrelación real (−0,071 y −0,339)
y paga con la rentabilidad (**3,83% con el Nasdaq al 19,68%**); invertir el de
**capitalización** compra rentabilidad sobre el azar (16,16 vs 10,88; 14,78 vs 12,41) y no
descorrelaciona nada (−0,055, ruido). **Juntarlas da lo peor de las dos: −8,41%.** La
estabilidad es lo que hace que el compartimento rinda. Refuta la hipótesis de que meter
volatilidad suba la rentabilidad, y encaja con C6: volatilidad extra es beta, y la beta es
gratis. Ver `ESTUDIO-CICLICAS-INVERTIDAS.md`.

**C14. El efecto tamaño dentro de cíclicas no es sesgo de supervivencia, pero tampoco es
usable.** Predicción declarada por adelantado: si fuera sesgo, debería encogerse en
2021–2023, el único tramo con muertes registradas (A1). **Salió al revés**: +0,25 pp en
2007–2014 (sin muertes registradas), +11,75 pp en 2015–2020, +6,88 pp en 2021–2023. Es cero
justo donde el sesgo sería máximo. Aun así falla la confirmación (p = 0,126, CAGR 14,78%
frente al 19,68% del Nasdaq) y lo dominan dos años: 2020 (+42,6 pp) y 2022 (+18,9 pp).
**Pendiente y barato: probarlo sobre el universo completo, no solo cíclicas.**

**C15. Todo el retorno del pool está en su cola, y la cola cíclica es más gorda y menos
correlacionada.** Distribución de 3.924 eventos cíclicos: p50 = 7,4%, **p90 = 69,9%,
p95 = 99,5%, p99 = 205,9%**, asimetría 3,46. La cola cíclica supera a la no cíclica en todos
los percentiles altos (+9,1 pp en p95) y **correlaciona menos con el Nasdaq cuanto más
arriba: 0,855 en la mediana, 0,825 en p95, 0,715 en p99**, y menos que la cola no cíclica
(0,814 en p99). El p90 cíclico bate al Nasdaq **17 años de 17** (+47,6 pp de media) y en 2022
lo batió por 69,8 pp con el índice en −16,1%. **Quitar el decil superior deja el pool en
1,49% de CAGR en vez de 11,83%: el 87% del retorno está en el 10% de los nombres.**

**C16. Ninguna variable del panel ve la cola.** AUC del perfil **previo** para predecir quién
acaba en el decil superior (0,5 = nada): **momento 0,482** (peor que una moneda), regla 40
**0,500** exacto, sd crecimiento 0,527, capitalización 0,439, **sd margen 0,569** — el único
con algo, y es justo el que usamos para **excluir**. El corte por deciles de momento lo
confirma: D1 10,7%, D6 8,2%, D10 12,4%, plano y sin orden. **El momento no ordena retornos en
el pool cíclico.** Ver `ESTUDIO-COLAS.md`.

**C17. Concentrar no sube la rentabilidad esperada: compra lotería.** Si la cola vale el 87%
del retorno y no es predecible, el tamaño decide. Carteras aleatorias del pool cíclico:
con **5 nombres** la mediana es 10,05% y bate al Nasdaq el **19%** de las veces; con **15**,
11,19% y **16%**; con **200**, 11,83% y **0%**. Nasdaq: 14,05%. **Concentrar sube la
dispersión, no la esperanza**, y el panel no registra las muertes (A1), así que la cola
izquierda real es peor que la medida: la lotería es peor de lo que sale.

**C18. La cola izquierda no son quiebras: son supervivientes.** En 2021–2023 las balas
(ticker que desaparece con retorno del último año < −25%) son solo el **1,2%** del universo,
promedian −54,2%, y **en el peor 1% del universo solo son el 15,6%**: el otro 84% son
empresas vivas cayendo 60–90%. En el decil inferior completo, las balas son el **7,4%**.
**Un filtro perfecto de solvencia mueve el percentil 10 de −55,4% a −54,2%** — 1,2 pp — y la
media +0,66 pp (+1,21 si las balas van de verdad a −100%). **El premio es diez veces menor
que el error de medición de ±11,5 pp (B6)**, así que no es detectable con estos datos.
Corolario que va en contra de la intuición: **el 2,6% que sale por COMPRA rinde +16,7% de
media**, así que una corrección ingenua del sesgo que cuente toda salida como muerte
empeoraría la estimación. Ver `ESTUDIO-CUANTO-VALE-ESQUIVAR-BALAS.md`.

**C19. El premio hay que medirlo dentro de la cartera candidata, no en el universo.** El 1,2%
de balas es la media del mercado entero. Una cartera que busque deliberadamente cíclicas
hundidas y apalancadas —lo que propone el bloque B del diseño— tendría una tasa mucho mayor.
**Regla: el estudio de supervivencia se ejecuta cuando exista una cartera candidata concreta,
y se mide dentro de ella.** Medirlo en el universo es promediar algo que solo importa en la
cola.

**C20. Las cíclicas son cuatro animales, y separarlos revela la señal.** Consumer Cyclical
CAGR 15,64% y correlación 0,925; Industrials 10,95% / 0,849; Basic Materials 10,00% / 0,764;
**Energy 5,71% / 0,529**. Energía y Consumo Cíclico correlacionan **0,617 entre sí**.
Promediarlas mezclaba un CAGR de 15,6% con uno de 5,7% y una correlación de 0,93 con una de
0,53. **El AUC del P/S pasa de 0,449/0,463 en el saco a 0,412/0,424 (Industrials) y
0,430/0,386 (Basic Materials)** al separar.

**C21. LO PRIMERO QUE SOBREVIVE A TODOS LOS CONTROLES: barato dentro de Industrials +
Materials.** El cuartil más barato por P/S rinde **17,79%** frente al **11,03%** de su propio
pool y al 13,71% del Nasdaq. Monótono (caras 5,54%). Pasa los cinco controles que mataron
todo lo demás: replica en pares (+7,2) e impares (+6,5); bate al azar de igual tamaño en
**+6,93 pp**; el alfa interno inmune a supervivencia (B4) es **+6,76 pp de CAGR** con
diferencia pareada **+10,15 pp y t = +2,38** —**el primer |t| > 2 de la serie**—, batiendo a
su pool **12 de 17 años**; el *leave-one-year-out* deja el alfa en **[+4,84, +8,27] pp sin
cambiar de signo**; y la trampa de valor, medida sobre el universo CON muertos, resta solo
~0,7 pp de los 21,6 pp de diferencial. **Pero no descorrelaciona** (0,785, real −0,031) y en
2008 hizo −43,6% frente al −30,1% del Nasdaq. Es la prima de valor, documentada desde
Fama-French: robusta, pero no es un descubrimiento nuestro. Ver `ESTUDIO-SUBTIPOS-CICLICOS.md`.

**C22. El CAGR ordena por beta; el alfa no. Y eso corrige C21.** Sobre las carteras medidas,
**corr(CAGR, correlación con el Nasdaq) = +0,704 pero corr(alfa, correlación) = +0,195**: la
proporcionalidad entre rentabilidad y correlación es aritmética de mercado alcista, no una
ley. Se invierte en años malos — Consumer Cyclical (β 1,35) hizo **−19,2%** y Industrials
(β 0,80) **−10,4%** en los 4 años de caída del Nasdaq. **Corrección a C21:** el cuartil barato
de Indu+Basi tiene **beta 1,46 y alfa Jensen de solo +0,87%** — su 17,79% era casi todo beta.

**C23. Separado por subtipo, el efecto valor es un efecto de INDUSTRIALS.** Cuartil barato
dentro de cada sector: **Industrials baratas es la única cartera de la serie con alfa Jensen
positivo (+1,71%)**, CAGR 15,40% vs 14,29% del Nasdaq, **beta 1,11**, y en años malos del
Nasdaq **−10,9% frente a −12,3%**: cae menos que el índice. El alfa replica (+8,1 pares,
+5,5 impares). Los contrastes enseñan más: **Basic Materials baratas da el CAGR más alto de
todo el estudio (20,99%) y es la peor idea** — beta **2,38**, volatilidad **73,5%**, alfa
−1,72%: es Nasdaq apalancado, no estrategia. En **Consumer Cyclical barato NO funciona**
(alfa −5,62%) y en **Energy no replica** (+6,4 pares, −3,1 impares). **Regla que queda: la
métrica de selección es alfa Jensen con beta ≤ 1,2, nunca CAGR bruto.** Ver
`ESTUDIO-ALFA-VS-BETA.md`.

**C24. Industrials baratas no bate al Nasdaq: el alfa interno es sólido, el externo no.**
Chequeo de rigor sobre C23. CAGR 15,40% vs 13,26%, pero el **alfa Jensen es +2,86% con
SE 5,97%: t = +0,48**, IC95% **[−8,85%, +14,56%]**. Volatilidad **31,7% vs 22,0%**, peor año
**−45,8% vs −32,9%**, y **Sharpe 0,423 frente a 0,512 del Nasdaq: ajustando por riesgo,
pierde.** Bate al índice 9/17 años. El *leave-one-out* **cambia de signo al quitar 2022**
(−3,39%), y el contrafactual aleatorio da p = 0,0638. **Lo que sí queda establecido es el alfa
INTERNO: +6,73 pp con t = +2,31** (baratas vs su propia familia Industrials), lo único de la
serie con |t| > 2. La diferencia entre t=2,31 y t=0,48 es B4 en acción: la comparación interna
es pareada y cancela el ruido de mercado; la externa carga con 31,7% de volatilidad. **Sirve
para elegir qué Industriales comprar, no para decidir comprar Industriales en vez de Nasdaq.**
Criterio declarado para que sea alternativa de cartera y no solo selector: **alfa Jensen con
t ≥ 2 y Sharpe ≥ 0,512**. Ver `NOTA-INDUSTRIALS-NO-BATE-AL-NASDAQ.md`.

---

## D. La conclusión que ordena todo lo demás

**Este panel es un universo de acciones estadounidenses de crecimiento y calidad. Todo lo
que hay dentro correlaciona 0,8–0,9 con todo lo demás.** Buscar descorrelación recortando
subconjuntos de ese universo es buscar un color distinto dentro de un bote de pintura azul:
salen tonos, no colores.

**Los dos caminos que quedaban están ahora explorados, y ninguno lleva a donde queríamos.**

1. **El eje temporal (C10, C11).** Descorrelaciona en 2007–2023 y no descorrelaciona en
   1972–2025. Lo que medimos era la ventana, no la regla. Y cuesta 1–3 pp anuales de forma
   consistente.
2. **Datos de fuera**, que es ya el único camino. Pero la petición ha cambiado: no son
   precios mensuales —el problema nunca fue la frecuencia de la señal, sino **el número de
   mercados bajistas observados**, y a frecuencia mensual seguirían siendo dos—. Es
   **historia larga con universo point-in-time** (CRSP vía WRDS, Sharadar, Norgate).

**Y hay una tarea nueva, barata y anterior a todo eso:** aplicar el test de ventanas de B8 a
todo lo que se midió sobre 17 años, empezando por C7. Se puede hacer hoy, solo con el índice,
sin comprar nada.

## E. Aviso de seguridad pendiente

**RLS está desactivado en `hypergrowth_panel` y otras 8 tablas.** Cualquiera con la anon key
puede leer y escribir todo. No resuelto por decisión del usuario.
