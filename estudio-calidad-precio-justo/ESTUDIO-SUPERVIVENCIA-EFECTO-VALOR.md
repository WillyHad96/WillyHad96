# El sesgo infla el NIVEL en ~5 pp, pero no crea el efecto valor

Estudio 1 de los tres aprobados. Responde: ¿cuánto del hallazgo de C23/C24 es supervivencia?
Sin necesidad de FMP, porque `multiplo_ps` existe también para el cubo `'desconocido'`.

## 1. El tamaño real del agujero

En el **universo elegible** (banda 300M–5.000M$, guardas de `consultas.sql`, 2007–2023):

| grupo | tickers | bajas | % que muere |
|---|---|---|---|
| con sector | 1.254 | **3** | **0,2%** |
| **`'desconocido'`** | 1.008 | **596** | **59,1%** |

**596 tickers que habrían sido elegibles están ausentes de todo análisis sectorial.** Son el
**32% del universo elegible verdadero** (596 de 1.850), y casi todos son muertos.

Esto es peor que A7 a nivel de panel completo (33,7%): **dentro del universo que la estrategia
realmente mira, el cubo sin sector muere el 59% de las veces.**

## 2. El test

Cuartiles de P/S calculados **dentro de cada universo** para que la comparación sea justa.
Retorno medio anual por evento:

| universo | Q1 baratas | Q2 | Q3 | Q4 caras | **spread Q1−Q4** |
|---|---|---|---|---|---|
| **A) solo con sector** (lo usado hasta hoy) | **20,05%** | 12,30% | 11,21% | 12,22% | **+7,83 pp** |
| **B) todo el elegible** (con muertos) | **15,35%** | 9,23% | 7,15% | 7,00% | **+8,35 pp** |
| C) elegible sin las bajas | 17,68% | 10,28% | 8,37% | 8,62% | +9,06 pp |

## 3. Las dos lecturas, que van en direcciones opuestas

**Mala: el nivel está inflado ~5 pp.** Meter los muertos baja Q1 de 20,05% a 15,35%
(**−4,70 pp**) y Q4 de 12,22% a 7,00% (**−5,22 pp**). Todos los números absolutos de esta
serie medidos sobre el universo sectorizado llevan esa inflación encima.

**Buena: el efecto valor NO es un artefacto de supervivencia.** El spread Q1−Q4 **no se
encoge: crece ligeramente**, de +7,83 a +8,35 pp. Los muertos castigan a baratas y a caras
casi por igual, así que **la señal relativa sobrevive intacta.**

Es exactamente la distinción de B4, ahora medida en vez de asumida: **la comparación interna
es robusta al sesgo; la comparación contra un índice no lo es.**

## 4. Qué significa para C23/C24

El CAGR de **15,40%** de Industrials baratas está medido sobre el universo A. Aplicando la
corrección de nivel del universo (−4,7 pp sobre Q1), la estimación honesta cae a
**~10–11%, frente al 13,26% del Nasdaq.**

*Es una extrapolación*: la corrección está medida sobre todo el universo elegible, no sobre
Industrials en concreto, porque los 596 muertos no tienen sector asignado. Pero la dirección
y el orden de magnitud son firmes.

**Conclusión: C24 queda reforzado, no debilitado.** Ya decía que Industrials baratas no bate
al Nasdaq (t = 0,48, Sharpe 0,423 vs 0,512). Este estudio añade que **su CAGR además estaba
inflado ~5 pp**. La distancia real al índice es mayor de lo que parecía.

**Y C23 queda reforzado también**, en lo suyo: el alfa interno de +6,73 pp no se apoya en el
sesgo, porque el spread aguanta al meter los muertos.

## 5. Lo que sigue faltando

Asignar sector a los 596 muertos (FMP `profile-symbol`, una llamada por ticker) para medir la
corrección **dentro de Industrials** en vez de extrapolarla. Es el único modo de convertir el
"~10–11%" en un número medido.

Prioridad media: la conclusión cualitativa —el nivel está inflado, la señal relativa no— ya
no va a cambiar. Lo que cambiaría es la cifra exacta.
