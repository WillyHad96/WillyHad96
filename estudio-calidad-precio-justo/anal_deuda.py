import json, math, statistics as st, random
raw=open('ciclicas_eventos.txt').read().strip()
ev={}
for blk in raw.split(';'):
    if not blk.strip(): continue
    t,sec,evs=blk.split('#')
    for e in evs.split(','):
        y,v,r,q=e.split(':')
        ev[(t,y)]=dict(sec=sec,ventas=float(v),ret=float(r),qqq=float(q))

rows=[]
for l in open('deuda_cic.csv').read().splitlines()[1:]:
    t,y,d,c=l.split(',')
    k=(t,y)
    if k not in ev: continue
    e=ev[k]
    nd=(float(d)-float(c))/1e6           # deuda neta en M
    rows.append(dict(t=t,yr=int(y),sec=e['sec'],ventas=e['ventas'],
                     ret=e['ret'],qqq=e['qqq'],exc=e['ret']-e['qqq'],
                     nd=nd, ndv=nd/e['ventas']))
print('eventos con retorno y deuda:',len(rows))
print('anos:',min(r['yr'] for r in rows),'-',max(r['yr'] for r in rows))

def desc(name,xs):
    n=len(xs)
    if n==0: return
    m=sum(xs)/n
    sd=st.stdev(xs) if n>1 else 0
    print('  %-14s n=%3d  media=%7.2f  mediana=%7.2f  sd=%6.1f  se=%5.2f'%(
        name,n,m,st.median(xs),sd,sd/math.sqrt(n) if n>1 else 0))

def welch(a,b):
    na,nb=len(a),len(b)
    ma,mb=sum(a)/na,sum(b)/nb
    va,vb=st.variance(a)/na, st.variance(b)/nb
    t=(ma-mb)/math.sqrt(va+vb)
    df=(va+vb)**2/(va**2/(na-1)+vb**2/(nb-1))
    return t,df,ma-mb

def perm_p(a,b,it=20000):
    obs=abs(sum(a)/len(a)-sum(b)/len(b))
    pool=a+b; na=len(a); cnt=0
    rnd=random.Random(7)
    for _ in range(it):
        rnd.shuffle(pool)
        if abs(sum(pool[:na])/na - sum(pool[na:])/(len(pool)-na)) >= obs: cnt+=1
    return (cnt+1)/(it+1)

print('\n=== distribucion de deuda neta / ventas ===')
v=sorted(r['ndv'] for r in rows)
for p in (0,10,25,50,75,90,100):
    i=min(int(p/100*(len(v)-1)),len(v)-1)
    print('  p%-3d %7.3f'%(p,v[i]))
print('  con caja neta (ndv<0): %d de %d (%.0f%%)'%(
    sum(1 for x in v if x<0),len(v),100*sum(1 for x in v if x<0)/len(v)))

# --- terciles globales ---
srt=sorted(rows,key=lambda r:r['ndv'])
n=len(srt); k=n//3
tercios=[srt[:k],srt[k:n-k],srt[n-k:]]
print('\n=== terciles GLOBALES por deuda neta/ventas (retorno en exceso vs QQQ, %) ===')
lab=['T1 poca deuda','T2 media','T3 mucha deuda']
for l,g in zip(lab,tercios):
    print('  %-16s corte ndv [%6.2f, %6.2f]'%(l,g[0]['ndv'],g[-1]['ndv']))
    desc('',[r['exc'] for r in g])
a=[r['exc'] for r in tercios[0]]; b=[r['exc'] for r in tercios[2]]
t,df,d=welch(a,b)
print('  T1 - T3 = %+.2f pp   t=%.2f  gl=%.0f  p_perm=%.4f'%(d,t,df,perm_p(a[:],b[:])))

# --- terciles DENTRO de cada ano (control de ano) ---
byyr={}
for r in rows: byyr.setdefault(r['yr'],[]).append(r)
g1,g2,g3=[],[],[]
usados=0
for y,g in sorted(byyr.items()):
    if len(g)<6: continue
    usados+=len(g)
    s=sorted(g,key=lambda r:r['ndv']); m=len(s); kk=m//3
    g1+= [r['exc'] for r in s[:kk]]; g3+=[r['exc'] for r in s[m-kk:]]
    g2+= [r['exc'] for r in s[kk:m-kk]]
print('\n=== terciles DENTRO de cada ano (solo anos con n>=6; %d eventos) ==='%usados)
for l,g in zip(lab,[g1,g2,g3]): desc(l,g)
if g1 and g3:
    t,df,d=welch(g1,g3)
    print('  T1 - T3 = %+.2f pp   t=%.2f  gl=%.0f  p_perm=%.4f'%(d,t,df,perm_p(g1[:],g3[:])))

# --- control por sector ---
print('\n=== control por sector (terciles dentro de cada sector) ===')
bysec={}
for r in rows: bysec.setdefault(r['sec'],[]).append(r)
s1,s3=[],[]
for s,g in sorted(bysec.items()):
    srt2=sorted(g,key=lambda r:r['ndv']); m=len(srt2); kk=m//3
    if kk<2: 
        print('  %-20s n=%3d  (muy pocos, se omite)'%(s,m)); continue
    lo=[r['exc'] for r in srt2[:kk]]; hi=[r['exc'] for r in srt2[m-kk:]]
    s1+=lo; s3+=hi
    print('  %-20s n=%3d  T1=%+6.1f  T3=%+6.1f  dif=%+6.1f'%(
        s,m,sum(lo)/len(lo),sum(hi)/len(hi),sum(lo)/len(lo)-sum(hi)/len(hi)))
if s1 and s3:
    t,df,d=welch(s1,s3)
    print('  AGREGADO dentro de sector: T1-T3 = %+.2f pp  t=%.2f  p_perm=%.4f'%(d,t,perm_p(s1[:],s3[:])))

# --- correlacion de rangos ---
def spearman(xs,ys):
    def rk(v):
        s=sorted(range(len(v)),key=lambda i:v[i]); r=[0]*len(v)
        for pos,i in enumerate(s): r[i]=pos
        return r
    a,b=rk(xs),rk(ys); n=len(xs)
    ma,mb=sum(a)/n,sum(b)/n
    num=sum((a[i]-ma)*(b[i]-mb) for i in range(n))
    den=math.sqrt(sum((x-ma)**2 for x in a)*sum((x-mb)**2 for x in b))
    return num/den
print('\n=== correlacion de rangos ndv vs exceso ===')
print('  Spearman = %+.4f  (n=%d)'%(spearman([r['ndv'] for r in rows],[r['exc'] for r in rows]),len(rows)))

# --- cola izquierda ---
print('\n=== cola izquierda: los 15 peores eventos ===')
peor=sorted(rows,key=lambda r:r['exc'])[:15]
med=st.median([r['ndv'] for r in rows])
print('  ndv mediano de la muestra: %.3f'%med)
print('  ndv mediano de los 15 peores: %.3f'%st.median([r['ndv'] for r in peor]))
for r in peor:
    print('   %-6s %d  exc=%+7.1f  ndv=%+6.2f  %s'%(r['t'],r['yr'],r['exc'],r['ndv'],r['sec']))
