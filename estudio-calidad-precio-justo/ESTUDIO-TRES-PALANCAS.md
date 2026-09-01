# Las tres cosas que podían mover la cifra: qué mueve cada una

Continuación de `ESTUDIO-MITADES.md`. Ataco las tres pendientes que quedaban sobre
la reconstrucción de C4 (14,16% de CAGR 2007–2023, NASDAQ 13,89%).

**Resumen: dos de las tres no mueven casi nada. La tercera mueve +1,03 pp — y de paso
destapa el problema serio, que no es ninguna de las tres.**

| palanca | efecto sobre el CAGR |
|---|---|
| 2. Sector: excluir financieras e inmobiliarias | **+0,31 pp** (14,16 → 14,47) |
| 2b. Sector: quitar la misma empresa duplicada bajo varios tickers | **+0,71 pp** (14,16 → 14,87) |
| 2 + 2b juntas | **+1,03 pp → 15,19%** |
| 1. Precio de salida de las que no cotizan al cierre | **−0,05 pp** (supuesto neutro) |
| 3. Umbrales del año anterior en vez del año en curso | **+0,07 pp** |

Con las dos correcciones del punto 2 la reconstrucción da **15,19%** frente al **15,42%**
documentado. Cierra el 82% del hueco que quedaba abierto en `ESTUDIO-MITADES.md`.

---

## Punto de partida: `sector` no es nulo, es `'desconocido'`

Primera corrección de método. El campo `sector` **no tiene un solo nulo** en las 431.259
filas del panel. El hueco es un centinela: `sector = 'desconocido'`, que cubre **5.105 de
los 6.967 tickers (73%)**. El bucket "sin sector" de `ESTUDIO-MITADES.md` era eso, y sus
cifras quedan confirmadas.

## 2. Sector: recuperados 121 de 122 tickers

Bajados con `profile-symbol` de FMP, que devuelve perfil también para deslistadas
(LNCE → Snyder's-Lance, `isActivelyTrading:false`). Guardados en `sect_recuperado.csv`.
El único que no resuelve es **LDL (Lydall)**: aparece en la búsqueda por nombre pero
`profile-symbol` no devuelve datos. 1 evento, peso despreciable.

### 2a. La composición: confirma y refuerza el estudio de mitades

Peso en cartera con cobertura sectorial **completa**:

| sector | peso H1 | peso H2 | dif | exc H1 | exc H2 |
|---|---|---|---|---|---|
| Consumer Cyclical | 26,7% | 17,4% | **−9,3** | +0,4 | −4,8 |
| Technology | 23,8% | 26,5% | **+2,7** | −3,0 | +11,6 |
| Industrials | 15,0% | 18,3% | +3,3 | −10,5 | +8,6 |
| Healthcare | 16,4% | 14,9% | −1,5 | −1,2 | −7,2 |
| Consumer Defensive | 6,1% | 8,7% | +2,6 | +8,2 | +5,6 |
| Basic Materials | 4,5% | 3,3% | −1,2 | +6,9 | +25,6 |
| Communication Services | 3,8% | 3,8% | 0,0 | −26,5 | +7,6 |
| Financial Services | 1,4% | 3,3% | +1,9 | −3,3 | −2,3 |
| Real Estate | 1,4% | 2,6% | +1,2 | +18,2 | −11,8 |
| Energy | 1,1% | 1,0% | −0,1 | −2,1 | −25,1 |

- **Cíclicas** (ConsCyc + Industriales + Materiales + Energía): **47,3% → 40,0%. Bajan.**
- **Tecnología: +2,7 pp.** Sigue siendo nada.
- Dentro de cada sector el exceso sí se mueve mucho: Tecnología −3,0 → +11,6;
  Industriales −10,5 → +8,6. Es **selección**, no rotación sectorial.

Con el dato completo la conclusión de `ESTUDIO-MITADES.md` no solo se mantiene: se
refuerza. La cartera de la segunda mitad es *menos* cíclica, no más tecnológica.

### 2b. La misma empresa comprada dos y tres veces

Al cruzar los perfiles aparecen tickers distintos con **el mismo CIK y el mismo CUSIP**:

| empresa | tickers en cartera | años afectados |
|---|---|---|
| Light & Wonder / Scientific Games | **LNW, LNWO, SGMS** | 2012, 2018, 2021 |
| iRobot | IRBT, IRBTQ | 2017 |
| Revlon | REV, REVRQ | 2010 |

Y otros pares que se detectan por retorno idéntico: UPBD/RCII (2020, 2021), CSWI/CSW
(2021, 2023), BRKS/AZTA (2018), CSU/SNDA (2013), AXL/DCH (2014, 2015).

Son **13 eventos duplicados** de 664. En 2018 Light & Wonder entra **tres veces**, con
pesos 1936 + 1849 + 1764 — el 15% de la cartera de ese año en una sola empresa. Quitando
duplicados el CAGR sube a **14,87% (+0,71 pp)**, más que la corrección de sector.

### 2c. Lo que de verdad importa: `desconocido` predice el retorno

Con los sectores rellenados se puede hacer la pregunta correcta: la penalización del
bucket "desconocido" (−8 a −9 pp en las dos mitades), ¿era composición sectorial, o es
el propio hecho de estar sin clasificar?

Test de permutación **estratificado**: dentro de cada celda (año × sector) que contiene
ambos grupos, se permuta la etiqueta `desconocido` y se recalcula la diferencia de
excesos. 81 celdas, 520 eventos, 20.000 iteraciones, semilla 13 (`perm_desc.py`).

| estadístico | diferencia | p |
|---|---|---|
| media simple de las 81 celdas | **−8,98 pp** | 0,064 |
| ponderada por tamaño de celda | **−12,63 pp** | **0,008** |

En 49 de 81 celdas el grupo `desconocido` rinde peor.

**La penalización sobrevive al control por año y por sector.** No es que las sin
clasificar sean de sectores malos: dentro del *mismo* sector y el *mismo* año rinden
entre 9 y 13 pp peor.

Dicho de otro modo: **el predictor más fuerte que ha aparecido en toda esta sesión no es
un factor, es si a la empresa le rellenaron un campo de metadatos.** Eso no es una señal
de inversión, es la firma de un sesgo en los datos.

## 1. El precio de salida: la palanca estaba vacía

La hipótesis era que ~15 empresas mueren dentro del año de tenencia y se les asigna el
último precio del panel en vez del precio real de deslistado.

**No es lo que pasa.** Las guardas de calidad (`p4 is distinct from p4p`, `not ff_ini`,
ventana de validez 0,75–1,25 años) no valoran mal esos eventos: **los descartan**. De
681 selecciones, 17 se caen por no tener retorno usable (2,5% de los eventos, 2,2% del
peso agregado). Solo 3 eventos corresponden a un ticker cuyo historial termina cerca de
la fecha de salida.

El problema real, entonces, no es el precio: es que **la cartera se mide solo sobre las
posiciones que llegaron vivas al final**. Banda de sensibilidad:

| supuesto para las 17 descartadas | CAGR |
|---|---|
| todas a −100% | 10,62% |
| todas al retorno del NASDAQ de ese año | 14,10% |
| base (renormalizando pesos, lo que hace el backtest) | 14,15% |

El extremo de −100% no es creíble: el año que más pesa es 2009, con 8 descartadas y el
17,7% del peso, y entre ellas están **WRK (WestRock), SSNC (SS&C) y DBD (Diebold)** —
empresas que sobrevivieron perfectamente. Se caen por falta de precio limpio, no por
morir. Con el supuesto neutro la palanca mueve **−0,05 pp**.

*(Nota: una versión anterior de este cálculo, con umbrales absolutos en vez de
`percent_rank`, daba 3,82% para el escenario −100%. La cifra buena es 10,62%.)*

## 3. Umbrales y supervivencia: el umbral no es nada, el universo sí

**Umbrales.** Recalculando los cuatro cortes (mediana de sd(margen bruto), mediana de
sd(crecimiento), p25 de regla40, p25 de capitalización) con el universo del **año
anterior** en vez del año en curso: 15,27% → **15,34%** en 2008–2023. **+0,07 pp.**
Confirmado como irrelevante, y además conceptualmente no era look-ahead: los cuatro
cortes se calculan sobre datos observables el 1 de febrero.

**Supervivencia del universo. Esto sí es grave.**

| año | tickers en el panel | % que siguen vivos en el panel en 2025 |
|---|---|---|
| 2002 | 2.420 | **84,4%** |
| 2008 | 3.657 | **83,4%** |
| 2014 | 5.451 | **84,7%** |
| 2020 | 6.538 | 86,5% |

Dos cosas no cuadran:

1. **El 83–85% de supervivencia a 15–20 años es imposible.** En el mercado
   estadounidense real la mortalidad (quiebras, fusiones, exclusiones) se lleva a
   grandes rasgos la mitad de una cohorte en ese plazo. Un corte de 2008 debería tener
   entre el 40% y el 55% de supervivientes, no el 83%.
2. **El número de tickers crece de 366 (1998) a 6.604 (2022).** El universo cotizado
   estadounidense hizo lo contrario: encogió. Ese perfil creciente es la firma de un
   panel construido desde una lista de empresas **actuales** con la historia rellenada
   hacia atrás.

Encaja con el punto 2c: el panel está dominado por supervivientes, los `desconocido` son
la cobertura parcial e incompleta de las que no lo son, y rinden 9–13 pp peor dentro del
mismo sector y año. **Eso es exactamente el aspecto que tiene un sesgo de supervivencia.**

Y no se arregla con los datos que hay. Haría falta una lista del universo cotizado
punto-en-el-tiempo para cada 1 de febrero.

## Dónde queda el alfa

| | CAGR | vs NASDAQ |
|---|---|---|
| reconstrucción base | 14,16% | +0,27 pp |
| con las dos correcciones del punto 2 | **15,19%** | **+1,30 pp** |
| documentado en `ESTUDIO-ALFA-POST-DELISTINGS.md` | 15,42% | — |

Y por encima de todo eso, un universo con el 83% de supervivientes donde debería haber
el 50%. **El +1,30 pp es un techo, no una estimación.**

## Conclusión

- De las tres palancas, **dos estaban vacías** (precio de salida: −0,05 pp; umbrales:
  +0,07 pp) y **una da +1,03 pp**, de la cual dos tercios vienen de un fallo que no
  buscaba: comprar la misma empresa bajo dos o tres tickers.
- Rellenar `sector` no cambió la lectura de las mitades — **la reforzó**: la cartera de
  la segunda mitad es menos cíclica, no más tecnológica.
- Lo que sí ha cambiado es dónde está el problema. No está en el precio de salida ni en
  los umbrales ni en el filtro sectorial. **Está en cómo se construyó el universo.**
  El campo `sector` predice el retorno dentro del mismo sector y año (p = 0,008), y la
  tasa de supervivencia del panel es imposible.
- Antes de seguir buscando factores conviene arreglar eso, porque cualquier alfa medido
  sobre este universo hereda el sesgo. Y el alfa que estamos midiendo es de +0,3 a
  +1,3 pp: del mismo orden que el sesgo.

## Ficheros

- `c4_base.sql` — reconstrucción de C4 en SQL, que no estaba guardada en ningún sitio.
- `sect_recuperado.csv` — 122 tickers con sector, industria, fecha de salida a bolsa y
  si sigue cotizando.
- `tk_desconocido.txt` — la lista de los 122.
- `celdas.txt` — los 520 eventos de las 81 celdas (año × sector) con ambos grupos.
- `perm_desc.py` — el test de permutación estratificado.
