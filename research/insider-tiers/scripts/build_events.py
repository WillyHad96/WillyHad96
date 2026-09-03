#!/usr/bin/env python3
"""Build insider-purchase events with %-of-capital tiers and forward returns."""
import json, glob, os, re, bisect, datetime as dt, collections

SP = "/tmp/claude-0/-home-user-WillyHad96/1981e284-84b3-5ae2-912a-581463ab2224/scratchpad"
COMMON = re.compile(r'\b(common|ordinary)\b', re.I)
BAD = re.compile(r'\b(warrant|preferred|unit|option|note|right|debenture|depositary|convertible|forward)\b', re.I)
START, END = "2014-01-01", "2025-08-31"        # events window (12m forward needs data to 2026-08)

def d(s): return dt.date.fromisoformat(s)

def load_series(path, valkey):
    """-> (sorted dates list, values list)"""
    rows = json.load(open(path))
    pairs = sorted((r["date"], r[valkey]) for r in rows if r.get(valkey) is not None)
    return [p[0] for p in pairs], [p[1] for p in pairs]

def at_or_before(dates, vals, target):
    i = bisect.bisect_right(dates, target) - 1
    return vals[i] if i >= 0 else None

def at_or_after(dates, vals, target, maxgap=10):
    i = bisect.bisect_left(dates, target)
    if i >= len(dates): return None, None
    if (d(dates[i]) - d(target)).days > maxgap: return None, None
    return vals[i], dates[i]

# benchmarks
bench = {}
for b in ("QQQ", "IWM", "SPY"):
    p = os.path.join(SP, "data", "price", b + ".json")
    if os.path.exists(p): bench[b] = load_series(p, "adjClose")

events = []
skipped = collections.Counter()
for f in sorted(glob.glob(SP + "/data/insider/*.json")):
    sym = os.path.basename(f)[:-5]
    ppath = os.path.join(SP, "data", "price", sym + ".json")
    mpath = os.path.join(SP, "data", "mcap", sym + ".json")
    if not (os.path.exists(ppath) and os.path.exists(mpath)):
        skipped["no_price_or_mcap"] += 1; continue
    pdates, pvals = load_series(ppath, "adjClose")
    mdates, mvals = load_series(mpath, "marketCap")
    if not pdates or not mdates: skipped["empty_series"] += 1; continue

    # collect qualifying purchase transactions
    txs = []
    for r in json.load(open(f)):
        if r.get("transactionType") != "P-Purchase": continue
        nm = r.get("securityName") or ""
        if not COMMON.search(nm) or BAD.search(nm): continue
        td, fd = r.get("transactionDate"), r.get("filingDate")
        if not td or not fd or not (START <= td <= END): continue
        px, sh = r.get("price"), r.get("securitiesTransacted")
        if not px or not sh or px <= 0 or sh <= 0: continue
        owned = r.get("securitiesOwned")
        who = (r.get("typeOfOwner") or "").lower()
        if (d(fd) - d(td)).days > 45: continue          # drop stale/amended filings
        txs.append({"td": td, "fd": fd, "val": px * sh, "sh": sh, "owned": owned,
                    "who": who, "is10": int("10 percent" in who), "cik": r.get("reportingCik")})
    if not txs: skipped["no_tx"] += 1; continue

    # cluster by calendar month of transaction date
    bymonth = collections.defaultdict(list)
    for t in txs: bymonth[t["td"][:7]].append(t)

    for month, group in bymonth.items():
        value = sum(t["val"] for t in group)
        value_od = sum(t["val"] for t in group if not t["is10"])   # officers/directors only
        value_10 = sum(t["val"] for t in group if t["is10"])
        entry_signal = max(t["fd"] for t in group)      # public knowledge date
        txdate = max(t["td"] for t in group)
        mcap = at_or_before(mdates, mvals, txdate)
        if not mcap or mcap <= 0: continue
        entry_px, entry_date = at_or_after(pdates, pvals, entry_signal)
        if not entry_px: continue
        # stake increase: largest single insider's buy vs their prior holding
        stake_inc = None
        for t in group:
            if t["owned"] and t["owned"] > t["sh"]:
                si = t["sh"] / (t["owned"] - t["sh"])
                stake_inc = si if stake_inc is None else max(stake_inc, si)
        rets = {}
        for lbl, days in (("r3m", 91), ("r6m", 182), ("r12m", 365)):
            tgt = (d(entry_date) + dt.timedelta(days=days)).isoformat()
            px, _ = at_or_after(pdates, pvals, tgt, maxgap=15)
            rets[lbl] = (px / entry_px - 1) if px else None
            for bname, (bd, bv) in bench.items():
                be, _ = at_or_after(bd, bv, entry_date, maxgap=10)
                bx, _ = at_or_after(bd, bv, tgt, maxgap=15)
                rets[lbl + "_" + bname] = (bx / be - 1) if (be and bx) else None
        events.append({
            "symbol": sym, "month": month, "txdate": txdate, "entry_date": entry_date,
            "value": value, "value_od": value_od, "value_10": value_10,
            "mcap": mcap, "pct_cap": value / mcap * 100,
            "pct_cap_od": value_od / mcap * 100,
            "n_od": sum(1 for t in group if not t["is10"]),
            "n_tx": len(group), "n_insiders": len({t["cik"] for t in group}),
            "stake_inc": stake_inc,
            "ceo_cfo": int(any(("chief executive" in t["who"] or "ceo" in t["who"]
                                or "chief financial" in t["who"] or "cfo" in t["who"]) for t in group)),
            "director_only": int(all("director" in t["who"] and "officer" not in t["who"] for t in group)),
            **rets})

json.dump(events, open(SP + "/data/events2.json", "w"))
print("events:", len(events), "| symbols:", len({e['symbol'] for e in events}), "| skipped:", dict(skipped))
if events:
    with12 = [e for e in events if e["r12m"] is not None]
    print("with 12m return:", len(with12))
    ys = collections.Counter(e["month"][:4] for e in events)
    print("by year:", dict(sorted(ys.items())))
    import statistics as st
    pc = sorted(e["pct_cap"] for e in events)
    qs = [pc[int(q*(len(pc)-1))] for q in (0.1,0.25,0.5,0.75,0.9,0.99)]
    print("pct_cap deciles p10/p25/p50/p75/p90/p99: " + " ".join("%.4f"%q for q in qs))
    vv = sorted(e["value"] for e in events)
    print("value p25/p50/p75: %.0f %.0f %.0f" % (vv[len(vv)//4], vv[len(vv)//2], vv[3*len(vv)//4]))

