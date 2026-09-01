import statistics as st
from km_lib import cargar, contraste, linea, welch, perm_p

rows,_=cargar()
desc=[r for r in rows if r['yr']%2==0]
conf=[r for r in rows if r['yr']%2==1]

REGLA=[('ROIC','roic','mediana','+'),('FCFY','fcfy','tercil','-')]

print('############ CONFIRMACION (anos impares, n=%d) — regla cerrada, una sola pasada ############'%len(conf))
res={}
for nom,campo,modo,signo in REGLA:
    ad,bd,_,_=contraste(desc,campo,modo)
    ac,bc,ga,gb=contraste(conf,campo,modo)
    dd=sum(ad)/len(ad)-sum(bd)/len(bd)
    print('\n--- %s (%s), signo esperado %s ---'%(nom,modo,signo))
    print('  descubrimiento (referencia): ALTO-BAJO=%+7.2f pp'%dd)
    dc=linea('CONFIRMACION',ac,bc)
    ok_signo = (dc>0)==(dd>0)
    print('  condicion 1 (mismo signo): %s'%('SI' if ok_signo else 'NO'))
    p=perm_p(ac,bc)
    print('  condicion 2 (p<0.05): %s (p=%.4f)'%('SI' if p<0.05 else 'NO',p))
    res[nom]=dict(dd=dd,dc=dc,p=p,ok=ok_signo and p<0.05,campo=campo,modo=modo)

print('\n=== control por ANO dentro de confirmacion (solo anos con n>=6) ===')
for nom,campo,modo,_ in REGLA:
    byyr={}
    for r in conf: byyr.setdefault(r['yr'],[]).append(r)
    A,B=[],[]; usados=0
    for y,g in sorted(byyr.items()):
        if len(g)<6: continue
        usados+=len(g)
        a,b,_,_=contraste(g,campo,modo); A+=a; B+=b
    if A and B:
        print('  %s (%d eventos en anos usados)'%(nom,usados)); linea('  dentro de ano',A,B)

print('\n=== control por SECTOR dentro de confirmacion ===')
for nom,campo,modo,_ in REGLA:
    bysec={}
    for r in conf: bysec.setdefault(r['sec'],[]).append(r)
    A,B=[],[]
    for s,g in sorted(bysec.items()):
        if len(g)<6: continue
        a,b,_,_=contraste(g,campo,modo); A+=a; B+=b
    if A and B:
        print('  %s'%nom); linea('  dentro de sector',A,B)

print('\n=== por si sirve de contexto: la muestra entera (264, NO es el test) ===')
for nom,campo,modo,_ in REGLA:
    a,b,_,_=contraste(rows,campo,modo)
    linea('%s conjunto'%nom,a,b)

print('\n=== veredicto ===')
for nom in res:
    r=res[nom]
    print('  %-5s descubrimiento %+7.2f -> confirmacion %+7.2f (p=%.3f):  %s'%(
        nom,r['dd'],r['dc'],r['p'],'HALLAZGO' if r['ok'] else 'REFUTADO'))
