# Liquidez, calendario, consistencia y banda de capitalización

Las cuatro pruebas pendientes de `METODOLOGIA-Y-PENDIENTES.md`, más dos hallazgos
colaterales. **Dos de las cuatro hipótesis quedan refutadas, y una de ellas era mía.**

---

## 1. Liquidez — ¿cuánto dinero cabe?

### 1.1 El dato

Volumen medio diario en dólares (mediana de las sesiones de agosto de 2026, obtenido de FMP;
el panel no tiene volumen). Agosto es un mes flojo, así que la estimación peca de conservadora.

| | ADV $ / día |
|---|---|
| Mediana de la cartera | **26,2 M$** |
| Nombre más líquido (VSH) | 120,6 M$ |
| Nombre más ilíquido (**CPAC**) | **0,53 M$** |
| Segundo más ilíquido (MOV) | 5,4 M$ |

**Sólo hay un problema, y es un nombre concreto.** CPAC es Cementos Pacasmayo, una cementera
peruana que cotiza en Nueva York como ADR y negocia de verdad en Lima. Un día de agosto cruzó
8.829 acciones — unos 103.000 $ en toda la sesión. El resto de la cartera está entre 5 y 120
millones diarios.

Es además un fallo de filtro: el "tickers limpios" que descarta warrants y unidades **no
descarta ADRs extranjeros**. CPAC entró por la puerta de atrás.

### 1.2 Capacidad

Suponiendo que quieres montar o deshacer la posición en **un solo día**:

| Configuración | A 5% del volumen diario | A 10% |
|---|---|---|
| Cartera tal cual (43 nombres) | 1,1 M$ | 2,3 M$ |
| **Quitando sólo CPAC (42 nombres)** | **11,4 M$** | **22,7 M$** |

Un único nombre divide la capacidad por diez. Con un filtro de ADV ≥ 2 M$ la estrategia
soporta **más de 11 millones de dólares**.

### 1.3 Tu pregunta: ¿valen 10.000 €?

Sí, y por un margen enorme. Con 10.000 € repartidos entre 43 nombres:

| Presupuesto | Por posición | Acciones (mediana) | % del volumen del peor nombre |
|---|---|---|---|
| 5.000 € | 126 $ | 3 | 0,02% |
| **10.000 €** | **251 $** | **6** | **0,05%** |
| 20.000 € | 502 $ | 13 | 0,10% |
| 100.000 € | 2.512 $ | 64 | 0,48% |
| 250.000 € | 6.279 $ | 160 | 1,19% |

Estás **tres órdenes de magnitud** por debajo de mover el precio. La liquidez no es tu
restricción y no lo será hasta pasado el millón de euros.

### 1.4 Lo que SÍ es tu restricción: la comisión mínima

El problema a tu escala no es el volumen, es que **cada operación tiene un coste mínimo fijo**
(≈1 $ en IBKR) y vas a hacer 86 operaciones al año (43 compras + 43 ventas).

| Presupuesto | 43 nombres | 21 nombres (cap ≥ 1.000 M$) | 116 nombres (4 tramos) |
|---|---|---|---|
| 5.000 € | 1,59% | 0,78% | 2,00% |
| **10.000 €** | **0,80%** | 0,39% | 2,00% |
| 20.000 € | 0,40% | 0,20% | 1,07% |
| 50.000 € | 0,17% | 0,10% | 0,43% |
| 100.000 € | 0,10% | 0,07% | 0,22% |

Con la ventaja de referencia (≈9,8 pp anuales, ver §5), y poniendo el listón en que las
comisiones no se lleven más del 10% de esa ventaja:

- **43 nombres → mínimo razonable ≈ 8.500 €**
- **21 nombres → mínimo razonable ≈ 4.000 €**
- **4 tramos (116 nombres) → mínimo razonable ≈ 22.000 €**

Con 10.000 € la versión de 43 nombres es viable pero justa. **Con 10.000 € es mejor la versión
de 21 nombres** (§4.3): menos comisión, más liquidez por nombre, y la ventaja apenas cambia.

Esto no incluye la horquilla de compraventa, que no puedo medir sin datos de cotización en
tiempo real. En nombres de 5–120 M$ diarios suele ser pequeña; en CPAC sería considerable, una
razón más para excluirlo.

---

## 2. El calendario — la prueba que faltaba

Recordatorio: el diseño elegía la primera presentación del año de cada empresa, lo que forzaba
febrero sin que nadie lo decidiera. Ahora se prueban los cuatro trimestres usando la 2ª, 3ª y
4ª presentación del año.

**Ventana común 2007–2024 (18 años), equiponderado:**

| Entrada | CAGR | SPY | Alfa | Volatilidad | Peor año | Gana |
|---|---|---|---|---|---|---|
| **Febrero** | 19,17% | 8,63% | **10,54** | 24,3% | −36,1% | 15/18 |
| Mayo | 15,26% | 8,32% | 6,94 | 24,3% | −35,7% | 14/18 |
| Agosto | 17,51% | 9,42% | 8,09 | 21,0% | −26,2% | 15/18 |
| Noviembre | 15,03% | 9,22% | 5,81 | 21,1% | −38,8% | 14/18 |
| **4 TRAMOS** | 17,28% | 9,34% | 7,94 | **20,4%** | **−21,7%** | **17/18** |

### Lo que dice

**La estrategia funciona en los cuatro meses.** Ese era el riesgo real y no se ha materializado:
la ventaja no depende de febrero. Va de 5,81 a 10,54 pp, siempre positiva.

**Pero febrero es el mejor de los cuatro, y lo elegimos por accidente.** Eso es un sesgo de
selección de manual: si coges el mejor de cuatro sin haberlo decidido, el número que ves está
inflado. **La expectativa honesta hacia delante es la media de los cuatro, ≈7,8 pp, no 10,5.**

Todos los números de alfa de estudios anteriores están medidos en febrero. Hay que leerlos con
ese descuento.

### Los cuatro tramos son mejores en riesgo

Repartir el capital en cuatro sobres trimestrales da algo menos de rentabilidad (17,28% frente
a 19,17%) pero:

- **Volatilidad 20,4% frente a 24,3%**
- **Peor año −21,7% frente a −36,1%** — 14 puntos menos de agujero
- **Gana al SPY 17 años de 18** en vez de 15

Es lo que cabía esperar: diversificar el momento de entrada elimina la lotería de la fecha. El
peaje es que multiplica por cuatro las operaciones, y a 10.000 € eso cuesta un 2% anual en
comisiones — más de lo que aporta. **Los tramos son la configuración correcta a partir de
~50.000 €; por debajo, no compensan.**

---

## 3. Frog-in-the-pan (consistencia del momentum) — REFUTADO

Era la que yo puse como prioridad *muy alta* y la única que podía **aumentar** la ventaja.
No aumenta nada.

### Por qué parecía que funcionaba

Midiendo la consistencia como "cuántos de los 4 trimestres previos subieron", a nivel de evento
el gradiente era precioso:

| Trimestres al alza | n | Exceso medio sobre SPY |
|---|---|---|
| 2 | 104 | +8,67% |
| 3 | 273 | +11,78% |
| 4 | 159 | +14,24% |

### Por qué es un espejismo

En la misma tabla, el momentum medio era 53,2% / 80,8% / 94,7%. **Subir los cuatro trimestres
correlaciona con haber subido mucho.** No estaba midiendo consistencia, estaba midiendo
momentum otra vez, disfrazado.

Controlando por cuartil de momentum, el patrón se rompe: el consistente gana en 3 de los 4
cuartiles y pierde claramente en el segundo (−2,43% frente a +0,49%). Y las medianas del
gradiente original no acompañan a las medias (16,2 / 12,1 / 17,6 / 13,1), señal de que todo
venía de las colas.

### La prueba que decide

Aplicar el filtro a la cartera real, después de seleccionar el top 20% por momentum:

| | CAGR | SPY | Alfa |
|---|---|---|---|
| Base (29 nombres) | 20,11% | 8,81% | 11,30 |
| Con consistencia ≥3 (23 nombres) | 20,43% | 8,63% | 11,81 |

**Diferencia año a año: media +0,36 pp, mediana +0,00 pp, gana en 8 de 17 años.** Una moneda al
aire. Filtrar por consistencia cuesta 6 nombres de diversificación y no compra nada.

---

## 4. La banda de capitalización — REFUTADO, y mi premisa era falsa

Yo escribí: *"300 M$ de 2008 no son 300 M$ de 2024: el umbral absoluto se desplaza y la
estrategia está cambiando de universo sola."* Lo medí. **Es falso en la forma en que lo dije.**

### 4.1 La banda no se ha movido

Porcentaje del panel que cae dentro de 300 M$ – 5.000 M$:

| Año | Debajo de 300M | **En la banda** | Encima de 5B | Mediana del panel |
|---|---|---|---|---|
| 2003 | 13,4% | **58,7%** | 27,8% | 1.700 M$ |
| 2010 | 17,6% | **55,9%** | 26,5% | 1.454 M$ |
| 2017 | 8,4% | **55,1%** | 36,6% | 2.661 M$ |
| 2026 | 0,6% | **52,7%** | 46,8% | 4.442 M$ |

La banda ha capturado entre el 52% y el 60% del panel durante veintitrés años. Notablemente
estable.

### 4.2 Lo que sí ha cambiado

- **El suelo de 300 M$ está muerto.** Excluía al 13,4% del panel en 2003 y hoy excluye al 0,6%.
  Ya no filtra nada.
- **El techo de 5.000 M$ es el que aprieta.** Excluía a un cuarto del panel y hoy excluye a casi
  la mitad.
- La mediana del panel pasó de 1.700 a 4.442 M$ — un 2,6× en 23 años, ≈4,3% anual.

### 4.3 Y la corrección por percentiles empeora las cosas

Sustituyendo la banda absoluta por una banda de percentiles fija (p13–p72, los percentiles que
ocupaban 300 M$ y 5.000 M$ en 2003):

| Variante | CAGR | SPY | Alfa | Alfa 2016–2025 |
|---|---|---|---|---|
| **Banda absoluta 300M–5B** | 19,74% | 9,10% | **10,64** | **12,96** |
| Banda por percentiles p13–p72 | 16,73% | 9,14% | 7,59 | 8,24 |
| Suelo subido a 1.000 M$ | 18,43% | 8,76% | 9,68 | 10,54 |

**La banda por percentiles pierde 3 puntos de alfa**, y más aún en la última década.

El motivo tiene sentido y es informativo: un techo por percentiles **sube contigo** según se
infla el mercado, y te arrastra hacia empresas grandes. Ya sabíamos por el estudio de tamaños
que el momentum se desvanece en large caps. **El techo en dólares te ancla en la zona donde el
efecto existe.** Era una virtud, no un defecto.

### 4.4 Lo aprovechable

Subir el **suelo** a 1.000 M$ cuesta 0,96 pp de alfa — dentro de la banda de ruido — y a cambio
da 21 nombres en vez de 29, todos más líquidos y más baratos de operar. **A presupuestos
pequeños es un buen cambio.** El techo, en cambio, no se toca.

---

## 5. Colateral: los dividendos, resueltos

Estaba en la lista como prioridad alta. Comprobado y cerrado.

**`precio_post` NO incluye dividendos.** Verificado al céntimo: DLX el 2019-01-24 vale 44,31 en
el panel; el cierre bruto de FMP ese día es 44,31; el cierre ajustado por dividendos es 30,47.

**Pero el SPY del panel también es sólo precio**, así que la comparación es limpia:

| | CAGR |
|---|---|
| SPY reconstruido del panel (2007–2025) | 9,10% |
| SPY real, sólo precio (feb-2007 → feb-2026) | 8,62% |
| SPY real, retorno total | ≈10,7% |

Nuestro 9,10% se pega al 8,62%, no al 10,7%. Es precio contra precio.

**El ajuste que queda:** en retorno total el S&P 500 gana más que nuestra cartera, porque su
dividendo histórico (≈1,9%) es mayor que el de nuestras pequeñas (≈1,0–1,3%). El alfa medido
debe descontarse en **≈0,8 pp**.

Corrigiendo por eso *y* por el sesgo de selección de febrero (§2), la ventaja defendible es
**≈7,0 pp anuales sobre el S&P 500**, no los 10,6 pp brutos. Sigue siendo mucho, y sigue sin
corregir el sesgo de supervivencia, que es el que falta y el que más puede doler.

---

## 6. Resumen

| Prueba | Veredicto |
|---|---|
| ¿Cabe dinero? | **Sí.** Hasta ~11 M$ quitando CPAC. 10.000 € no roza el límite |
| ¿Cuál es el límite real a 10.000 €? | **La comisión mínima**, 0,80% anual. Mínimo sensible ≈8.500 € |
| ¿Depende de febrero? | **No.** Funciona los 4 meses (5,8 a 10,5 pp) |
| ¿Febrero está inflado? | **Sí.** Es el mejor de 4 y salió por accidente. Descontar a ≈7,8 pp |
| ¿Mejoran los 4 tramos? | **En riesgo sí** (peor año −21,7% vs −36,1%). En coste no, por debajo de 50.000 € |
| ¿Consistencia del momentum? | **No aporta nada.** El gradiente era momentum disfrazado |
| ¿Banda por percentiles? | **Empeora 3 pp.** El techo en dólares era una virtud |
| ¿Dividendos? | **Resuelto.** Comparación limpia; descontar 0,8 pp para retorno total |

### Cambios que recomiendo

1. **Excluir CPAC y añadir un filtro de ADV ≥ 2 M$.** Multiplica por diez la capacidad y tapa
   el agujero de los ADR extranjeros.
2. **A 10.000 €, subir el suelo a 1.000 M$** y operar 21 nombres en vez de 43. Misma ventaja
   dentro del ruido, la mitad de comisión.
3. **Dejar el techo de 5.000 M$ como está.** Está haciendo trabajo real.
4. **Reetiquetar la ventaja esperada como ≈7 pp**, no 10,6.
5. **Guardar los 4 tramos para cuando la cartera pase de ~50.000 €.**

### Lo que sigue pendiente

- **Sesgo de supervivencia** (delistings) — el grande, y necesita el plan de FMP
- Europa como validación fuera de muestra
- La horquilla de compraventa, que no he podido medir
- Momentum relativo al sector, y estabilidad medida contra tendencia en vez de contra la media
