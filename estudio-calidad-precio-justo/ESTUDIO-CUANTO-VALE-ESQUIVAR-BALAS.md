# ¿Cuánto vale esquivar balas? El premio, medido antes de gastar en el estudio

Cálculo previo al estudio de supervivencia, sobre 2021–2023 (el único tramo con registro de
bajas creíble, A1). 8.799 eventos ticker-año. Definición de bala: el ticker desaparece del
panel dentro de los 18 meses siguientes **y** su retorno del último año fue < −25%
(separa quiebra de compra con prima, ver `NOTA-DONDE-ESTAN-LAS-MUERTES.md`).

## 1. Cuántas son y cuánto duelen

| clase | % del universo | retorno medio | p10 | mediana |
|---|---|---|---|---|
| sobrevive | 96,2% | −0,3% | **−54,8%** | −4,4% |
| sale por compra | 2,6% | **+16,7%** | −21,7% | +3,2% |
| **BALA** | **1,2%** | **−54,2%** | −90,7% | −61,2% |

Las balas duelen mucho **pero son pocas**: 106 de 8.799 eventos.

## 2. El dato que mata la idea: el decil inferior no son balas

| tramo | eventos | balas | **% del tramo que es bala** | retorno medio |
|---|---|---|---|---|
| **peor 1%** | 90 | 14 | **15,6%** | −93,3% |
| 1–5% | 351 | 27 | 7,7% | −78,4% |
| 5–10% | 440 | 24 | 5,5% | −61,6% |
| 10–25% | 1.320 | 25 | 1,9% | −40,2% |
| resto | 6.598 | 16 | 0,2% | +16,9% |

**En el peor 1% del universo, el 84,4% son supervivientes teniendo un año catastrófico.** En
el decil inferior completo, las balas son solo el **7,4%**.

Dicho de otra forma: **la cola izquierda no la producen las quiebras. La producen empresas
vivas que caen un 60–90% y siguen cotizando.** Un filtro de solvencia no las toca.

## 3. Lo que vale un filtro PERFECTO

| escenario | media anual | p1 | p5 | **p10** | p25 |
|---|---|---|---|---|---|
| con balas (lo que mide el panel) | −0,53% | −89,3 | −70,9 | **−55,4** | −27,6 |
| **sin balas — filtro perfecto** | **+0,13%** | −88,5 | −69,2 | **−54,2** | −26,7 |
| con balas marcadas a −100% | −1,08% | −100 | −73,9 | −56,6 | −27,8 |

- **Efecto en la media: +0,66 pp anuales.** Si las balas van de verdad a −100% y el panel se
  queda corto (que es lo probable), **+1,21 pp**.
- **Efecto en el percentil 10: 1,2 pp.** De −55,4% a −54,2%.

En una cartera de 15 nombres: probabilidad de llevar al menos una bala en un año dado
**16,6%**; coste esperado **0,65 pp/año** (1,2 pp si van a −100%). Sobre 17 años, unas 3
balas en total.

## 4. Veredicto

**Esquivar balas vale entre 0,7 y 1,2 pp anuales con un filtro perfecto, y los filtros
perfectos no existen.** El error de medición del CAGR de esta serie es **±11,5 pp** (B6).

**El premio es diez veces menor que la barra de error.** No es medible con estos datos, y no
lo será por muchos tickers que se descarguen.

Por eso **no se ejecutan las 27 rondas del estudio de supervivencia.** No porque la idea sea
mala —es la correcta y la literatura la respalda— sino porque **el premio ya está medido y no
llega al umbral de lo detectable.**

## 5. Las dos condiciones que lo cambiarían

Esto no cierra la puerta; la deja con dos llaves concretas:

1. **Si la estrategia compra deliberadamente nombres apalancados y deprimidos** (que es justo
   lo que propone el bloque B del diseño: valoración de suelo), **la tasa de balas en ESE
   subconjunto no es el 1,2% del universo, sino mucho mayor.** El 1,2% es la media de todo el
   mercado, no la de una cartera que va a buscar cíclicas hundidas. **Este cálculo acota el
   caso general, no el caso concreto.**
2. **El panel sigue subregistrando.** Un 1,2% de eventos-año implica una tasa de baja anual
   muy por debajo del 3–5% típico de small caps. Si la tasa real triplica, el premio triplica
   a ~2–3,5 pp, que ya empieza a ser material.

**Regla que queda:** el estudio de supervivencia se ejecuta **cuando y solo cuando** exista
una cartera candidata concreta, y se mide la tasa de balas **dentro de esa cartera**, no en
el universo. Medirlo en el universo es medir el promedio de algo que solo importa en la cola.

## 6. Lo que sí queda comprado con este cálculo

- **La cola izquierda de este universo es un fenómeno de empresas vivas**, no de quiebras.
  Ninguna variable de solvencia va a arreglarla.
- **El 2,6% que sale por compra rinde +16,7% de media.** Las salidas no son un riesgo: en
  agregado son un beneficio. Contarlas todas como muertes —que es lo que haría una corrección
  ingenua del sesgo de supervivencia— **empeoraría la estimación en vez de mejorarla.**
