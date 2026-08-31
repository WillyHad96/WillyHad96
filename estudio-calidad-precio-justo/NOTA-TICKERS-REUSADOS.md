# Tickers reutilizados detectados durante la descarga de deuda

Al descargar `enterprise-values` para los 129 eventos ciclicos/industriales aparecieron
sImbolos cuyo historico en FMP mezcla dos empresas distintas. Esto es un riesgo real de
contaminacion, del mismo tipo que el sesgo de `sector` ya documentado en
ESTUDIO-DELISTINGS.md.

## SGI - EXCLUIDO del analisis de deuda
- Evento del panel: 2007, ventas 360 M USD, etiquetado "Consumer Cyclical".
- La serie de FMP bajo SGI tiene dos bloques incompatibles: filas con cierre en junio
  (2011-2016, Silicon Graphics / Rackable) y filas con cierre en diciembre desde 2020
  con ~200 M de acciones y ~1.7-8 B de deuda, que corresponden a Somnigroup /
  Tempur Sealy (SGI desde 2025).
- El balance a 2006-12-31 que devuelve la API (deuda 19.9 M, caja 30.4 M, 155 M acciones,
  precio 5.11) no cuadra con Silicon Graphics, que en 2006 salIa de Chapter 11.
- Decision: se excluye el evento. 1 de 192.

## TEN - INCLUIDO, con reserva
- Evento del panel: 2014, ventas 7964 M USD, etiquetado "Energy".
- TEN fue Tenneco hasta 2022 (compra por Apollo) y hoy es Tsakos Energy Navigation.
  La etiqueta "Energy" viene de Tsakos, no de la empresa del evento.
- El balance usado (2013-12-31: deuda 1380 M, caja 172 M, 60.5 M acciones) es coherente
  con Tenneco, no con Tsakos (que en 2013 tenIa ~46 M acciones). Se mantiene.

## DCH - EXCLUIDO por duplicado
- DCH es un simbolo duplicado de American Axle (AXL), ya capturado. Se omite para no
  contar el mismo evento dos veces.

## Implicacion general
La etiqueta `sector` del panel se tomo del perfil ACTUAL de FMP. Para tickers reutilizados
esa etiqueta describe a la empresa que ocupa hoy el simbolo, no a la del evento. Es otra
via del mismo look-ahead ya identificado.

## UGP - EXCLUIDO por moneda mezclada
- Ultrapar (ADR brasileno). En `enterprise-values` de FMP la capitalizacion viene en USD
  (precio ADR x acciones) pero `addTotalDebt` y `minusCashAndCashEquivalents` vienen del
  balance reportado en BRL.
- Para el evento 2007 eso daria deuda 1546 M frente a ventas 2197 M (= 0.70x) cuando el
  ratio real en una sola moneda es ~0.33x. Un error de mas del doble en el ratio que
  precisamente estamos ordenando.
- Es el unico emisor del grupo que no reporta en USD (ESLT, JHX, ARCO, HBM, DAC, GIL y
  TGLS si lo hacen). Se excluye. 1 de 192.
