-- Reproduce la tabla de NOTA-PRECIOS-PLANOS-PRE-2007.md
-- Universo filtrado identico a c4_base.sql, sin quitar ninguna guarda.
with clean as (
  select ticker, fecha, precio_post, ingresos_ttm, multiplo_ps, regla40,
    case when margen_bruto between 0.05 and 0.95 then margen_bruto end mb,
    case when crecimiento between -0.99 and 3.0 then crecimiento end cr
  from hypergrowth_panel
  where fecha >= '1995-01-01' and precio_post > 0
    and ticker ~ '^[A-Z]{1,5}$'
    and not (length(ticker) >= 5 and right(ticker,1) in ('F','Y'))
    and not (length(ticker) >= 4 and right(ticker,1) in ('W','U','R','Z'))
),
px as (
  select *, (precio_post is not distinct from lag(precio_post) over w) ff_ini,
    lag(precio_post,4) over w p_1y, count(mb) over w8 n8,
    row_number() over (partition by ticker, date_trunc('year',fecha) order by fecha) rn_yr
  from clean
  window w  as (partition by ticker order by fecha),
         w8 as (partition by ticker order by fecha rows between 7 preceding and current row)
),
u as (
  select extract(year from fecha)::int yr, precio_post/nullif(p_1y,0)-1 mom12
  from px
  where mb is not null and cr is not null and ingresos_ttm >= 1e7 and precio_post >= 1
    and multiplo_ps*ingresos_ttm between 3e8 and 5e9
    and n8 >= 6 and rn_yr = 1 and regla40 is not null and p_1y is not null
)
select yr, count(*) n,
  round((100.0*avg((mom12>0)::int))::numeric,1) pct_positivo,
  round((100.0*avg((mom12=0)::int))::numeric,1) pct_cero_exacto,
  round((100.0*avg((mom12<0)::int))::numeric,1) pct_negativo,
  round((100*percentile_cont(0.5) within group (order by mom12))::numeric,2) mediana
from u where yr between 2004 and 2023 group by yr order by yr;
