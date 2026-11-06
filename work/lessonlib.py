#!/usr/bin/env python3
"""Shared code for the lesson batch files: writes work/topics/<slug>.json."""
import json, re, zlib
ROTATE = False  # batch 5 on: spread correct answers across positions, leaving numeric options in order
M = {m["module_id"]: m for m in json.load(open("work/manifest.json", encoding="utf8"))["modules"]}
FIGS = json.load(open("work/figs/figs.json"))

def build(code, place, passages, concepts, examples, facts, summary, blend, word=None, word_file=None, objectives=None):
    m = M[code]; H = m["handbook"]
    cite = lambda pg: pg if str(pg).startswith(("Word:", "NRC slides", "PSAR")) else f"{H} {code} p.{pg}"
    P = [dict(id=f"P{i+1}", key=k, quote=q, sec=s, cite=cite(pg)) for i, (k, q, s, pg) in enumerate(passages)]
    ids = {p["key"]: p["id"] for p in P}
    def fig(key, alt):
        f = FIGS[key]
        return dict(t="fig", id=key, num=f["num"], cap=f["title"], alt=alt, cite=cite(f["page"]))
    def body(b):
        t = b[0]
        if t == "q": return dict(t="quote", p=ids[b[1]])
        if t == "p": return dict(t="p", text=b[1], cite=cite(b[2]))
        if t == "eq": return dict(t="eq", text=b[1], cite=cite(b[2]))
        if t == "l": return dict(t="list", items=b[1], cite=cite(b[2]))
        if t == "f": return fig(b[1], b[2])
        raise ValueError(t)
    def check(c):
        if "existing" in c: return c
        assert len(c["o"]) == 4 and len(set(c["o"])) == 4, c["q"]
        if ROTATE and not all(re.match(r"[-\d]", o) for o in c["o"]):
            r = zlib.crc32(c["q"].encode()) % 4
            c = dict(c, o=c["o"][-r:] + c["o"][:-r] if r else c["o"], a=(c["a"] + r) % 4)
        return dict(c, p=ids[c["p"]])
    out = dict(module_id=code, slug=m["topic"]["slug"], title=m["title"], status=m["topic"]["status"], scope_tags=(["Draft source"] if any(r["rule"] == "Rule 5" for r in m["scope_review"]) else []) + (["Water-system only"] if any(r["rule"] == "Approved decision" and "Water-system only" in r["note"] for r in m["scope_review"]) else []), source_id=m["source_id"], handbook=H, word_file=word_file,
        quiz_t=place[0], quiz_topic=place[1], objectives=objectives or m["terminal_objectives"], passages=[{k: v for k, v in p.items() if k != "key"} for p in P], word_sequence=[dict(step=w[1], cite=f"Word: {w[2] if len(w) > 2 else word_file}, slide {w[0]}") for w in (word or [])],
        concepts=[dict(title=c["title"], eo=c["eo"], tag=c.get("tag"), body=[body(b) for b in c["body"]], checks=[check(x) for x in c.get("checks", [])]) for c in concepts],
        examples=[dict(e, cite=cite(e["page"]), **({"fig": fig(*e["fig"])} if "fig" in e else {})) for e in examples],
        facts=[dict(q=f[0], a=f[1], p=ids[f[2]], place=f[3] if len(f) > 3 else None) for f in facts],
        summary=[dict(text=t, cite=cite(pg)) for t, pg in summary],
        blend_notes=[dict(type=t, note=n, cite=cite(pg)) for t, n, pg in blend])
    out["page_tags"] = sorted({x["tag"] for x in out["concepts"] + out["examples"] if x.get("tag")})
    json.dump(out, open(f"work/topics/{out['slug']}.json", "w", encoding="utf8"), indent=1, ensure_ascii=False)
    print(out["slug"], len(P), "quotes", sum(len(c["checks"]) for c in out["concepts"]), "checks", len(out["facts"]), "facts")

