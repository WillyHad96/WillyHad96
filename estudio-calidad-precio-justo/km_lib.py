import math, statistics as st, random

def cargar():
    ev={}
    for blk in open('ciclicas_eventos.txt').read().strip().split(';'):
        if not blk.strip(): continue
        t,sec,evs=blk.split('#')
        for e in evs.split(','):
            y,v,r,q=e.split(':'); ev[(t,y)]=(sec,float(r),float(q))
    pm={}
    for l in open('panel_muestra.csv').read().splitlines()[1:]:
        p=l.split(','); pm[(p[0],p[1])]=(float(p[4]),float(p[5]))
    sect={}
    for l in open('sectores.csv').read().splitlines()[1:]:
        p=l.split(','); sect[p[0]]=p[1]
    km={}
    for l in open('km.csv').read().splitlines()[1:]:
        p=l.split(',')
        km[(p[0],p[1])]=dict(fy=p[2],roic=float(p[3]),fcfy=float(p[4]),
                             iq=float(p[5]),capexrev=float(p[6]),ccc=float(p[7]))
    rows=[]; sin_ret=0
    for (t,y),m in km.items():
        if (t,y) in ev:
            sec,r,q=ev[(t,y)]; src='cic'
        elif (t,y) in pm:
            r,q=pm[(t,y)]
            if r==0.0 and q==0.0: sin_ret+=1; continue
            sec=sect.get(t,'?'); src='pil'
        else:
            sin_ret+=1; continue
        rows.append(dict(t=t,yr=int(y),sec=sec,exc=r-q,src=src,**m))
    return rows,sin_ret

def welch(a,b):
    na,nb=len(a),len(b); ma,mb=sum(a)/na,sum(b)/nb
    va,vb=st.variance(a)/na,st.variance(b)/nb
    t=(ma-mb)/math.sqrt(va+vb)
    df=(va+vb)**2/(va**2/(na-1)+vb**2/(nb-1))
    return t,df,ma-mb

def perm_p(a,b,it=20000,seed=13):
    obs=abs(sum(a)/len(a)-sum(b)/len(b)); pool=list(a)+list(b); na=len(a); c=0
    rnd=random.Random(seed)
    for _ in range(it):
        rnd.shuffle(pool)
        if abs(sum(pool[:na])/na-sum(pool[na:])/(len(pool)-na))>=obs: c+=1
    return (c+1)/(it+1)

def contraste(rows,campo,modo):
    """modo='tercil' -> T3 (alto) vs T1 (bajo);  modo='mediana' -> mitad alta vs baja.
       Devuelve (alto, bajo) como listas de exceso."""
    s=sorted(rows,key=lambda r:r[campo]); n=len(s)
    if modo=='tercil':
        k=n//3; bajo=s[:k]; alto=s[n-k:]
    else:
        k=n//2; bajo=s[:k]; alto=s[n-k:]
    return [r['exc'] for r in alto],[r['exc'] for r in bajo],alto,bajo

def linea(etq,alto,bajo,seed=13):
    t,df,d=welch(alto,bajo)
    print('  %-22s n=%3d/%3d  alto=%+7.2f  bajo=%+7.2f  ALTO-BAJO=%+7.2f pp  t=%+5.2f  p_perm=%.4f'%(
        etq,len(alto),len(bajo),sum(alto)/len(alto),sum(bajo)/len(bajo),d,t,perm_p(alto,bajo,seed=seed)))
    return d
