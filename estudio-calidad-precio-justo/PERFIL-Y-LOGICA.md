# El perfil completo, la lista actual, y por qué podría funcionar

## 1. La receta, entera

```
UNIVERSO
  · Bolsa estadounidense, capitalización entre 300 M$ y 5.000 M$
    (capitalización = multiplo_ps × ingresos_ttm)
  · Sector asignado (nunca 'desconocido')
  · Ingresos TTM ≥ 10 M$   ·   Precio ≥ 1 $
  · Tickers limpios (sin warrants, unidades, derechos ni extranjeras OTC)
  · Excluidos Financial Services y Real Estate

PERFIL (las dos condiciones, ambas relativas a la mediana del año)
  · Desviación típica del MARGEN BRUTO en los últimos 8 trimestres
    por debajo de la mediana del universo ese año
  · Desviación típica del CRECIMIENTO en los últimos 8 trimestres
    por debajo de la mediana del universo ese año
  → hoy: 212 empresas de 682 del universo

SELECCIÓN
  · Ordenar por la subida del precio en los últimos 12 meses
  · Quedarse con el TOP 20%  → ~29–43 nombres

PESOS
  · Por el ORDEN de momentum dentro del grupo (suave, no por el valor)

VENTA
  · Todo, a los 12 meses. Sin excepciones.
  · Sin stop, sin salida por valoración, sin salida por deterioro fundamental
    (las tres probadas: las tres empeoran)
```

**Lo que el perfil NO exige** y conviene tener presente: no exige ser rentable, ni márgenes
altos, ni crecer, ni no diluir, ni valoración barata. Todos esos filtros se probaron y **ninguno
mejora** el resultado. El perfil solo exige **regularidad**, y es un criterio *relativo*: basta
con ser más estable que la mediana de ese año.

## 2. La lista de hoy (43 nombres, top 20% por momentum)

Orden de mayor a menor subida en 12 meses; en la versión ponderada, los de arriba pesan más.

| Sector | Nombres |
|---|---|
| Tecnología (11) | VECO, VSH, HIMX, NTCT, VNET, ROG, DIOD, ATEN, SYNA, DDD, SONO |
| Industriales (10) | NWPX, ALNT, HLIO, DCO, NMM, GRC, CTOS, VVX, SXI, MRCY |
| Consumo cíclico (7) | REAL, MYE, MOV, BJRI, RSI, RERE, BLBD |
| Salud (6) | VCYT, CERS, BVS, BKD, AUPH, LIVN |
| Energía (3) | TTI, OII, PUMP |
| Consumo defensivo (3) | UNFI, SENEA, CHEF |
| Materiales (2) | RYAM, CPAC |
| Comunicación (1) | DLX |

Capitalización mediana ~2.400 M$. Subidas de 12 meses entre +58% y +188%.

## 3. Por qué esto podría funcionar de verdad

Cuatro mecanismos, y los tres primeros tienen apoyo en nuestros propios datos.

### a) Pescamos donde el dinero grande no puede entrar

Un fondo de 10.000 M$ no puede poner un 2% (200 M$) en una compañía de 500 M$ sin quedarse con
el 40% de la empresa. Por debajo de ~2.000 M$ la cobertura de analistas se desploma y los
índices grandes no las incluyen. **Hay menos capital informado compitiendo por el mismo
precio**, y el descubrimiento de precio es más lento.

### b) El momentum captura información que viaja despacio

La explicación estándar del momentum es la infrarreacción: las noticias se incorporan al precio
poco a poco. Donde hay pocos analistas, se incorporan **más despacio**.

**Nuestros datos lo confirman con precisión**: el diferencial de momentum es +7,84 pp en micro,
+3,82 en small, +2,67 en mid, y desaparece en large y mega (sección 3). Decae exactamente según
sube la cobertura. Eso es más consistente con un mecanismo real que con una casualidad.

### c) El filtro de estabilidad es un detector de mentiras

Los universos de pequeña capitalización están llenos de valores especulativos con perfil de
lotería, que atraen demanda minorista y están sistemáticamente caros. Filtrar por regularidad
fundamental **los elimina**.

Y esto es lo que más me convence: **el mismo momentum da +3,44 pp dentro del perfil y +0,94 pp
fuera** (sección 20.3 de `RESULTADOS.md`), y fuera se desvanece a 4 trimestres. No es que el
perfil aporte por su cuenta y el momentum por la suya: **es que el perfil dice cuándo creerse el
momentum**.

Dicho de otro modo: una subida de precio no distingue por sí sola entre "el negocio está
mejorando en silencio y nadie se ha dado cuenta" y "es un valor de moda". La estabilidad
fundamental es la prueba de corroboración.

### d) Doce meses porque la información tarda meses, no semanas

Dos tercios de lo que se pierde rotando cada trimestre **no son costes, son señal**
(sección 11). La ventaja se acumula a lo largo del año.

## 4. Lo que NO estamos aprovechando

Conviene tenerlo claro para no contarse una película:

- **No compramos calidad compuesta.** El test del "vivero" falló: el perfil no distingue en
  absoluto quién se convertirá en gigante (41% en todos los tramos de destino).
- **No aprovechamos la valoración.** Dentro de la calidad, el precio no predice.
- **No acertamos sectores.** El orden sectorial no persiste.
- **No es una cartera de calidad.** Entran cíclicas, navieras, empresas con margen operativo
  negativo y algunas que diluyen al 20%.

Lo que hay es más estrecho y más honesto: **operar donde el dinero grande no llega, comprando
fuerza de precio solo cuando el fundamental la corrobora.**

## 5. Qué haría que dejara de funcionar

- **Que se comprima la prima de tamaño**: más ETFs de small caps, más cobertura algorítmica,
  más capital paciente en el tramo. El mecanismo es una ineficiencia, y las ineficiencias se
  arbitran.
- **La liquidez**: no se puede mover mucho dinero en 29 compañías de 300 M$–5.000 M$. Esta
  estrategia tiene un techo de capacidad bajo, y ese techo es también lo que la protege.
- **El régimen**: la ventaja es mayor en 2016–2024 (+13,83 pp) que en 2008–2015 (+7,54 pp).

## 6. Las cifras, con sus asteriscos

| | Valor | Asterisco |
|---|---|---|
| Periodo medido | 2008–2024, **17 años** | Solo hay historia utilizable desde 2005 |
| CAGR (ponderado por momentum) | 20,53–20,72% | Panel sin quiebras: es un techo |
| CAGR del SPY | ~10,0% | |
| Ventaja | ~10 pp anuales | Réstale ~1 pp por los dividendos |
| Ventanas de 5 años perdedoras | **0 de 13** | La peor gana por +4,18 pp |
| Años perdedores frente al SPY | 4 de 17 | 2009, 2014, 2015, 2021 |

**Todo está medido sobre PRECIO**, no sobre retorno total. Si `precio_post` no incorpora
dividendos —y hay indicios de que no—, la comparación favorece a nuestra cartera, porque el
S&P reparte ~1,9% anual y estas compañías bastante menos. **Impacto estimado: ~0,9 pp anuales
de ventaja inflada.** No lo he podido verificar en el panel; queda como comprobación pendiente
y conviene descontarlo mentalmente.
