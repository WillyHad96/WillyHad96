# Estudio ROIC y flujo de caja libre — refutado

Preregistro: `PREREGISTRO-ROIC-FCF.md` (escrito antes de descargar nada).
Regla cerrada: `REGLA-CERRADA-ROIC-FCF.md` (escrita después del descubrimiento y **antes**
de mirar la confirmación).
Datos: `km.csv`. Código: `km_lib.py`, `desc_km.py`, `conf_km.py`.

## Resultado en una línea

La calidad del capital medida por ROIC y por generación de caja libre **no separa**
ganadores de perdedores dentro de la selección. Los dos contrastes preespecificados
cambian de signo entre descubrimiento y confirmación. No se añade ningún filtro al modelo.

## Datos

264 eventos con las cinco métricas descargadas (190 cíclicas + 74 del piloto), cobertura
completa: ni un evento del universo se quedó sin dato y ninguno sobra. Uno del piloto se
descarta por no tener retorno (placeholder 0/0), así que el análisis corre sobre 263.

Campos, tal como los fijó el preregistro y sin añadir ninguno:
`returnOnInvestedCapital`, `freeCashFlowYield`, `incomeQuality`, `capexToRevenue`,
`cashConversionCycle`. Regla de fecha: último ejercicio que cierra en o antes del 15 de
enero del año de entrada.

Partición mecánica: años pares = descubrimiento (119), años impares = confirmación (144).

## Descubrimiento (119 eventos, años pares)

| contraste | ALTO-BAJO | p |
|---|---|---|
| ROIC por tercil | +1.98 pp | 0.832 |
| ROIC por mediana | +7.73 pp | 0.263 |
| FCFY por tercil | −10.51 pp | 0.240 |
| FCFY por mediana | −2.30 pp | 0.745 |

Exploratorias, no preespecificadas como contraste: incomeQuality −5.64 pp (p=0.53),
capexToRevenue −4.02 pp (p=0.61), cashConversionCycle −8.88 pp (p=0.31).

Nada llegó ni cerca de 0.05 en la mitad de descubrimiento. Ya ahí la lectura honesta es
que no hay señal; el paso a confirmación se hizo porque el preregistro lo exige, no
porque hubiera nada prometedor que confirmar.

Detalle que conviene retener: ROIC por terciles sale en **U** (T1 +7.87, T2 +1.69,
T3 +9.85). El tercil de ROIC bajo lo hace casi igual de bien que el alto. Que la mediana
diera más diferencia que el tercil es consecuencia de esa forma, no de un efecto fuerte.

## Confirmación (144 eventos, años impares) — una sola pasada

| contraste | descubrimiento | confirmación | p | signo |
|---|---|---|---|---|
| ROIC por mediana | +7.73 pp | **−1.37 pp** | 0.807 | invertido |
| FCFY por tercil | −10.51 pp | **+4.72 pp** | 0.506 | invertido |

Ninguno cumple la condición 1 (mismo signo). Ninguno cumple la condición 2 (p<0.05).
La condición 3 ni llega a evaluarse, pero los controles se corrieron igual y tampoco
rescatan nada:

- ROIC dentro de año: −7.77 pp (p=0.17). Dentro de sector: −3.48 pp (p=0.55).
- FCFY dentro de año: +8.91 pp (p=0.23). Dentro de sector: +11.43 pp (p=0.14).

Los controles mueven los números más que el propio contraste, que es la firma de ruido.

Contexto, no test: sobre los 263 juntos, ROIC por mediana da +2.58 pp (p=0.56) y FCFY por
tercil −1.26 pp (p=0.82). Es decir, ni siquiera juntando las dos mitades — lo que sería
exactamente el error que mató el estudio de deuda — aparece nada.

## Qué significa

Dentro de esta selección, saber si una empresa gana un 6% o un 13% sobre el capital
invertido no dice nada sobre lo que hará la acción los doce meses siguientes. Lo mismo
con la caja libre. La explicación más simple es que el filtro de entrada (crecimiento +
regla 40 + capitalización) ya deja fuera a las empresas de calidad de capital
verdaderamente mala, y lo que queda dentro está demasiado apretado para que la métrica
discrimine.

Sobre FCFY hay además el problema que ya se anotó al cerrar la regla: `freeCashFlowYield`
lleva la capitalización en el denominador, así que ordenar por él es en parte ordenar por
lo barato que estaba el valor. Que el signo se invierta entre mitades quita interés a la
discusión, pero si algún día se retoma, hay que usar FCF sobre ventas o sobre capital
empleado, no sobre precio.

## Lo que sí funcionó esta vez: el método

Quinta vez que un efecto aparente muere al controlarlo (`sector`, `desaceleracion_guia`,
deuda a n=75, deuda a n=263, y ahora ROIC/FCF). La diferencia es que esta es la primera
que muere **sin haberme costado nada**: las reglas estaban escritas antes, la partición
era mecánica, y la confirmación se corrió una sola vez. No hubo ocasión de engañarse.

El coste de haberlo hecho al revés se ve en el estudio de deuda: +30.34 pp con p=0.003 en
74 eventos que resultaron ser un espejismo.

## Estado del modelo

Sin cambios. **C4 (regla 40 + capitalización, 15.42%) sigue siendo lo único que ha
sobrevivido a un control fuera de muestra.** No se añade filtro de ROIC ni de caja libre.

## Limitaciones

- Muestra sesgada a cíclicas e industriales por construcción; no se puede extrapolar al
  panel entero.
- 11 minoristas con cierre a finales de enero reciben el dato con ~12 meses de retraso.
  Es correcto según la regla de fecha, pero desigual respecto al resto.
- `sector` viene del perfil actual de FMP, con el problema de tickers reutilizados
  documentado en `NOTA-TICKERS-REUSADOS.md`.
- Los alfas de referencia siguen calculados con el filtro `sector`, que los infla ~5.7 pp.
  Eso afecta al nivel de C4, no a estos contrastes, que son diferencias entre grupos de
  la misma muestra.
