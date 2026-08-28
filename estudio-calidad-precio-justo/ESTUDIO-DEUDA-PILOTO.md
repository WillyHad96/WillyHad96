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
