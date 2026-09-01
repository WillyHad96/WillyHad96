# Regla cerrada, escrita antes de mirar la confirmación

Fecha: cierre de la fase de descubrimiento. Commit anterior: km.csv completo (264 eventos).

## Lo que se vio en descubrimiento (119 eventos, años pares)

Nada alcanzó significación. Los números, para que quede constancia:

| contraste | ALTO-BAJO | p permutación |
|---|---|---|
| ROIC por tercil    | +1.98 pp  | 0.832 |
| ROIC por mediana   | +7.73 pp  | 0.263 |
| FCFY por tercil    | -10.51 pp | 0.240 |
| FCFY por mediana   | -2.30 pp  | 0.745 |

ROIC por terciles sale en U (T1 +7.87, T2 +1.69, T3 +9.85): el tercil bajo lo hace casi
tan bien como el alto. Por eso la mediana da más diferencia que el tercil, y no porque el
efecto sea más fuerte.

## Regla que se aplica a confirmación, una sola vez

Elegida solo con lo de arriba, sin haber mirado ningún año impar:

1. **ROIC**: partición por la **mediana** de `returnOnInvestedCapital`.
   Signo esperado: mitad alta **por encima** de la baja (+).
2. **FCFY**: partición por **terciles** de `freeCashFlowYield`, T3 contra T1.
   Signo esperado: tercil alto **por debajo** del bajo (−).

Se reportan las dos, cada una con su contraste. No se elige ganadora a posteriori.
Test: permutación de dos colas, 20.000 iteraciones, semilla fija.

## Criterio de hallazgo (del preregistro, sin cambios)

1. Mismo signo en confirmación que en descubrimiento.
2. p de permutación < 0.05 en confirmación.
3. Sobrevive al control por sector y al control por año.

Las tres o no hay hallazgo.

## Advertencia sobre FCFY

El signo negativo de FCFY en descubrimiento (rinde más el de FCF yield bajo) es
sospechoso de ser un artefacto de valoración, no de calidad: `freeCashFlowYield` lleva la
capitalización en el denominador, así que ordenar por él es en parte ordenar por lo caro
que estaba el valor. Se deja el contraste tal como se preespecificó, pero si sale
significativo hay que tratarlo como una señal de precio, no de calidad del negocio.
