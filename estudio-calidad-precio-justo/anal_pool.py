import math, statistics as st, random
rows=[]
# ciclicas
raw=open('ciclicas_eventos.txt').read().strip()
ev={}
for blk in raw.split(';'):
    if not blk.strip(): continue
    t,sec,evs=blk.split('#')
    for e in evs.split(','):
        y,v,r,q=e.split(':'); ev[(t,y)]=(sec,float(v),float(r),float(q))
for l in open('deuda_cic.csv').read().splitlines()[1:]:
    t,y,d,c=l.split(',')
    if (t,y) not in ev: continue
    sec,v,r,q=ev[(t,y)]
    rows.append(dict(t=t,yr=int(y),sec=sec,exc=r-q,ndv=(float(d)-float(c))/1e6/v,src='cic'))
# piloto
pm={}
for l in open('panel_muestra.csv').read().splitlines()[1:]:
    p=l.split(','); pm[(p[0],p[1])]=(float(p[2]),float(p[4]),float(p[5]))
sect={}
for l in open('sectores.csv').read().splitlines()[1:]:
    p=l.split(','); sect[p[0]]=p[1]
nz=0
for l in open('deuda.csv').read().splitlines()[1:]:
    t,y,d,c=l.split(',')
    if (t,y) not in pm: continue
    v,r,q=pm[(t,y)]
    if r==0.0 and q==0.0: nz+=1; continue          # placeholders sin retorno
    rows.append(dict(t=t,yr=int(y),sec=sect.get(t,'?'),exc=r-q,ndv=(float(d)-float(c))/1e6/v,src='pil'))
print('eventos totales: %d  (ciclicas %d + piloto %d; %d del piloto descartados por retorno 0/0)'%(
    len(rows),sum(1 for r in rows if r['src']=='cic'),sum(1 for r in rows if r['src']=='pil'),nz))

def welch(a,b):
    na,nb=len(a),len(b); ma,mb=sum(a)/na,sum(b)/nb
    va,vb=st.variance(a)/na,st.variance(b)/nb
    return (ma-mb)/math.sqrt(va+vb), ma-mb
def perm_p(a,b,it=20000):
    obs=abs(sum(a)/len(a)-sum(b)/len(b)); pool=a+b; na=len(a); c=0; rnd=random.Random(11)
    for _ in range(it):
        rnd.shuffle(pool)
        if abs(sum(pool[:na])/na-sum(pool[na:])/(len(pool)-na))>=obs: c+=1
    return (c+1)/(it+1)

for etiqueta, sel in [('CONJUNTO (264)',rows),
                      ('solo ciclicas', [r for r in rows if r['src']=='cic']),
                      ('solo piloto',   [r for r in rows if r['src']=='pil'])]:
    s=sorted(sel,key=lambda r:r['ndv']); n=len(s); k=n//3
    a=[r['exc'] for r in s[:k]]; b=[r['exc'] for r in s[n-k:]]
    t,d=welch(a,b)
    print('\n%-16s n=%3d   T1=%+6.2f  T3=%+6.2f   T1-T3=%+6.2f pp  t=%+5.2f  p_perm=%.3f'%(
        etiqueta,n,sum(a)/len(a),sum(b)/len(b),d,t,perm_p(a[:],b[:])))

# deciles: hay algo no lineal en el extremo?
s=sorted(rows,key=lambda r:r['ndv']); n=len(s)
print('\n=== deciles de deuda neta/ventas (conjunto) ===')
for i in range(10):
    g=s[i*n//10:(i+1)*n//10]
    e=[r['exc'] for r in g]
    print('  D%-2d n=%2d  ndv[%+6.2f,%+6.2f]  exc medio=%+7.2f  mediana=%+7.2f'%(
        i+1,len(g),g[0]['ndv'],g[-1]['ndv'],sum(e)/len(e),st.median(e)))

# el extremo: >1x ventas
alto=[r for r in rows if r['ndv']>1.0]; resto=[r for r in rows if r['ndv']<=1.0]
a=[r['exc'] for r in alto]; b=[r['exc'] for r in resto]
t,d=welch(a,b)
print('\n=== apalancamiento extremo (deuda neta > 1x ventas) ===')
print('  n=%d de %d   exc medio=%+.2f vs %+.2f   dif=%+.2f pp  t=%+.2f  p_perm=%.3f'%(
    len(alto),len(rows),sum(a)/len(a),sum(b)/len(b),d,t,perm_p(a[:],b[:])))
print('  tasa de desastres (exc < -30pp): extremo %.0f%%  resto %.0f%%'%(
    100*sum(1 for x in a if x<-30)/len(a), 100*sum(1 for x in b if x<-30)/len(b)))
