# Delistings: el sesgo de supervivencia, medido — y era mío

**Este documento revisa a la baja el resultado principal de todo el estudio.** La ventaja
publicada de +10,09 pp anuales sobre el S&P 500 baja a **+4,41 pp**, y a **≈2,5 pp** tras aplicar
también los descuentos ya establecidos por el sesgo de febrero y por dividendos.

---

## 1. El panel no era el problema. Mi filtro sí

Llevo todo el estudio diciendo que el panel sólo contiene tickers vivos hoy. **Es falso.** El
panel contiene 1.319 empresas que dejaron de reportar:

| Último dato disponible | Empresas | % |
|---|---|---|
| Viva (2026 Q2 o posterior) | 4.498 | 67,5% |
| 2026 Q1 | 772 | 11,6% |
| 2025 | 489 | 7,3% |
| 2024 | 287 | 4,3% |
| 2020–2023 | 459 | 6,9% |
| 2015–2019 | 135 | 2,0% |
| Antes de 2015 | 25 | 0,4% |

Y sin embargo, de las **6.705** observaciones del universo elegible entre 2007 y 2023, **cero**
pertenecían a empresas que después desaparecieran. Ni una. Eso es imposible en datos reales, así
que el filtro estaba en mi lado.

### El mecanismo

| | Filas sin `sector` |
|---|---|
| Empresas que siguen vivas | 59,7% |
| **Empresas que desaparecen** | **99,7%** |

El campo `sector` se rellenó en una pasada de enriquecimiento posterior que **sólo cubrió a las
cotizadas vivas en ese momento**. Mi universo exigía desde el preregistro:

```sql
and sector is not null and sector <> 'desconocido'
and sector not in ('Financial Services','Real Estate')
```

Esa primera línea **borraba el 99,7% de las empresas desaparecidas**. Y es *look-ahead* puro: en
2010 nadie podía saber a qué empresas les asignaría FMP una etiqueta de sector en 2026.

---

## 2. Quitando el filtro: la mortalidad aparece

Sin el filtro de sector, entre 2007 y 2023 la estrategia selecciona **971 eventos** en vez de 467.

| | |
|---|---|
| Seleccionadas | 971 |
| De empresas que acabaron desapareciendo | 229 |
| **Que desaparecen dentro del año de tenencia** | **21** |
| **Mortalidad anual** | **2,16%** |
| Retorno medio a 12m de las supervivientes | +14,79% |
| Retorno de las que mueren (hasta su último precio) | **+8,64%** |

Un 2,16% anual encaja con lo que se observa en la realidad. Y las que mueren **no se desploman**:
hacen +8,64%. Lo que confirma que la mayoría de las desapariciones son **compras, no quiebras**.

---

## 3. Los cinco escenarios

Todos con entrada en febrero, 2007–2023, equiponderado, sólo precio.

| Escenario | CAGR | SPY | **Alfa** | Vol | Gana |
|---|---|---|---|---|---|
| **A. Con filtro de sector (lo publicado)** | 18,14% | 8,04% | **+10,09** | 25,6% | 14/17 |
| **B. Sin filtro, sólo supervivientes** | 14,46% | 7,96% | **+6,50** | 24,4% | 12/17 |
| **C. Sin filtro, con los muertos a su precio final** | 11,90% | 7,50% | **+4,41** | 21,1% | 11/17 |
| D. Sin filtro, muertos con un −30% adicional | 11,35% | 7,50% | +3,86 | 21,1% | 11/17 |
| E. Sin filtro, muertos a cero | 10,05% | 7,50% | +2,56 | 21,2% | 9/17 |

### Descomposición

- **A → B = −3,59 pp.** Esto **no** es supervivencia: es el filtro de sector actuando como criterio
  de calidad retroactivo. Es la parte más grande, y es enteramente mi error.
- **B → C = −2,09 pp.** Ésta sí es la corrección de supervivencia pura: mismo universo, misma
  definición, sólo añadiendo de vuelta a los muertos.
- **C → E = −1,85 pp** más si se asume que toda desaparición vale cero, que es demasiado
  pesimista dado que la mayoría son adquisiciones.

**El escenario C es el defendible: +4,41 pp.**

---

## 4. ¿Qué hay en el grupo "sin sector"? Lo miré

No iba a recortar seis puntos sin ver la muestra. Ejemplos de seleccionadas sin etiqueta de
sector:

| Ticker | Empresa | Qué le pasó |
|---|---|---|
| HSKA | Heska | Comprada por Mars (2023) |
| CIR | CIRCOR International | Comprada por KKR (2023) |
| SPNC | Spectranetics | Comprada por Philips (2017) |
| OVTI | OmniVision | Comprada (2015) |
| ABCO | Advisory Board Company | Comprada (2017) |
| HTA | Healthcare Trust of America | Fusionada con Healthpeak (2022) |
| IRBTQ | iRobot | Concurso de acreedores |
| MED, DBI, STKL, CRMT | Medifast, Designer Brands, SunOpta, Car-Mart | Siguen cotizando |

**No es basura. Son compañías medianas estadounidenses perfectamente reales**, y la mayoría de
las que desaparecieron lo hicieron por adquisición.

### Y sin embargo rinden mucho peor

| Grupo | CAGR | Alfa | n medio |
|---|---|---|---|
| A1. Sector conocido, sin Fin/RE (publicado) | 18,14% | +10,09 | 33 |
| A2. Sector conocido, con Fin/RE | 17,46% | +9,44 | 36 |
| **A3. Sector desconocido, supervivientes** | **−2,39%** | **−9,82** | 8 |
| **A4. Sector desconocido, desaparecidas** | **+2,24%** | **−3,54** | 12 |

*(De paso: excluir Financials e inmobiliarias sólo aporta +0,65 pp. Confirma que aquel filtro
estaba dentro del ruido, como ya sospechábamos.)*

### Comprobé si eran splits mal ajustados. Casi no

Hipótesis: si el enriquecimiento también reajustó precios, las no etiquetadas tendrían caídas
falsas del −50% o −33% por splits.

| | Sin sector | Con sector |
|---|---|---|
| Mediana del retorno a 12m | **−0,52%** | +6,47% |
| Caídas cerca de −50% | 2,43% | 1,72% |
| Caídas cerca de −33% | 4,20% | 3,42% |
| Caídas severas (< −45%) | **11,34%** | 6,77% |

Hay exceso de caídas con forma de split, pero explica **menos de 1 punto de los 10** de
diferencia. El resto es real: ese grupo lo hizo genuinamente peor, con casi el doble de caídas
severas. **Mi hipótesis era casi toda falsa y la corrección se mantiene.**

---

## 5. El número revisado

Acumulando todas las correcciones establecidas en el estudio:

| Corrección | Efecto | Alfa resultante |
|---|---|---|
| Publicado | — | **+10,09 pp** |
| Quitar el filtro de sector (look-ahead) | −3,59 | +6,50 |
| Añadir las empresas desaparecidas | −2,09 | **+4,41** |
| Sesgo de selección de febrero (×0,74) | −1,13 | +3,28 |
| Dividendos (el S&P reparte más) | −0,80 | **≈ +2,5 pp** |
| Comisiones a 20.000 € | −0,40 | **≈ +2,1 pp neto** |

**De +10 pp a ~2 pp.** Sigue siendo positivo, y sigue habiendo una estrategia. Pero es una
estrategia que bate al índice por dos puntos, no por diez.

### Lo que sobrevive intacto

- La **dirección** de todos los hallazgos: momentum funciona, la estabilidad ayuda, ponderar por
  capitalización es peor que equiponderar, inclinar hacia momentum aporta, el horizonte da igual.
- La **comparación relativa** entre variantes, porque todas comparten el mismo sesgo.
- La descomposición 59/41: el universo pesa más que la selección.

### Lo que hay que rehacer

Todas las cifras absolutas de `RESULTADOS.md`, `ESTUDIO-SECTORES-Y-POSICION.md`,
`ESTUDIO-LIQUIDEZ-Y-CALENDARIO.md`, `ESTUDIO-HORIZONTES-AÑO-2.md` y `ESTUDIO-PONDERACIONES.md`
están calculadas con el filtro de sector puesto. **Los alfas están inflados en ~5,7 pp.** Las
comparaciones internas siguen valiendo.

---

## 6. Europa: bloqueado, y comprobado

Con el plan Premium recién contratado, para símbolos **no estadounidenses**:

| Endpoint | Estado |
|---|---|
| `profile-symbol` (ITX.MC, ROVI.MC) | ✅ funciona |
| `search-company-screener` por `country` | ✅ funciona |
| `search-company-screener` por `exchange` | ❌ requiere plan superior |
| `income-statement` **anual** (ROVI.MC) | ❌ requiere plan superior |
| `income-statement` **trimestral** (ROVI.MC) | ❌ requiere plan superior |
| `historical-price-eod` (ROVI.MC) | ❌ requiere plan superior |

Sin estados financieros ni precios para valores europeos **no hay forma de construir el panel**.
Toda la metodología descansa en fechas de presentación trimestrales, crecimiento trimestral y
margen bruto trimestral.

Además, el screener por país devuelve las **fichas OTC estadounidenses** de las empresas europeas
(CDNIF por Logista, AIXXF por Aixtron), no las cotizaciones primarias en Madrid o Fráncfort. Sin
el filtro por bolsa no se puede corregir.

**Europa necesita el siguiente escalón de FMP.** No es cuestión de esfuerzo: los datos no están
disponibles con este plan.

---

## 7. Qué haría ahora

1. **Rehacer los cinco documentos sin el filtro de sector.** Es mecánico y hay que hacerlo antes
   de tomar cualquier decisión con estos números.
2. **Recuperar el sector de las desaparecidas vía FMP** (`profile-symbol` sí funciona para
   tickers estadounidenses delistados). Son ~150 tickers únicos entre las seleccionadas. Eso
   permitiría aplicar la exclusión de Financials/inmobiliarias también a los muertos y quedarse
   con un escenario C limpio del todo.
3. **Reconstruir el retorno terminal real de las 21 que mueren dentro del año** con precios de
   FMP hasta el día del delisting, en vez del último precio del panel. Ahí es donde está el
   supuesto más frágil del escenario C.
4. Revisar si hay más campos con el mismo problema de enriquecimiento retroactivo que `sector`.
