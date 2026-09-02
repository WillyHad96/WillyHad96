# Hallazgos que sobreviven

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
tickers (73%).

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

**C10. El eje temporal descorrelaciona de verdad, pero no llega en rentabilidad.** Regla
pre-registrada sin parámetros libres (dentro si el Nasdaq subió los 12 meses previos):
correlación **0,918 → 0,549**, descorrelación real **−0,221** (p = 0,013 contra el null de
permutación), peor año **−42,5% → −7,3%**. **Es el mejor resultado de descorrelación de toda
la serie** — frente al −0,14 de C7, y con contraste que lo respalda, que C7 no tenía. Pero el
CAGR cae a 12,01% (Nasdaq 13,89%) y **el signo del efecto sobre la rentabilidad cambia al
quitar un solo año**: −6,48 pp sin 2008, +0,54 pp sin 2023. El alfa interno pareado es
−3,71 pp con t = −0,79: no distinguible de cero. **La descorrelación queda establecida; la
rentabilidad queda indeterminada.** Ver `ESTUDIO-EJE-TEMPORAL.md`.

---

## D. La conclusión que ordena todo lo demás

**Este panel es un universo de acciones estadounidenses de crecimiento y calidad. Todo lo
que hay dentro correlaciona 0,8–0,9 con todo lo demás.** Buscar descorrelación recortando
subconjuntos de ese universo es buscar un color distinto dentro de un bote de pintura azul:
salen tonos, no colores.

De los dos caminos que quedaban, **el primero ya está explorado** (C10) y el resultado parte
la pregunta en dos mitades con respuestas distintas:

1. **El eje temporal SÍ descorrelaciona** — 0,918 → 0,549, robusto, significativo. Es lo
   único de toda la serie que lo consigue. **Pero no se puede saber si mantiene la
   rentabilidad**, y no por falta de ideas: por aritmética (B6). Con 17 observaciones anuales
   la pregunta no se cierra.
2. **Datos de fuera**, que ahora es el cuello de botella real. Por orden:
   - **Precios mensuales del índice.** Barato, no exige tocar el panel, y lleva la señal de
     17 a ~200 observaciones. Es lo que más desbloquea, con diferencia.
   - Historia pre-2007 con precios que se muevan (A6), que añadiría 2000–2002.
   - Universo point-in-time (Sharadar, Norgate, CRSP), que resuelve A1–A4 de raíz.

## E. Aviso de seguridad pendiente

**RLS está desactivado en `hypergrowth_panel` y otras 8 tablas.** Cualquiera con la anon key
puede leer y escribir todo. No resuelto por decisión del usuario.
