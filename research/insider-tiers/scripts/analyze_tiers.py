#!/usr/bin/env python3
import json, statistics as st, collections, random, math
import csv, os
CSV = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "insider_events.csv")

def load(path=CSV):
    """Read the exported event table; every numeric column is cast, blanks -> None."""
    out = []
    with open(path) as f:
        for row in csv.DictReader(f):
            e = {}
            for k, v in row.items():
                if k in ("symbol", "month", "txdate", "entry_date"):
                    e[k] = v
                else:
                    e[k] = float(v) if v not in ("", None) else None
            out.append(e)
    return out

ALL=[e for e in load() if e["r12m"] is not None and e["r12m_QQQ"] is not None]
OD=[e for e in ALL if e["n_od"]>0 and e["value_od"]>0]
med=lambda x: st.median(x) if x else float('nan')
mean=lambda x: sum(x)/len(x) if x else float('nan')

T=[(0,0.01,"<0.01%"),(0.01,0.05,"0.01-0.05%"),(0.05,0.15,"0.05-0.15%"),(0.15,0.50,"0.15-0.50%"),(0.50,1e9,">0.50%")]
def tier(e,k="pct_cap_od"):
    for lo,hi,l in T:
        if lo<=e[k]<hi: return l
    return T[-1][2]
order=[t[2] for t in T]

def show(events,title,hz="r12m",k="pct_cap_od"):
    print("\n=== %s | horizon %s ==="%(title,hz))
    print("%-13s %5s %5s %9s %9s | %8s %8s %6s | %9s %9s"%(
        "tier","n","syms","medCap$M","medBuy$k","med","mean","win%","exQQQ","exIWM"))
    g=collections.defaultdict(list)
    for e in events:
        if e.get(hz) is None: continue
        g[tier(e,k)].append(e)
    for l in order:
        v=g.get(l,[])
        if len(v)<5: continue
        r=[x[hz] for x in v]
        eq=[x[hz]-x[hz+"_QQQ"] for x in v if x.get(hz+"_QQQ") is not None]
        ei=[x[hz]-x[hz+"_IWM"] for x in v if x.get(hz+"_IWM") is not None]
        print("%-13s %5d %5d %9.0f %9.0f | %7.1f%% %7.1f%% %5.0f%% | %8.1f%% %8.1f%%"%(
            l,len(v),len({x['symbol'] for x in v}),med([x['mcap'] for x in v])/1e6,
            med([x['value_od'] for x in v])/1e3,100*med(r),100*mean(r),
            100*sum(1 for x in r if x>0)/len(r),100*med(eq),100*med(ei)))
    return g

print("OFFICER/DIRECTOR OPEN-MARKET BUYS ONLY  (n=%d events, %d companies, 2014-2025)"%(len(OD),len({e['symbol'] for e in OD})))
for hz in ("r3m","r6m","r12m"): show(OD,"By buy size as %% of market cap",hz)

print("\n=== SAME TIERS, 10%%-OWNER (fund/PIPE) BUYS FOR CONTRAST | 12m ===")
TEN=[e for e in ALL if e["value_10"]>0]
show(TEN,"10%-owner buys","r12m","pct_cap")

print("\n=== SIZE CONTROL (officers/directors, median 12m excess vs IWM) ===")
def cb(e):
    m=e["mcap"]
    return "nano <50M" if m<50e6 else "micro 50-300M" if m<300e6 else "small 0.3-2B" if m<2e9 else "mid/large >2B"
print("%-16s %20s %20s"%("cap bucket","LOW <0.05% of cap","HIGH >=0.15% of cap"))
for b in ["nano <50M","micro 50-300M","small 0.3-2B","mid/large >2B"]:
    lo=[e for e in OD if cb(e)==b and e["pct_cap_od"]<0.05 and e.get("r12m_IWM") is not None]
    hi=[e for e in OD if cb(e)==b and e["pct_cap_od"]>=0.15 and e.get("r12m_IWM") is not None]
    f=lambda v: ("n=%-4d %+6.1f%%"%(len(v),100*med([x["r12m"]-x["r12m_IWM"] for x in v]))) if len(v)>=10 else "n=%-4d    --"%len(v)
    print("%-16s %20s %20s"%(b,f(lo),f(hi)))

print("\n=== CONVICTION SIGNALS (officers/directors, 12m) ===")
tests=[("all officer/director buys",lambda e:True),
       ("CEO or CFO bought",lambda e:e["ceo_cfo"]==1),
       ("2+ insiders same month",lambda e:e["n_insiders"]>=2),
       ("buy >=0.15% of cap",lambda e:e["pct_cap_od"]>=0.15),
       ("CEO/CFO AND >=0.15% cap",lambda e:e["ceo_cfo"]==1 and e["pct_cap_od"]>=0.15),
       ("2+ insiders AND >=0.15% cap",lambda e:e["n_insiders"]>=2 and e["pct_cap_od"]>=0.15),
       ("buy >= $250k",lambda e:e["value_od"]>=250e3),
       ("CEO/CFO AND >= $250k",lambda e:e["ceo_cfo"]==1 and e["value_od"]>=250e3)]
print("%-30s %5s %8s %8s %6s %9s %9s"%("filter","n","med","mean","win%","exQQQ","exIWM"))
for lbl,sel in tests:
    v=[e for e in OD if sel(e)]
    if len(v)<20: continue
    r=[x["r12m"] for x in v]
    eq=[x["r12m"]-x["r12m_QQQ"] for x in v]
    ei=[x["r12m"]-x["r12m_IWM"] for x in v if x.get("r12m_IWM") is not None]
    print("%-30s %5d %7.1f%% %7.1f%% %5.0f%% %8.1f%% %8.1f%%"%(
        lbl,len(v),100*med(r),100*mean(r),100*sum(1 for x in r if x>0)/len(r),100*med(eq),100*med(ei)))

random.seed(7)
def boot(sel_a,sel_b,pool,n=4000,key="r12m",bench="r12m_IWM"):
    bysym=collections.defaultdict(list)
    for e in pool: bysym[e["symbol"]].append(e)
    syms=sorted(bysym); out=[]
    for _ in range(n):
        s=[]
        for _ in range(len(syms)): s+=bysym[random.choice(syms)]
        a=[x[key]-x[bench] for x in s if sel_a(x) and x.get(bench) is not None]
        b=[x[key]-x[bench] for x in s if sel_b(x) and x.get(bench) is not None]
        if len(a)>=15 and len(b)>=15: out.append(med(a)-med(b))
    out.sort()
    return med(out),out[int(.025*len(out))],out[int(.975*len(out))],sum(1 for d in out if d<=0)/len(out)
print("\n=== CLUSTER BOOTSTRAP by company (4000 reps), median 12m excess vs IWM ===")
for lbl,a,b in [("(>=0.15% of cap) - (<0.05% of cap)",lambda e:e["pct_cap_od"]>=0.15,lambda e:e["pct_cap_od"]<0.05),
                ("(>=$250k) - (<$50k)",lambda e:e["value_od"]>=250e3,lambda e:e["value_od"]<50e3)]:
    d,lo,hi,p=boot(a,b,OD)
    print("  %-36s %+6.1f pp  95%% CI [%+.1f, %+.1f]  P(<=0)=%.3f"%(lbl,100*d,100*lo,100*hi,p))

print("\n=== ROBUSTNESS: same tiers with 2020 entries removed (12m, officers/directors) ===")
no20=[e for e in OD if not e["month"].startswith("2020")]
show(no20,"By buy size as %% of market cap, ex-2020","r12m")

print("\n=== IMPLEMENTABLE STRATEGY: each quarter buy every signal, equal weight, hold 3 months ===")
print("    (ex-2020 = same rule with the four 2020 cohorts dropped; shows how much is COVID rebound)")
def quarter(m): y,mm=m.split("-"); return "%s-Q%d"%(y,(int(mm)-1)//3+1)

def cagr(qs,q):
    """Compound the equal-weight quarterly returns of the cohorts in qs."""
    cum=1.0
    for k in qs: cum*=(1+mean([x["r3m"] for x in q[k]]))
    return cum-1, cum**(4/len(qs))-1

print("%-28s %4s %8s %8s %8s %6s %6s %10s %9s %9s"%(
    "filter","qtrs","avg/qtr","QQQ/qtr","vol/qtr","corr","beta","cum","CAGR","CAGRex20"))
for lbl,sel in [("all officer/director buys",lambda e:True),
                (">=0.05% of cap",lambda e:e["pct_cap_od"]>=0.05),
                (">=0.15% of cap",lambda e:e["pct_cap_od"]>=0.15),
                (">=$250k",lambda e:e["value_od"]>=250e3),
                ("CEO/CFO + >=0.15% cap",lambda e:e["ceo_cfo"]==1 and e["pct_cap_od"]>=0.15)]:
    q=collections.defaultdict(list)
    for e in OD:
        if e["r3m"] is None or e.get("r3m_QQQ") is None or not sel(e): continue
        q[quarter(e["month"])].append(e)
    qs=sorted(k for k,v in q.items() if len(v)>=3)
    if len(qs)<20: continue
    s=[mean([x["r3m"] for x in q[k]]) for k in qs]
    b=[mean([x["r3m_QQQ"] for x in q[k]]) for k in qs]
    ms,mb=mean(s),mean(b)
    sd=lambda v,m: math.sqrt(sum((x-m)**2 for x in v)/(len(v)-1))
    ss,sb=sd(s,ms),sd(b,mb)
    cov=sum((s[i]-ms)*(b[i]-mb) for i in range(len(s)))/(len(s)-1)
    cum,cg=cagr(qs,q)
    _,cg20=cagr([k for k in qs if not k.startswith("2020")],q)
    print("%-28s %4d %7.2f%% %7.2f%% %7.2f%% %+5.2f %+5.2f %9.0f%% %8.1f%% %8.1f%%"%(
        lbl,len(qs),100*ms,100*mb,100*ss,cov/(ss*sb),cov/(sb*sb),100*cum,100*cg,100*cg20))
