# Compras de insiders por tramos de % del capital

Estudio de eventos sobre compras en mercado abierto declaradas en el Formulario 4
de la SEC, con la pregunta: **¿aporta ventaja filtrar las señales de insider por el
tamaño de la compra respecto a la capitalización de la empresa?**

Informe (artifact): https://claude.ai/code/artifact/a3451039-d94a-4583-acbe-15ec5440db3b
Copia local: [`report.html`](report.html)

## Hipótesis de partida

Muchas compras de directivos son simbólicas: importes minúsculos que solo sirven para
que salte la señal en los screeners. Si es así, filtrar por compras grandes **en
proporción al capital** debería separar la convicción real del ruido.

## Resultado corto

- **La premisa se confirma.** La compra mediana de un directivo son **67.656 $**, un
  **0,012 % del capital** (1,2 puntos básicos). El percentil 25 son 14.438 $. La mitad
  de las señales son, en efecto, calderilla.
- **La conclusión no se sostiene.** Ordenar por % del capital no produce una ventaja
  fiable. El bootstrap por empresa da **−3,1 pp** de diferencia entre el tramo alto
  (≥0,15 %) y el bajo (<0,05 %), con IC 95 % **[−16,2, +8,5]**: cruza el cero.
- **El tramo más grande es el peor.** Compras de **>0,50 % del capital**: mediana a 12
  meses **−7,8 %**, tasa de acierto **42 %**, **−22,1 pp** frente al IWM. Sin 2020 sigue
  igual de mal (−9,2 %, 39 % de acierto). Una compra enorme respecto al tamaño de la
  empresa suele ser señal de que la empresa es diminuta y está en problemas, no de
  convicción.
- **El CAGR aparente es de 2020.** La regla ≥0,05 % del capital rinde 42,6 % anual
  compuesto sobre la muestra completa, pero **16,4 % sin las cuatro cohortes de 2020**;
  la de ≥0,15 % pasa de 30,1 % a **6,6 %**. Son carteras de 4 a 8 nombres.
- **La correlación no baja lo suficiente.** Correlación trimestral con el QQQ de
  **+0,44 a +0,68** según el filtro, con beta 0,79–1,78. No resuelve el objetivo de
  "rentabilidad tipo Nasdaq con poca correlación".

## Metodología

- **Universo**: 150 símbolos muestreados de forma estratificada por capitalización a
  partir de las páginas de actividad insider de todo el mercado
  (`data/universe_sample.json`).
- **Ventana**: transacciones de 2014-01-01 a 2025-08-31.
- **Filtro de transacción**: solo `P-Purchase` sobre acción ordinaria (`common` u
  `ordinary` en `securityName`, excluyendo warrants, preferentes, unidades, opciones,
  notas, derechos, convertibles y ADR depositarios).
- **Agregación**: los eventos se agrupan por símbolo-mes natural, sumando el importe de
  todas las compras del grupo.
- **Entrada**: la **fecha de declaración más tardía** del grupo, no la de la
  transacción. Es lo primero que un inversor externo podría haber sabido; evita el
  look-ahead. Se descartan declaraciones con más de 45 días de retraso (correcciones y
  presentaciones tardías).
- **Separación crítica**: los eventos se parten entre **directivos/consejeros** y
  **titulares del 10 %**. Es imprescindible: el **80 % de las compras de más de 2 M$**
  son de titulares del 10 %, y suelen ser PIPEs y operaciones estructuradas, no
  convicción de gestión. Mezclarlos contaminaba por completo los tramos altos.
- **Retornos**: total return ajustado por dividendos a +91/+182/+365 días naturales
  (primer día de cotización disponible, con hueco máximo de 15 días), contra QQQ, IWM y
  SPY. El **IWM es la comparación justa**: la capitalización mediana de la muestra es
  microcap.
- **Significación**: bootstrap con clusters **por empresa** (4.000 repeticiones). Los
  eventos de un mismo símbolo no son independientes; un bootstrap por evento
  sobreestimaría muchísimo la precisión.

## Contenido

```
data/insider_events.csv     1.762 eventos símbolo-mes con tramos y retornos futuros
data/universe_sample.json   los 150 símbolos de la muestra
scripts/build_events.py     construye los eventos a partir de los volcados de la API
scripts/analyze_tiers.py    tablas de tramos, control de tamaño, bootstrap, estrategia
scripts/harvest_tool_results.py  ordena los volcados de la API en data/{insider,price,mcap}
report.html                 el informe
```

Para reproducir las tablas del informe basta con el CSV incluido:

```
python3 scripts/analyze_tiers.py
```

`build_events.py` y `harvest_tool_results.py` necesitan los volcados en bruto de la API,
que no se versionan por tamaño.

## Limitaciones

- 150 símbolos, 116 empresas con eventos utilizables. Es una muestra, no el mercado.
- Sesgo de supervivencia: el universo se construyó a partir de la actividad insider
  actual, así que las empresas excluidas de bolsa están infrarrepresentadas. Empuja los
  resultados **al alza**, sobre todo en los tramos de microcap.
- Media y mediana divergen mucho (media 12 m del tramo 0,15-0,50 %: +34,6 %; mediana:
  +11,4 %). En microcaps unos pocos multibaggers mueven la media; la mediana describe
  mejor la experiencia típica.
- Sin costes de transacción ni deslizamiento. En microcaps con poca liquidez esto
  importa mucho.
- Las carteras trimestrales tienen entre 3 y 8 nombres en los filtros restrictivos.

## Siguientes pasos sugeridos

1. Ampliar el universo a 500-1.000 símbolos con reconstrucción histórica de la lista de
   cotizadas, para atacar el sesgo de supervivencia.
2. Probar el **incremento de participación** (`stake_inc`, ya en el CSV) como señal en
   lugar del % del capital: mide convicción relativa al patrimonio del directivo, no al
   tamaño de la empresa.
3. Cruzar la señal con calidad de balance para excluir el patrón "compra enorme en
   empresa diminuta en apuros" que hunde el tramo >0,50 %.
