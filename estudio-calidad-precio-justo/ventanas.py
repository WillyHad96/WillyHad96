# Descorrelacion REAL (observada - null de permutacion) en cada ventana de 17 anhos.
# Responde: ¿cuanto de lo que medimos en 2007-2023 era la ventana y no la regla?
import numpy as np
P={}
for l in open('nasdaq_febrero.csv').read().splitlines()[1:]:
    y,p=l.split(','); P[int(y)]=float(p)
yrs=np.array(sorted(y for y in P if y-1 in P and y+1 in P))
idx=np.array([P[y+1]/P[y]-1 for y in yrs])
sig=np.array([1.0 if P[y]/P[y-1]-1>0 else 0.0 for y in yrs])
RF=0.02; n=len(yrs); W=17
cagr=lambda r: np.prod(1+r)**(1/len(r))-1
rng=np.random.default_rng(13)

def desc_real(s_sig,s_idx,IT=4000):
    o=s_sig*s_idx+(1-s_sig)*RF
    obs=np.corrcoef(o,s_idx)[0,1]
    E=np.array([rng.permutation(s_sig) for _ in range(IT)])
    Pf=E*s_idx+(1-E)*RF
    pm=Pf-Pf.mean(axis=1,keepdims=True); qm=s_idx-s_idx.mean()
    cr=(pm@qm)/np.sqrt((pm**2).sum(axis=1)*(qm**2).sum())
    return obs, cr.mean(), obs-cr.mean(), np.mean(cr<=obs)

print(f"  {'ventana':>13} {'corr obs':>9} {'corr azar':>10} {'DESC REAL':>10} {'p':>7} {'salidas':>8}")
filas=[]
for i in range(n-W+1):
    s=slice(i,i+W)
    if sig[s].sum()==W:
        print(f"  {yrs[i]}-{yrs[i+W-1]} {'(nunca sale)':>38}"); continue
    o,a,d,p=desc_real(sig[s],idx[s])
    filas.append((yrs[i],d,p))
    marca=' <<<' if yrs[i]==2007 else ''
    print(f"  {yrs[i]}-{yrs[i+W-1]} {o:>9.3f} {a:>10.3f} {d:>+10.3f} {p:>7.3f} {int(W-sig[s].sum()):>8}{marca}")
D=np.array([f[1] for f in filas]); PP=np.array([f[2] for f in filas])
print()
print(f"  ventanas: {len(filas)}")
print(f"  DESCORRELACION REAL — mediana {np.median(D):+.3f}   rango [{D.min():+.3f}, {D.max():+.3f}]")
print(f"  ventanas con p<0,05: {np.sum(PP<0.05)}/{len(filas)} ({100*np.mean(PP<0.05):.0f}%)")
print(f"  ventanas con descorrelacion real mas fuerte que -0,14 (el C7): {np.sum(D<-0.14)}/{len(filas)}"
      f" ({100*np.mean(D<-0.14):.0f}%)")
print()
print("  Sobre los 54 anhos completos:")
o,a,d,p=desc_real(sig,idx,IT=20000)
print(f"    corr obs {o:.3f}   corr azar {a:.3f}   DESC REAL {d:+.3f}   p={p:.4f}")
