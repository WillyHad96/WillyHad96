#!/usr/bin/env python3
"""Move persisted MCP tool-result files into data/{kind}/{SYMBOL}.json, merging insider pages."""
import json, glob, os

TOOLDIR = "/root/.claude/projects/-home-user-WillyHad96/1981e284-84b3-5ae2-912a-581463ab2224/tool-results"
SP = "/tmp/claude-0/-home-user-WillyHad96/1981e284-84b3-5ae2-912a-581463ab2224/scratchpad"

def load(path):
    try:
        raw = open(path).read()
        d = json.loads(raw)
    except Exception:
        return None
    if isinstance(d, list) and len(d) == 1 and isinstance(d[0], dict) and set(d[0].keys()) == {"type", "text"}:
        try:
            d = json.loads(d[0]["text"])
        except Exception:
            return None
    return d if isinstance(d, list) and d and isinstance(d[0], dict) else None

def kind_of(rec):
    k = set(rec.keys())
    if "transactionType" in k: return "insider"
    if "marketCap" in k: return "mcap"
    if "adjClose" in k: return "price"
    if "price" in k and "date" in k: return "price"
    return None

def key(r):
    return (r.get("url"), r.get("transactionDate"), r.get("reportingCik"),
            r.get("securitiesTransacted"), r.get("price"), r.get("transactionType"),
            r.get("securitiesOwned"), r.get("securityName"))

moved = skipped = frame_n = 0
for f in sorted(glob.glob(os.path.join(TOOLDIR, "*"))):
    d = load(f)
    if d is None:
        skipped += 1; continue
    kind = kind_of(d[0])
    if kind is None:
        skipped += 1; continue
    syms = {r.get("symbol") for r in d if r.get("symbol")}
    if kind == "insider" and len(syms) > 1:
        dest = os.path.join(SP, "data", "frame", "page_%s.json" % os.path.basename(f).split("-")[-1].split(".")[0])
        json.dump(d, open(dest, "w")); os.remove(f); frame_n += 1; moved += 1; continue
    if len(syms) != 1:
        skipped += 1; continue
    sym = syms.pop().replace("/", "_")
    dest = os.path.join(SP, "data", kind, "%s.json" % sym)
    if kind == "insider" and os.path.exists(dest):
        old = json.load(open(dest))
        seen = {key(r) for r in old}
        merged = old + [r for r in d if key(r) not in seen]
        json.dump(merged, open(dest, "w"))
    else:
        json.dump(d, open(dest, "w"))
    os.remove(f); moved += 1

print("moved=%d frame_pages=%d skipped=%d" % (moved, frame_n, skipped))
for k in ("insider", "price", "mcap"):
    print("  %-8s %d files" % (k, len(glob.glob(os.path.join(SP, "data", k, "*.json")))))

