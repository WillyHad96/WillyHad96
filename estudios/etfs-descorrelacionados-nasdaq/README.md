# Buscando lo que no se mueve con el Nasdaq

Estudio cuantitativo de ETFs y fondos invertibles desde Interactive Brokers que
combinen **baja correlación con el Nasdaq-100** y **rentabilidad comparable**.

Continúa la serie de estudios con datos de FMP; aquí los precios mensuales vienen
del histórico de IBKR y el retorno total (con dividendos) de las series ajustadas
de FMP.

---

## 1. Metodología

| | |
|---|---|
| **Benchmark** | QQQ (Invesco QQQ Trust, Nasdaq-100) |
| **Universo cribado** | ~65 ETFs/fondos US: metales, materias primas, 25 países, sectores, gestión alternativa, bonos |
| **Finalistas analizados** | 16 series completas |
| **Ventana principal** | nov-2016 → ago-2026 (117 retornos mensuales, 9,75 años) |
| **Ventanas de control** | mar-2014 → ago-2026 (12,4 a) · sep-2021 → ago-2026 (5 a) · mar-2014 → dic-2024 (excluye el rally de metales) |
| **Retornos** | totales, con dividendos reinvertidos |
| **Tipo sin riesgo** | 2,0 % (Sharpe) |

**Cómo se construye el retorno total.** Las barras mensuales de IBKR están
ajustadas por splits pero no por dividendos. La serie ajustada de FMP está
retro-ajustada (el último valor es el precio actual), así que
`precio_hoy / adjClose(30-nov-2016)` es el retorno total exacto del periodo. De
ahí se despeja la tasa de dividendo implícita de cada fondo y se reparte
uniformemente entre los meses. Es exacto en acumulado y una aproximación muy
buena en riesgo mensual, porque los dividendos son pequeños y regulares frente a
la volatilidad del precio.

**Limitaciones conscientes:**

- Reparto uniforme de dividendos: no captura el salto del día ex-dividendo.
- Todo en USD. Para una cuenta en EUR hay un riesgo divisa adicional no modelado.
- Sin costes de transacción, spreads ni retenciones fiscales sobre dividendos.
- El cribado inicial usa variaciones de precio (sin dividendos), lo que penaliza
  a los activos de alta rentabilidad por dividendo. Se corrigió manualmente antes
  de seleccionar finalistas.

Reproducible: `python3 analisis.py`, `python3 carteras.py`, `python3 robustez.py`.

---

## 2. Resultado principal

Ventana nov-2016 → ago-2026. Ordenado por rentabilidad.

| Ticker | Qué es | CAGR | Vol | Sharpe | MaxDD | **Corr QQQ** | Beta |
|---|---|---:|---:|---:|---:|---:|---:|
| QQQ | Nasdaq-100 *(referencia)* | 21,2 % | 19,3 % | 1,00 | −32,6 % | 1,00 | 1,00 |
| EWT | Taiwán | 19,8 % | 23,1 % | 0,77 | −36,3 % | 0,72 | 0,86 |
| COPX | Mineras de cobre | 18,7 % | 35,4 % | 0,47 | −55,9 % | 0,48 | 0,88 |
| **GDX** | **Mineras de oro** | **18,4 %** | 34,8 % | 0,47 | −43,4 % | **0,25** | 0,45 |
| URA | Uranio | 18,1 % | 37,2 % | 0,43 | −44,1 % | 0,43 | 0,84 |
| GREK | Grecia | 17,3 % | 25,5 % | 0,60 | −46,2 % | 0,45 | 0,60 |
| ARGT | Argentina | 16,9 % | 33,7 % | 0,44 | −55,8 % | 0,44 | 0,77 |
| XME | Metales y minería US | 16,1 % | 32,1 % | 0,44 | −56,0 % | 0,55 | 0,91 |
| EWY | Corea del Sur | 15,6 % | 31,1 % | 0,44 | −47,9 % | 0,63 | 1,01 |
| EWI | Italia | 15,2 % | 21,7 % | 0,61 | −33,9 % | 0,53 | 0,59 |
| **GLD** | **Oro físico** | **14,2 %** | **15,1 %** | **0,81** | **−23,8 %** | **0,12** | **0,10** |
| ITA | Defensa y aeroespacial US | 13,7 % | 21,7 % | 0,54 | −37,6 % | 0,54 | 0,61 |
| EWP | España | 13,4 % | 20,8 % | 0,55 | −38,6 % | 0,45 | 0,49 |
| EPOL | Polonia | 13,3 % | 27,6 % | 0,41 | −58,0 % | 0,50 | 0,72 |
| SIL | Mineras de plata | 12,9 % | 37,0 % | 0,29 | −51,6 % | 0,32 | 0,61 |
| EWZ | Brasil | 6,2 % | 31,1 % | 0,14 | −49,5 % | 0,31 | 0,50 |

Nada del universo bate al Nasdaq en rentabilidad. Eso ya es un resultado: en esta
década no ha existido "lo mismo pero descorrelacionado". La pregunta útil no es
qué sustituye al Nasdaq, sino **qué se le puede añadir sin pagar rentabilidad**.

---

## 3. Los cinco hallazgos

### 3.1 El oro es el único diversificador real, en todos los regímenes

Correlación 0,12 en la ventana principal y **0,05 en 12,4 años**. Por
subperiodos: 0,04 (2017-19), 0,32 (2020-21), 0,33 (2022), **−0,00 (2023-26)**.
Ningún otro activo del estudio mantiene la correlación cerca de cero cuando el
mercado se estresa.

Lo decisivo no es la correlación media sino **el decil peor**. En los 12 meses en
que el Nasdaq cayó de media −8,7 %:

| | Rentabilidad media del activo |
|---|---:|
| **GLD (oro)** | **+1,1 %** |
| GDX (mineras de oro) | −1,6 % |
| GREK (Grecia) | −4,0 % |
| SIL (mineras de plata) | −4,1 % |
| EWZ (Brasil) | −4,5 % |
| EWP (España) | −5,0 % |
| EPOL (Polonia) | −5,6 % |
| ARGT (Argentina) | −6,0 % |
| EWI (Italia) | −6,3 % |
| ITA (defensa) | −7,4 % |
| URA (uranio) | −9,0 % |
| EWT (Taiwán) | −9,1 % |
| EWY (Corea) | −10,1 % |
| XME (metales) | −11,5 % |

El oro es **el único que gana dinero cuando el Nasdaq se hunde**. Su captura
bajista es −0,06 (sube ligeramente cuando QQQ baja) y su captura alcista 0,35.

### 3.2 La sorpresa: las mineras de oro dieron rentabilidad tipo-Nasdaq sin correlación

GDX: **18,4 % anual con correlación 0,25 y beta 0,45**. Es el único activo del
estudio que se acerca a la rentabilidad del Nasdaq siendo genuinamente
independiente. Su captura bajista es 0,24: en los meses malos del Nasdaq cae una
cuarta parte.

Consecuencia contraintuitiva: **una cartera 80 % QQQ / 20 % GDX rentó *más* que el
Nasdaq puro con *menos* volatilidad y *menos* caída máxima.**

| Cartera | CAGR | Vol | Sharpe | MaxDD |
|---|---:|---:|---:|---:|
| 100 % QQQ | 21,2 % | 19,3 % | 1,00 | −32,6 % |
| 80 % QQQ / 20 % GDX | **21,8 %** | **18,4 %** | **1,07** | **−30,3 %** |

Ojo al apartado 3.5 antes de sacar conclusiones de esta fila.

### 3.3 La trampa: Taiwán y Corea no son diversificación, son Nasdaq con otro nombre

Son los dos países más rentables del cribado (19,8 % y 15,6 %) y por eso aparecen
en cualquier búsqueda de "alternativas rentables". Pero:

- EWT: correlación 0,72 global y **0,77 en 2023-2026** — la única del estudio que
  *sube* con el tiempo. Captura bajista 0,65.
- EWY: correlación 0,63, beta 1,01, captura bajista **0,92**. Prácticamente no
  amortigua nada.

Son TSMC y Samsung/SK Hynix. Comprarlos es doblar la apuesta de semiconductores,
no diversificarla. Rentabilidad sí; descorrelación no.

### 3.4 Las sorpresas geográficas son reales, pero dependen del punto de partida

Grecia (17,3 %), Argentina (16,9 %), Italia (15,2 %), España (13,4 %), Polonia
(13,3 %) con correlaciones de 0,44-0,53. Interesante… hasta que se mueve la fecha
de inicio dos años y medio atrás:

| | 2016-11 → 2026-08 | **2014-03 → 2026-08** |
|---|---:|---:|
| QQQ | 21,2 % | 19,3 % |
| ARGT | 16,9 % | 14,8 % |
| ITA | 13,7 % | 13,3 % |
| GDX | 18,4 % | 13,3 % |
| EWY | 15,6 % | 11,2 % |
| GLD | 14,2 % | 10,1 % |
| XME | 16,1 % | 10,1 % |
| EWP | 13,4 % | **6,9 %** |
| EPOL | 13,3 % | **6,1 %** |
| GREK | 17,3 % | **4,1 %** |
| EWZ | 6,2 % | **3,6 %** |

Grecia pasa de 17,3 % a 4,1 %; España de 13,4 % a 6,9 %. Noviembre de 2016 cae
justo después del suelo del ciclo de materias primas y emergentes de 2015-16.
**Son historias de recuperación desde un mínimo, no motores estructurales de
rentabilidad.** El oro y las mineras aguantan mucho mejor el cambio de ventana
(10,1 % y 13,3 %), y el Nasdaq apenas se mueve (19,3 %).

### 3.5 Casi todo el resultado de los diversificadores es el año 2025

CAGR de la ventana principal con y sin el año natural 2025:

| Ticker | Con 2025 | Sin 2025 | Diferencia |
|---|---:|---:|---:|
| SIL | 12,9 % | 0,9 % | −12,0 pp |
| GDX | 18,4 % | 7,4 % | −11,0 pp |
| EWY | 15,6 % | 6,1 % | −9,5 pp |
| COPX | 18,7 % | 10,3 % | −8,4 pp |
| URA | 18,1 % | 10,6 % | −7,6 pp |
| XME | 16,1 % | 8,5 % | −7,6 pp |
| GREK | 17,3 % | 10,7 % | −6,6 pp |
| EWP | 13,4 % | 7,1 % | −6,3 pp |
| GLD | 14,2 % | 8,3 % | −6,0 pp |
| **QQQ** | **21,2 %** | **21,3 %** | **−0,1 pp** |

En 2025 GDX hizo **+181 %**, SIL +201 %, COPX +127 %, GLD +84 %, Grecia +96 %,
España +88 %. El Nasdaq hizo +23 %. Quitando ese año, **ningún diversificador se
acerca al Nasdaq**, y el 80/20 con mineras deja de ser gratis:

| Cartera | 2014-03 → 2026-08 | 2014-03 → **2024-12** | 2021-09 → 2026-08 |
|---|---:|---:|---:|
| 100 % QQQ | 19,3 % (Sh 0,94) | **18,6 % (Sh 0,92)** | 16,0 % (Sh 0,66) |
| 85 / 15 oro | 18,2 % (Sh 1,03) | 17,1 % (Sh 0,96) | 17,1 % (Sh 0,82) |
| 75 / 25 oro | 17,5 % (Sh 1,07) | 16,0 % (Sh 0,98) | 17,7 % (Sh 0,94) |
| 80 / 20 mineras oro | 19,4 % (Sh 0,99) | **16,9 % (Sh 0,85)** | 19,9 % (Sh 0,90) |
| 70 / 20 oro / 10 mineras | 17,9 % (Sh 1,05) | 15,6 % (Sh 0,91) | 19,3 % (Sh 1,00) |

Lectura honesta: **el oro mejora el Sharpe en las cuatro ventanas** (siempre a
cambio de 1-2 puntos de rentabilidad); **las mineras de oro solo lo mejoran si se
incluye 2025**. Lo primero es una propiedad estructural; lo segundo, todavía, un
episodio.

---

## 4. Carteras

Mezclas con rebalanceo mensual, ventana nov-2016 → ago-2026.

| Cartera | CAGR | Vol | Sharpe | MaxDD |
|---|---:|---:|---:|---:|
| 100 % Nasdaq | 21,2 % | 19,3 % | 1,00 | −32,6 % |
| 85 / 15 oro | 20,5 % | 16,8 % | 1,10 | −29,1 % |
| 80 / 20 mineras de oro | 21,8 % | 18,4 % | 1,07 | −30,3 % |
| 75 / 25 oro | 20,0 % | 15,4 % | 1,17 | −26,9 % |
| 70 / 20 oro / 10 mineras | 20,5 % | 15,9 % | 1,16 | −26,9 % |
| 60 / 25 oro / 15 mineras | 20,2 % | 15,8 % | 1,15 | −25,3 % |
| 55 / 20 oro / 10 mineras / 15 Grecia | 20,2 % | 15,5 % | 1,18 | −24,6 % |
| 60 / 25 oro / 15 defensa | 19,1 % | 14,6 % | 1,17 | −23,6 % |
| 50 / 50 oro | 18,4 % | 13,0 % | 1,27 | −21,2 % |

La búsqueda del máximo Sharpe converge en ~45-50 % de oro (Sharpe 1,28). **Es
sobreajuste**: coincide con la mayor década del oro desde los setenta. La zona
defendible está en el 15-25 %, donde la mejora de Sharpe se mantiene en todas las
ventanas de control y el coste en rentabilidad es de 1-2 puntos.

---

## 5. Restricción práctica: la cuenta es europea

La cuenta tiene divisa base EUR y posiciones en AEB. Bajo PRIIPs, **un cliente
minorista del EEE no puede comprar ETFs domiciliados en EE. UU.** en IBKR: no
tienen KID. Encaja con la cartera actual, que tiene PSLV y SPCX (*closed-end
funds*, exentos) y ninguna participación en ETFs estadounidenses.

Es decir: **los tickers de este estudio son el vehículo de análisis, no el
vehículo de compra.** Los equivalentes UCITS verificados en el contrato de IBKR:

| Análisis | Equivalente UCITS | Ticker IBKR | Mercado |
|---|---|---|---|
| GLD — oro físico | iShares Physical Gold ETC | `SGLN` | LSEETF |
| GLD — oro físico | WisdomTree Core Physical Gold | `WGLD` | LSEETF / IBIS2 |
| GLD — oro físico | Amundi Physical Gold ETC | `GLDD` / `GLDA` | AEB / LSE |
| GDX — mineras de oro | VanEck Gold Miners UCITS | `GDX` / `GDX1` | LSEETF / SBF |
| GDXJ — mineras junior | VanEck Junior Gold Miners UCITS | `GDXJ` | LSEETF |
| SIL — mineras de plata | Global X Silver Miners UCITS | `SILV` / `SILG` | BVME.ETF / LSEETF |
| COPX — mineras de cobre | Global X Copper Miners UCITS | `COPX` | LSEETF |
| URA — uranio | Global X Uranium UCITS | `URNU` | BVME.ETF |
| ITA — defensa | VanEck Defense UCITS | `DFNG` | LSEETF |
| EWP — España | Amundi IBEX 35 UCITS | `LYXIB` / `CS1` | BM / SBF |
| EWP — España | BBVA Acción IBEX 35 | `BBVAI` | BM |

**Grecia y Argentina no tienen equivalente UCITS.** Son precisamente dos de las
sorpresas del cribado, y no hay forma limpia de comprarlas desde una cuenta
minorista europea. Las alternativas (acciones sueltas, el ETF griego cotizado en
ATHEX) cambian el perfil del análisis y no están cubiertas aquí.

Antes de operar conviene confirmar dos cosas en la cuenta: que el instrumento
concreto es comprable, y en qué divisa liquida (varios cotizan en USD y GBP
además de EUR).

---

## 6. Qué no funcionó

Del cribado inicial, descartado con motivo:

- **China** (KWEB −38 % a 10 años, MCHI +11 %): descorrelacionada, sí; rentable, no.
- **Brasil** (EWZ 6,2 %) y **Turquía** (TUR −2 % a 10 años): lo mismo.
- **Managed futures** (DBMF, KMLM): la descorrelación es excelente, pero DBMF renta
  ~7 % anual con dividendos y KMLM menos. Además no hay UCITS accesible.
- **Bonos largos** (TLT −41 % de precio a 10 años): el diversificador clásico ha
  sido un lastre en todo el periodo.
- **Anti-beta** (BTAL −43 % a 10 años): funciona como seguro, cuesta como seguro.
- **Fondos de primas alternativas** (QSPIX, AQMIX): interesantes en 2025-26, pero
  son fondos de inversión estadounidenses, inaccesibles desde una cuenta europea.
- **Infraestructuras, agua, agricultura, MLPs, REITs**: rentabilidades de 5-11 %
  con correlaciones de 0,5-0,7. Ni una cosa ni la otra.

---

## 7. Conclusión

1. **No existe "el Nasdaq pero descorrelacionado".** En diez años nada del
   universo lo ha batido, y lo que más se le acerca en rentabilidad (Taiwán,
   Corea) es Nasdaq encubierto.
2. **El oro es el diversificador estructural**, el único que mantiene correlación
   ~0 en todos los regímenes y el único que gana dinero en los peores meses del
   Nasdaq. Cuesta 1-2 puntos de rentabilidad y compra 6-11 puntos de caída
   máxima.
3. **Las mineras de oro son la mejor candidata a "rentabilidad sin
   correlación"**, con un asterisco grande: sin 2025 su CAGR cae del 18,4 % al
   7,4 %.
4. **Grecia, España, Italia y Polonia son reales pero frágiles**: el resultado
   depende casi por completo de empezar a medir en el suelo de 2016.
5. **El cuello de botella no es encontrar los activos, es poder comprarlos.**
   Oro, mineras de oro, plata, cobre, uranio y defensa tienen UCITS accesibles;
   Grecia y Argentina, no.

---

*Estudio cuantitativo con fines de análisis. No es una recomendación de
inversión. Rentabilidades pasadas no garantizan resultados futuros, y este
estudio muestra precisamente cuánto cambian las conclusiones al mover la ventana
de medición.*

**Fuentes:** precios mensuales — Interactive Brokers (`get_price_history`, barras
mensuales, ajustadas por splits). Retorno total y cribado — Financial Modeling
Prep. Instrumentos y contratos — Interactive Brokers (`search_contracts`).
Datos a 3 de septiembre de 2026.
