import statistics as st
from km_lib import cargar, contraste, linea

rows,sin=cargar()
print('eventos con metricas y retorno: %d   (descartados %d)'%(len(rows),sin))
desc=[r for r in rows if r['yr']%2==0]
conf=[r for r in rows if r['yr']%2==1]
print('DESCUBRIMIENTO (anos pares): %d      CONFIRMACION (impares): %d'%(len(desc),len(conf)))
print('anos desc:',sorted({r["yr"] for r in desc}))
print('anos conf:',sorted({r["yr"] for r in conf}))

print('\n=== distribucion de las 5 metricas (muestra entera, solo referencia) ===')
for c in ('roic','fcfy','iq','capexrev','ccc'):
    v=sorted(r[c] for r in rows)
    q=lambda p: v[min(int(p/100*(len(v)-1)),len(v)-1)]
    print('  %-9s p10=%8.3f  p25=%8.3f  med=%8.3f  p75=%8.3f  p90=%8.3f'%(c,q(10),q(25),q(50),q(75),q(90)))

print('\n############ SOLO DESCUBRIMIENTO (n=%d) ############'%len(desc))
for c in ('roic','fcfy'):
    print('\n--- %s ---'%c.upper())
    for modo in ('tercil','mediana'):
        a,b,_,_=contraste(desc,c,modo)
        linea('%s por %s'%(c,modo),a,b)

print('\n--- las otras tres metricas (exploratorio, no preespecificadas como contraste) ---')
for c in ('iq','capexrev','ccc'):
    a,b,_,_=contraste(desc,c,'tercil')
    linea('%s por tercil'%c,a,b)

print('\n--- descubrimiento: terciles de ROIC en detalle ---')
s=sorted(desc,key=lambda r:r['roic']); n=len(s); k=n//3
for et,g in (('T1 ROIC bajo',s[:k]),('T2',s[k:n-k]),('T3 ROIC alto',s[n-k:])):
    e=[r['exc'] for r in g]
    print('  %-14s n=%3d  roic[%+.3f,%+.3f]  exc medio=%+7.2f  mediana=%+7.2f'%(
        et,len(g),g[0]['roic'],g[-1]['roic'],sum(e)/len(e),st.median(e)))
print('\n--- descubrimiento: terciles de FCFY en detalle ---')
s=sorted(desc,key=lambda r:r['fcfy']); n=len(s); k=n//3
for et,g in (('T1 FCFY bajo',s[:k]),('T2',s[k:n-k]),('T3 FCFY alto',s[n-k:])):
    e=[r['exc'] for r in g]
    print('  %-14s n=%3d  fcfy[%+.3f,%+.3f]  exc medio=%+7.2f  mediana=%+7.2f'%(
        et,len(g),g[0]['fcfy'],g[-1]['fcfy'],sum(e)/len(e),st.median(e)))
