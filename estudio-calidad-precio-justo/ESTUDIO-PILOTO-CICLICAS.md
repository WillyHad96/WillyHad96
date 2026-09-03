# Piloto del panel de cíclicas: no rechaza, pero no tenía potencia para probar

Ejecuta el plan de `DISEÑO-PANEL-CICLICAS.md` §6. Scripts: `construye_ciclo.py`,
`auc_ciclo.py`, `poder_piloto.py`. Datos: `fmp_raw/` (50 tickers), `ciclicas_ciclo.csv`.

## Resumen en una frase

**Ninguna variable pasa el umbral pre-declarado, pero el umbral era inalcanzable con 50
tickers: el SE del AUC es 0,097 y yo pedí un efecto de 0,10 replicado en dos mitades. El
piloto no rechaza la hipótesis — no tenía potencia para probarla.**

---

## 1. Lo que se construyó

- **50 tickers cíclicos**, muestra aleatoria (semilla 13) de los 225 con ≥8 años de panel.
- **key-metrics trimestral de FMP**, 60–80 trimestres por ticker (mediana 80), desde 2007.
- **3.400 filas trimestrales** con 21 variables cíclicas derivadas.
- **531 decisiones de febrero** unidas al panel, 2010–2023, cobertura ~100%.

**Desfase anti-look-ahead:** solo se usa el último trimestre cerrado antes del **15 de
noviembre del año anterior**. Es conservador (Q3 del año previo, reportado con seguridad
antes del febrero de la decisión) y descarta cualquier uso de información no publicada.

Variables construidas, todas nuevas respecto al panel: posición dentro del rango propio de
20 trimestres para ROCE, capex/depreciación, días de inventario, EV/ventas y FCF yield;
**EV / EBITDA de mitad de ciclo** y **deuda neta / EBITDA de mitad de ciclo** (EBITDA
promediado sobre 20T); medias de 8T; y primeras derivadas a 4T como confirmación del giro.

## 2. El resultado

Ninguna variable alcanza |AUC − 0,5| ≥ 0,10 replicado. **La interacción de §5 del diseño
—suelo de ciclo + valoración de suelo + balance sano— falla del todo: 0,472 / 0,500 en
quintil, 0,494 / 0,536 en decil.**

Lo único que replica con signo y algo de tamaño, contra el **decil** superior:

| variable | AUC pares | AUC impares | dirección |
|---|---|---|---|
| **posición de EV/ventas en su historia** | 0,442 | 0,416 | **barato vs sí misma** predice la cola |
| **Δ capex/depreciación a 4T** | 0,437 | 0,414 | **capex cayendo** predice la cola |

Ambas apuntan donde dice la teoría, y la primera coincide con lo que ya daba el panel por su
cuenta (P/S nivel 0,449 / 0,463). **Son tres medidas independientes diciendo lo mismo:
barato respecto a su propia historia predice la cola.** La segunda es nueva y es
exactamente la tesis de disciplina de capacidad.

Trampa evitada: `deuda neta / EBITDA de mitad de ciclo` da **0,684** en años pares y **0,517**
en impares. Sin el corte pares/impares habría entrado como hallazgo.

## 3. Por qué el resultado no significa lo que parece

`poder_piloto.py`:

| nivel | n en la cola | SE(AUC) por mitad | IC95% |
|---|---|---|---|
| quintil | 106 | 0,069 | ±0,135 |
| **decil** | **53** | **0,097** | **±0,190** |

El umbral pedía |AUC − 0,5| ≥ 0,10 **replicado en ambas mitades**. Con SE 0,097, un efecto
real de exactamente 0,10 supera el listón en una mitad ~50% de las veces, y en las dos
~25%. **El test no podía pasar aunque la señal fuera real. Error de calibración mío: fijé
el umbral en el diseño sin calcular antes la potencia del piloto.**

Y al revés: el IC95% de 0,416 es aproximadamente [0,23, 0,61]. Contiene 0,5. **Nada de lo
que sale aquí, ni a favor ni en contra, es concluyente.**

## 4. Qué tamaño resuelve la pregunta

| tickers | decisiones | n cola (decil) | SE(AUC)/mitad | IC95% |
|---|---|---|---|---|
| 50 (piloto) | 531 | 53 | 0,097 | ±0,190 |
| 150 | 1.593 | 159 | 0,056 | ±0,110 |
| 300 | 3.186 | 318 | 0,040 | ±0,078 |
| **468** (universo con ≥8 años) | **4.970** | **497** | **0,032** | **±0,062** |

Con el universo completo el SE baja a 0,032: **ahí sí se distingue 0,60 de 0,50, y también
0,44 de 0,50.** La pregunta es resoluble; el piloto no la resolvía.

## 5. Lo que sí queda validado — la tubería

- **Los trimestrales de FMP llegan a 2006–2007** y cubren la ventana entera.
- **La construcción de variables de ciclo funciona** con cobertura ~100%.
- **El desfase anti-look-ahead está implementado** y es conservador.
- **El coste de contexto por ticker es ~0**: las respuestas grandes se guardan a disco.
  Los 468 tickers son viables desde esta sesión, a ~12 llamadas por ronda.

## 6. Decisión

El criterio de §6 del diseño decía "solo si pasa, construir la tabla completa". **No pasa,
pero el criterio estaba mal puesto**, así que aplicarlo literalmente sería tomar una decisión
con un test que yo mismo diseñé sin potencia.

Recomendación: **seguir con la descarga completa**, por tres razones y no por una:

1. El piloto **no rechaza**: sus intervalos contienen tanto 0,5 como 0,60.
2. Las dos supervivientes son **coherentes con la teoría y con lo que ya daba el panel** por
   una vía independiente.
3. El coste real es **tiempo de descarga, no dinero ni contexto**, y el resultado con 468
   tickers **sí sería concluyente en ambas direcciones**.

Umbral revisado, declarado ahora y calculado esta vez: con 468 tickers, **AUC ≥ 0,56 o
≤ 0,44 replicado en ambas mitades** es un efecto de ~2 SE por mitad. Ése es el listón.

## 7. Lo que sigue sin resolver, y no lo resuelve FMP

El bloque de supervivencia (deuda neta / EBITDA de mitad de ciclo) es el que menos se puede
validar aquí: **las cíclicas apalancadas que quebraron no están en el panel** (A1). Es
precisamente la variable que la teoría dice que separa el +200% del −100%, y es la que estos
datos no pueden medir.
