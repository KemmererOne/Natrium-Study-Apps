#!/usr/bin/env python3
"""Check every lesson quote and citation in work/topics/*.json against the extracted source text.

  python3 scripts/verify-quotes.py            report; exit 1 if anything fails
  python3 scripts/verify-quotes.py --remove   also remove failed quotes and log them

A quote must appear on the page it cites. A cite must name a real page, and every
statement block must have one. Failed quotes go to work/rejected-quotes.log."""
import glob, json, os, re, sys, unicodedata, datetime

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
os.chdir(ROOT)
MANIFEST = json.load(open("work/manifest.json", encoding="utf8"))
FILES = {m["handbook"]: m["file"] for m in MANIFEST["modules"] if m["handbook"]}
FOOT = re.compile(r"(?:Rev\.\s*\d*\s+Page\s+(\S+)\s+([A-Z]{2,3}-\d+)|([A-Z]{2,3}-\d+)\s+Page\s+(\S+)\s+Rev\.\s*\d+)")
CITE = re.compile(r"^(DOE-HDBK-\d+(?:/\d)?-\d+) ([A-Z]{2}-\d\d) p\.(\S+)$")
WORD = re.compile(r"^Word: (.+\.docx), (.+)$")
SLIDE = re.compile(r"^NRC slides (ML\d+A\d+), slide (\d+)$")
PSAR = re.compile(r"^PSAR Rev 1, ML25276A288, Sec\. [\d.]+, p\. (\d+\.\d+-\d+)$")

def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), ("­", "")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip().lower()

pages = {}
def book(designation):
    if designation not in pages:
        name = FILES[designation][:-4]
        raw = open(f"work/text/{name}.txt", errors="replace").read().split("\f")
        index = {}
        for i, p in enumerate(raw):
            for m in FOOT.finditer(p):
                index[((m[2] or m[3]), (m[1] or m[4]))] = i
        pages[designation] = ([norm(p) for p in raw], index)
    return pages[designation]

word = {}
def word_text(file):
    if file not in word:
        word[file] = norm(open(f"work/text/{file[:-5]}.txt", errors="replace").read())
    return word[file]

def word_slide(file, where):
    """The text of one slide, including its layers, or None if the slide is not in the file."""
    lines = open(f"work/text/{file[:-5]}.txt", errors="replace").read().splitlines()
    head = "# " + where.removeprefix("slide ")
    start = next((i for i, l in enumerate(lines) if norm(l) == norm(head)), None)
    if start is None: return None
    end = next((i for i in range(start + 1, len(lines)) if re.match(r"# \d", lines[i])), len(lines))
    return norm(" ".join(lines[start:end]))

def check_cite(cite):
    """Return the text to search for a cite, or None if the cite is not a real location."""
    m = CITE.match(cite or "")
    if m:
        if m[1] not in FILES: return None
        text, index = book(m[1])
        i = index.get((m[2], m[3]))
        if i is None: return None
        return text[i] + " " + (text[i + 1] if i + 1 < len(text) else "")
    n = SLIDE.match(cite or "")
    if n and os.path.exists(f"work/text/{n[1]}.txt"):
        raw = open(f"work/text/{n[1]}.txt", errors="replace").read().split("\f")
        return norm(raw[int(n[2]) - 1]) if int(n[2]) <= len(raw) else None
    s = PSAR.match(cite or "")
    if s:
        raw = open("work/text/ML25276A288.txt", errors="replace").read().split("\f")
        return next((norm(p) for p in raw if re.search(r"SUBJECT TO DOE.*?\s" + re.escape(s[1]) + r"\s", p)), None)
    w = WORD.match(cite or "")
    if w and os.path.exists(f"work/text/{w[1][:-5]}.txt"):
        return word_slide(w[1], w[2])
    return None

def walk(node, path, out):
    if isinstance(node, dict):
        if node.get("t") in ("p", "eq", "list", "fig") or "problem" in node or path.endswith("summary") or path.endswith("blend_notes") or path.endswith("word_sequence"):
            out.append((path, node))
        for k, v in node.items(): walk(v, path + "." + k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, path if not isinstance(v, dict) else path, out)

failed = bad_cites = quotes = cites = figures = 0
log = []
remove = "--remove" in sys.argv
for path in sorted(glob.glob("work/topics/*.json")):
    topic = json.load(open(path, encoding="utf8"))
    name = os.path.basename(path)
    keep = []
    for p in topic["passages"]:
        quotes += 1
        text = check_cite(p["cite"])
        if text is None or norm(p["quote"]) not in text:
            failed += 1
            why = "bad cite" if text is None else "quote not on cited page"
            print(f"FAIL {name} {p['id']}: {why}: {p['cite']}: {p['quote'][:80]}")
            log.append(f"{datetime.date.today()} {name} {p['id']} {why} | {p['cite']} | {p['quote']}")
        else:
            keep.append(p)
    statements = []
    walk({k: v for k, v in topic.items() if k in ("concepts", "examples", "summary", "blend_notes", "word_sequence")}, "topic", statements)
    for where, node in statements:
        cites += 1
        if check_cite(node.get("cite")) is None:
            bad_cites += 1
            print(f"NO VALID CITE {name} {where}: {node.get('cite')}: {str(node.get('text') or node.get('problem') or node.get('step'))[:70]}")
        elif node.get("t") == "fig":
            figures += 1
            label = norm(f"Figure {node['num']}")
            if label not in check_cite(node["cite"]) or not node.get("alt") or not os.path.exists(f"work/figs/{node['id']}.png"):
                bad_cites += 1
                print(f"BAD FIGURE {name} {node['id']}: caption not on cited page, no alt text, or no image")
    if remove and len(keep) != len(topic["passages"]):
        ids = {p["id"] for p in keep}
        topic["passages"] = keep
        for c in topic["concepts"]:
            c["body"] = [b for b in c["body"] if b.get("t") != "quote" or b["p"] in ids]
        json.dump(topic, open(path, "w", encoding="utf8"), indent=1, ensure_ascii=False)
if log:
    with open("work/rejected-quotes.log", "a", encoding="utf8") as f:
        f.write("\n".join(log) + "\n")
print(f"{quotes} quotes checked, {failed} failed. {cites} statement cites checked, including {figures} figures, {bad_cites} failed.")
sys.exit(1 if failed or bad_cites else 0)
