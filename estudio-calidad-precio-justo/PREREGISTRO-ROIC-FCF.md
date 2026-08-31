# Preregistro: ROIC y flujo de caja libre

Escrito **antes** de descargar ningún dato y antes de ver ningún resultado.
Commit anterior: c01b874 (cierre del estudio de deuda).

## Por qué existe este documento

El estudio de deuda acaba de morir de la siguiente manera: encontré el efecto en una
muestra de 74 eventos (p = 0.003), lo di por prometedor, y al ampliarlo a 190 eventos
nuevos el efecto cambió de signo y el p subió a 0.65. El error no fue estadístico: fue
descubrir y confirmar en el mismo sitio, y decidir el corte después de ver los números.

Es la cuarta vez en este estudio (`sector`, `desaceleracion_guia`, deuda a n=75, deuda a
n=263). Así que esta vez las reglas van por delante.

## Hipótesis a contrastar

Que la calidad del capital — medida por ROIC y por generación de caja libre — separa
dentro de la selección los ganadores de los perdedores, y que añadirla como filtro sube
el alfa por encima del 15.42% del escenario C4.

## Datos

Endpoint `key-metrics` de FMP, anual. Campos que se van a usar, fijados aquí:

1. `returnOnInvestedCapital` — ROIC
2. `freeCashFlowYield` — FCF / capitalización
3. `incomeQuality` — caja operativa / beneficio neto
4. `capexToRevenue` — intensidad de capital
5. `cashConversionCycle` — días de ciclo de caja

No se van a mirar otros campos del payload. Si más tarde hiciera falta uno nuevo, se
anota aquí como añadido posterior y se trata como exploratorio, no como confirmatorio.

## Regla de fecha

La misma que en el estudio de deuda, ya validada: entrada el 1 de febrero del año Y,
se usa **el último año fiscal que cierra en o antes del 15 de enero de Y**.

## Partición: descubrimiento y confirmación

Los 263 eventos (190 cíclicos + 73 del piloto) se parten en dos por una regla mecánica
fijada aquí y que no depende de ningún resultado:

- **DESCUBRIMIENTO** = eventos con año par (2008, 2010, 2012, 2014, 2016, 2018, 2020, 2022)
- **CONFIRMACIÓN**  = eventos con año impar (2007, 2009, 2011, 2013, 2015, 2017, 2019, 2021, 2023)

Se parte por año y no al azar porque el riesgo real de esta muestra es que un único año
malo (2008, 2020) arrastre el resultado. Partiendo por año, ningún año cae en las dos
mitades y cada mitad cubre todo el periodo.

Toda la exploración — elegir entre ROIC y FCF, elegir el corte, elegir si es tercil o
mediana — se hace **solo** sobre descubrimiento. Después se aplica la regla ya cerrada
sobre confirmación, **una sola vez**.

## Qué contaría como hallazgo

Se considera que hay efecto si y solo si se cumplen las tres cosas:

1. En confirmación, la diferencia entre el grupo alto y el bajo tiene **el mismo signo**
   que en descubrimiento.
2. En confirmación, `p` de permutación **< 0.05** en el contraste único preespecificado.
3. La diferencia sobrevive al control por sector y al control por año.

Si el signo se invierte, se declara refutado y se escribe así, igual que con la deuda.

## Qué no se va a hacer

- No se va a probar un segundo corte si el primero falla.
- No se va a cambiar la métrica si ROIC no funciona y FCF sí (se reportan las dos, cada
  una con su contraste; no se elige la ganadora a posteriori).
- No se va a ampliar la muestra si el resultado queda cerca de 0.05.

## Limitaciones conocidas de antemano

- 11 minoristas con cierre a finales de enero (DDS, ROST, BURL, PVH, URBN, ULTA, OXM,
  GIII, SHOO, MOV, LZB) tendrán el dato con ~12 meses de retraso. Es correcto pero
  desigual.
- La muestra está sesgada a cíclicas e industriales por cómo se construyó, así que el
  resultado no se puede extrapolar sin más al panel entero.
- `sector` viene del perfil actual de FMP, con el problema de tickers reutilizados ya
  documentado en `NOTA-TICKERS-REUSADOS.md`.
