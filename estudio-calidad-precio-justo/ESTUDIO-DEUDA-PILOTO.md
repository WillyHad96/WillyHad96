# Deuda neta: piloto sobre 69 eventos

Descargados datos de balance de FMP (`enterprise-values`, anual) para **46 empresas y 74
eventos** de la selección C4 — el 11% de los 645 totales. Es un piloto, no el estudio completo.

**Resultado corto: la deuda predice los retornos con fuerza, pero NO por la razón que yo dije.
Mi hipótesis principal queda refutada, y aun así el hallazgo es el más prometedor del estudio.**

---

## 1. Lo que encontré

Deuda neta = deuda total − caja, en el ejercicio **anterior** a la compra. Normalizada por ventas.
Excluidos REITs y bancos (5 eventos), donde la deuda no significa lo mismo.

**Muestra operativa: 69 eventos, 42 empresas.**

| Tercil de deuda neta / ventas | n | Rango | Ret. medio | Ret. mediana | **vs NASDAQ** |
|---|---|---|---|---|---|
| **T1 (poca o ninguna)** | 23 | −1,42 a 0,03 | **+34,3%** | **+40,1%** | **+13,8** |
| T2 (media) | 23 | 0,04 a 0,27 | +1,9% | −0,4% | +0,7 |
| **T3 (mucha)** | 23 | 0,29 a 2,59 | +7,8% | 0,0% | **−12,6** |

**Diferencia T1 − T3: +26,5 pp de exceso sobre el NASDAQ.**
**Permutación (20.000 simulaciones): p = 0,0057.**

Partiendo en dos por caja neta frente a deuda neta:

| | n | Ret. medio | Ret. mediana |
|---|---|---|---|
| Con **caja** neta | 20 | +31,2% | **+40,2%** |
| Con **deuda** neta | 49 | +7,9% | **−0,3%** |

Cuarenta puntos de diferencia en la mediana.

---

## 2. Mi hipótesis principal era falsa

Escribí: *"En una cíclica el apalancamiento es el riesgo. Es casi seguro donde viven nuestras
caídas del −60%."* **No es cierto.**

| | Deuda neta / ventas (mediana) |
|---|---|
| Los 8 desastres (retorno < −30%) | 0,18 |
| Los 61 restantes | 0,11 |
| **p (permutación)** | **0,38** |

No predice nada en la cola izquierda. Y basta mirar los peores:

| Ticker | Año | Retorno | DN/Ventas | |
|---|---|---|---|---|
| MAX | 2021 | −81,3% | 0,27 | deuda normal |
| **CIR** | 2008 | −52,8% | **−0,02** | **con caja neta** |
| BWA | 2008 | −52,0% | 0,08 | deuda baja |
| CATM | 2017 | −51,5% | 0,34 | |
| **HIMX** | 2014 | −45,1% | **−0,03** | **con caja neta** |
| AXL | 2015 | −42,5% | 0,35 | |
| LNW | 2018 | −35,3% | 2,59 | muy endeudada |
| BCC | 2018 | −33,1% | 0,06 | deuda baja |

Dos de los cinco peores desastres tenían **caja neta**. El apalancamiento no es lo que te
arruina en esta cartera.

**Lo que sí hace la deuda es desplazar toda la distribución hacia abajo**, no engordar la cola.
Es un efecto sobre el caso típico, no sobre el desastre. Menos espectacular de contar, pero más
útil: un efecto sobre la mediana se captura con una cartera diversificada; un efecto sobre la
cola, no.

---

## 3. Los avisos, que son serios

### a) Puede ser el tipo de empresa, no la deuda

| | T1 (poca deuda) | T3 (mucha deuda) |
|---|---|---|
| Empresas | ATGE, CIR, CVLT, DIOD, DRQ, EVBG, FORM, GLOB, GNTX, HEI, HIMX, HURN, INSP, IRBT, KFRC, MED, MELI | AIMC, ATGE, AXL, BALL, BDC, CATM, CBRE, CCOI, CNK, DLX, EPAC, HEI, HURN, LNW |
| Margen operativo medio | 8,5% | 11,5% |
| Año medio de entrada | 2014,9 | 2015,4 |

Los años y los márgenes son casi idénticos — **no es un efecto de calendario ni de
rentabilidad**. Pero T1 es visiblemente más tecnológica y T3 más industrial. Parte del efecto
puede ser sector disfrazado de deuda. El exceso se mide contra el NASDAQ, lo que ayuda, pero no
lo resuelve.

### b) El control intra-empresa es flojo

Once empresas aparecen con niveles de deuda muy distintos en años distintos. Comparando cada una
consigo misma:

**Media +5,5 pp a favor de la versión menos endeudada, ganando en 7 de 11.** Con dos casos
enormes en direcciones opuestas (ATGE +117,5; INSP −77,2).

Eso es mucho más débil que los +26,5 pp del corte transversal, y sugiere que **buena parte del
efecto está entre empresas, no dentro de cada una.** Es decir: probablemente sí hay sector
metido dentro.

### c) Es el 11% de la muestra

69 eventos de 645. La significancia es real (p=0,0057) pero el intervalo es ancho.

---

## 4. Estimación preliminar

| | n | Ret. medio | vs NASDAQ |
|---|---|---|---|
| C4 sin filtro | 69 | +14,7% | +0,6 pp |
| C4 + deuda neta/ventas ≤ mediana | 35 | **+21,8%** | **+7,2 pp** |

**No es un backtest de cartera** — no tengo años completos, así que no se puede encadenar un
CAGR. Es la media de los eventos disponibles. Tómalo como indicación de magnitud, no como
resultado.

---

## 5. Qué haría ahora

**Completar la descarga.** Faltan 383 de los 429 tickers. Con `enterprise-values` cuesta unas
5.000 filas anuales, perfectamente asumible. Con la muestra completa se podría:

1. Reconstruir **años completos** y hacer un backtest de cartera de verdad, con CAGR encadenado
   y partición temporal.
2. Controlar el sector: ahora sí, pidiendo `profile-symbol` para los 429 tickers, incluidos los
   delistados.
3. Hacer el contraste intra-empresa con n suficiente, que es el que de verdad separa "la deuda
   importa" de "las empresas con poca deuda son de otro tipo".

**Es el hallazgo más prometedor que ha salido en todo el estudio**: +26,5 pp entre extremos con
p=0,0057, sobre un factor que no estaba en la tabla y que tú señalaste. Pero está a medio probar,
y los dos avisos de arriba son exactamente el tipo de cosa que ya nos ha engañado dos veces
(`sector` y la disponibilidad de la guía).

### Lo que este piloto ya deja cerrado

- **La deuda no predice las quiebras ni los desplomes** en esta cartera (p=0,38). Si el objetivo
  era protegerse de la cola izquierda, este no es el camino.
- **Sí desplaza la mediana**, y mucho.
- Los datos que faltaban existen y son baratos de traer: el cuello de botella era saber pedirlos,
  no el plan.

---

## 6. Control por sector (añadido): el efecto no es tecnología, pero tampoco es cíclicas

Sectores obtenidos del panel para 33 de los 46 tickers; los 13 restantes (delistados) los completé
yo, y va marcado en `sectores.csv`.

### Composición de los extremos

| Sector | T1 (poca deuda) | T3 (mucha deuda) |
|---|---|---|
| Technology | **9** | 5 |
| Industrials | 5 | 6 |
| Consumer Cyclical | 4 | 5 |
| **Communication Services** | **0** | **5** |
| Consumer Defensive | 2 | 1 |
| Energy / Healthcare | 2 | 0 |

T1 es un 41% tecnología frente al 23% de T3 — el sesgo que sospechaba existe.

### Y aun así el efecto sobrevive… salvo donde más importaba

| Submuestra | n | T1 vs NASDAQ | T3 vs NASDAQ | Diferencia | p |
|---|---|---|---|---|---|
| Muestra completa | 68 | +10,5 | −14,7 | **+25,3 pp** | **0,0091** |
| **Sin Technology** | 50 | +14,6 | −13,2 | **+27,8 pp** | **0,0100** |
| **Sólo cíclicas e industriales** | 38 | −4,3 | −10,0 | **+5,7 pp** | **0,27** |

**No es un efecto tecnología**: quitando el sector entero, la diferencia *sube* a +27,8 pp y el p
se mantiene en 0,010. Eso descarta el confundido que yo temía.

**Pero se evapora dentro del núcleo cíclico-industrial**, que es el 53% de nuestra cartera y
justamente donde yo predije que el apalancamiento sería decisivo. Ahí quedan +5,7 pp con p=0,27:
nada.

Mirando la tabla de composición se ve de dónde sale: **los cinco Communication Services del T3**
(CCOI, CNK, DLX, MAX, LNW) son medios, cable y juego muy endeudados que lo hicieron mal, y no hay
ninguno en T1. Buena parte de los +25 pp es ese puñado de nombres.

### Lectura honesta

Es la tercera vez que un hallazgo sobrevive al primer control y se cae en el segundo. El efecto
de la deuda es real en la muestra amplia, pero **no funciona donde lo necesitábamos** y descansa
en un grupo pequeño y sectorialmente concreto. Como filtro general sigue teniendo interés; como
protección de la cartera cíclica que tenemos, no está demostrado.

---

## 7. La descarga completa está bloqueada en esta sesión

El proxy de egreso de esta sesión no permite `financialmodelingprep.com`: devuelve **403
Forbidden**. El README del proxy es explícito — un 403 significa que el destino no está en la
política de la organización, y que no hay que reintentar ni rodearlo.

La herramienta MCP de FMP sí funciona porque va por otra ruta, pero `bajar_deuda.py` no puede
ejecutarse aquí. El script está escrito, probado de sintaxis y commiteado: **funciona si se
ejecuta fuera de esta sesión**, con `FMP_KEY=... python3 bajar_deuda.py`.

---

## 8. Lectura intermedia sobre cíclicas e industriales (n=75)

Descargados 37 eventos nuevos de empresas cíclicas e industriales (2 lotes de 10), que sumados a
los 38 del piloto **doblan la muestra** en el subgrupo donde el efecto había fallado.

| Tercil | n | Rango DN/ventas | Ret. medio | Ret. mediana | vs NASDAQ |
|---|---|---|---|---|---|
| T1 poca deuda | 25 | −0,36 a 0,08 | +4,4% | **−5,0%** | **−0,6** |
| **T2 media** | 25 | 0,08 a 0,22 | **+14,1%** | **+17,4%** | **+4,2** |
| T3 mucha deuda | 25 | 0,23 a 2,59 | +5,6% | +6,1% | −7,7 |

**T1 − T3 = +7,1 pp, permutación p = 0,182** (con n=38 era +5,7 pp, p = 0,27).

Dos señales, y la segunda pesa más que la primera:

1. **Doblar la muestra apenas movió el p** (0,27 → 0,18). Si el efecto tuviera el tamaño que
   sugería el piloto, debería haberse acercado mucho más a la significancia.
2. **La relación no es monótona: gana el tercil del medio.** T2 hace +17,4% de mediana y +4,2 pp
   sobre el NASDAQ; T1, el de poca deuda, hace **−5,0% de mediana**. Eso no es "menos deuda es
   mejor", es una joroba — y una joroba con 25 observaciones por tercil es la forma habitual del
   ruido, no la de un mecanismo.

Encaja con lo ya sabido: el +25 pp del piloto venía de comparar tecnología con caja neta contra
medios y cable muy endeudados. **Dentro del núcleo cíclico-industrial, que es el 53% de la
cartera, el efecto no aparece.**

### Estado de la descarga

37 de 194 eventos nuevos. Quedan 8 lotes. Recomendación: **parar aquí** — la forma de los datos
ya apunta a un nulo, y terminar la descarga son muchas vueltas para confirmarlo.

El mismo esfuerzo rinde más en **ROIC y flujo de caja libre**, que están en `key-metrics`, no
dependen del apalancamiento, y son las otras dos hipótesis de `AUDITORIA-DATOS.md`.

### Ficheros

- `ciclicas_eventos.txt` — los 194 eventos cíclicos/industriales con año, ventas, retorno y QQQ
- `ciclicas_limites.txt` — los 129 tickers con los años de histórico que necesita cada uno
- `deuda_cic.csv` — deuda y caja descargadas hasta ahora (37 eventos)
- `interim.py` — el contraste de esta sección
