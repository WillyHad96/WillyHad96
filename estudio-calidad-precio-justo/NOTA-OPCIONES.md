# ¿Comprar calls en vez de acciones daría más alfa? No: convierte rentabilidad en seguro

Pregunta del usuario. `opciones.py`.

## 1. ¿Se puede medir con FMP? No, y la aproximación tampoco lo cierra

FMP **no** tiene histórico de cadenas de opciones ni de volatilidad implícita por nombre y
fecha. IBKR tiene opciones pero **en vivo, no histórico**. Para hacerlo bien harían falta
superficies de IV históricas (OptionMetrics/IvyDB, ORATS, CBOE DataShop).

Aproximación hecha: valorar las calls con **Black-Scholes a la volatilidad realizada** del
propio universo (45,2% por nombre). **Y hay que decir que esta aproximación no es limpia en
ninguna dirección**:

- La implícita real suele estar **3–6 pp por encima** de la realizada → mi precio es **barato**.
- Pero Black-Scholes con una sola sigma **infravalora** una distribución con cola derecha
  gorda como ésta (p99 = +205%) → mi precio es **caro** respecto a lo que cobraría un mercado
  que conoce el sesgo.

Los dos efectos van en sentidos opuestos y **sin precios reales no se puede saber cuál manda**.
Así que lo de abajo acota la mecánica, no zanja la rentabilidad.

## 2. A mismo nocional, las calls dan menos y protegen más

Pagas la prima, controlas 1,0 de exposición, el resto en efectivo al 2%:

| estrategia | CAGR | vol | **peor año** | años + | prima |
|---|---|---|---|---|---|
| **acciones, cuartil barato** | **15,40%** | 31,7% | **−45,8%** | 11/17 | — |
| call ATM | 10,54% | 22,4% | **−17,1%** | 10/17 | 18,7% |
| call 10% OTM | 9,19% | 19,7% | −13,2% | 9/17 | 14,9% |
| call 25% OTM | 7,27% | **15,8%** | **−8,8%** | 9/17 | 10,6% |

**Las calls no añaden alfa: restan CAGR y quitan riesgo.** Es una compra de seguro, no una
mejora de rentabilidad. Y el usuario ya declaró que **la volatilidad no le penaliza**, así
que por su propio criterio ese beneficio no cuenta.

## 3. El error de concepto en "ejecutar solo los percentiles que interesen"

**Eso es exactamente lo que una call ya hace sola**: solo ejerces las que acaban en dinero.
Pero **la prima se paga sobre todas**, por adelantado. La opcionalidad de elegir después ya
está comprada y cobrada en el precio. No hay ahí una ventaja que capturar: es la definición
del instrumento.

Y la especificación ingenua —meter todo el capital en primas cada año— es ruinosa: en 2008
**todas** las calls del cuartil barato expiraron sin valor (payoff 0% contra prima 18,7%), lo
que borra la cartera entera. Un año así basta.

## 4. El único dato que sí invita a mirarlo con datos reales

El payoff medio realizado de las calls ATM fue **29,6%** contra una prima teórica de **18,7%**:
**+10,9 pp de margen**, y sigue en **+8,6 pp** subiendo la sigma a 51%. Eso refleja que la
cola derecha real es más gorda que la lognormal que asume Black-Scholes.

**Pero es justo el punto donde mi aproximación es más débil**, porque el mercado de opciones
cotiza esa cola con prima de sesgo (*skew*), y Black-Scholes no. Muy probablemente ese margen
se lo come el *skew* real. **Para saberlo hacen falta precios de opciones históricos, y no los
tenemos.**

## 5. Conclusión

- **Para más alfa: no.** A mismo nocional dan menos CAGR, y el mecanismo que se propone
  ("ejecutar solo lo bueno") ya está pagado en la prima.
- **Para un suelo duro en el peor año: sí, y bastante** — −17,1% frente a −45,8%. Pero eso es
  gestión de riesgo, no alfa, y no encaja con el criterio declarado.
- **Coste de averiguarlo de verdad:** datos de opciones históricos de pago. **No lo
  recomendaría** hasta que exista una estrategia subyacente con alfa demostrado, y hoy lo
  único con |t| > 2 es un selector interno, no una tesis de cartera (C24, C25).
