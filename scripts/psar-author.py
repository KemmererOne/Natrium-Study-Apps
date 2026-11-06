#!/usr/bin/env python3
"""Compile the PSAR lesson sources in work/psar/src/*.txt into work/psar/<slug>.json.

Every statement carries an anchor: words copied exactly from PSAR Rev 1. The tool finds the
anchor inside the lesson's page range and writes the section and page cite from that spot,
so a cite cannot be typed wrong. Anything not found stops the build.

Source format, one item per line (blank lines and lines starting with ; are skipped):
  # id | title | kind (system, event, topic) | subject
  range: 7.1-50 7.1-74          page ranges to search, as first and last page labels
  sec: Sec. 7.1.3, pp. 7.1-50 to 7.1-74   the lesson's PSAR citation
  intro: one sentence for the Objectives page
  obj: extra objective text      topic lessons list their own objectives
  == Page title | 1,4            a page, and the objective numbers it teaches
  S statement @@ anchor          a cited statement
  Q verbatim quote               a quoted passage
  L item ;; item ;; item @@ anchor
  T head | head | head           a table; rows follow
  R cell | cell | cell @@ anchor
  N note                         a study note that states no plant fact
  F 7.1.3-1                      a PSAR figure
  K question | A | B | C | D | index of answer, 0 to 3 | explanation @@ anchor
  Z statement @@ anchor          a line in the Summary page
"""
import glob, json, os, re, struct, subprocess, sys, unicodedata, zlib
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
os.chdir(ROOT)
PDF = "sources/ML25276A288.pdf"
BODY_END = 1764                      # the Core Design report bound in after this page is not the PSAR

def norm(s):
    s = unicodedata.normalize("NFKC", s)
    for a, b in (("’", "'"), ("‘", "'"), ("“", '"'), ("”", '"'), ("–", "-"), ("—", "-"), ("­", "")):
        s = s.replace(a, b)
    return re.sub(r"\s+", " ", s).strip().lower()

raw = open("work/text/ML25276A288.txt", errors="replace").read().split("\f")[:BODY_END]
label = {}
for i, p in enumerate(raw):
    m = re.search(r"SUBJECT TO DOE.*?\s(\d+\.\d+-\d+)\s", p)
    if m: label[i] = m[1]
index = {v: k for k, v in reversed(list(label.items()))}
text = {i: norm(raw[i]) for i in label}
HEAD = re.compile(r"^\s*(\d{1,2}(?:\.\d+){1,5})\s+[A-Z(]")
# Section headings in page order. A heading must sit in the page's own chapter section.
heads = {}
current = None
for i in sorted(label):
    prefix = label[i].split("-")[0]
    out, pos = [], 0
    for line in raw[i].splitlines():
        m = HEAD.match(line)
        if m and (m[1] == prefix or m[1].startswith(prefix + ".")) and not re.search(r"\.{4}|\. \. \.", line):
            at = text[i].find(norm(line), pos)
            if at >= 0:
                out.append((at, m[1])); pos = at
    heads[i] = out

def section_at(i, at):
    for j in range(i, min(label) - 1, -1):
        if j not in heads: continue
        hits = [s for a, s in heads[j] if j < i or a <= at]
        if hits: return hits[-1]
    return label[i].split("-")[0]

def locate(anchor, pages):
    n = norm(anchor)
    for i in pages:
        at = text[i].find(n)
        if at >= 0:
            return f"PSAR Rev 1, ML25276A288, Sec. {section_at(i, at)}, p. {label[i]}"
    return None

def fig_page(num, pages):
    want = re.compile(r"(?m)^\s*Figure\s+" + re.escape(num) + r"\s+(.+)$")
    for i in pages:
        m = want.search(raw[i])
        # A caption starts with a capital. A lowercase start is a body sentence that cites the figure.
        if m and m[1][0].isupper() and not re.search(r"\. \. \.", m[1]):
            return i, " ".join(m[1].split())
    return None, None

def read_gray(path):
    """Read a binary PGM file into a list of row bytes."""
    data = open(path, "rb").read()
    m = re.match(rb"P5\s+(\d+)\s+(\d+)\s+(\d+)\s", data)
    w, h, at = int(m[1]), int(m[2]), m.end()
    return [data[at + y * w:at + (y + 1) * w] for y in range(h)]

def write_gray4(path, rows):
    """Write rows as a 4-bit gray PNG: small, and plenty for line drawings."""
    w, h = len(rows[0]), len(rows)
    packed = bytearray()
    for r in rows:
        packed.append(0)
        q = bytes(v >> 4 for v in r) + (b"\0" if w % 2 else b"")
        packed += bytes((q[i] << 4) | q[i + 1] for i in range(0, len(q), 2))
    def chunk(k, d): return struct.pack(">I", len(d)) + k + d + struct.pack(">I", zlib.crc32(k + d))
    open(path, "wb").write(b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB", w, h, 4, 0, 0, 0, 0)) + chunk(b"IDAT", zlib.compress(bytes(packed), 9)) + chunk(b"IEND", b""))

def render(num, i):
    """Render a figure page, then cut the margins, running header and footer."""
    fid = "psar-fig-" + num.replace(".", "-").lower()
    out = f"work/figs/{fid}.png"
    if os.path.exists(out): return fid
    tmp = out[:-4] + "-page"
    subprocess.run(["pdftoppm", "-gray", "-r", "110", "-f", str(i + 1), "-l", str(i + 1), "-singlefile", PDF, tmp], check=True)
    rows = read_gray(tmp + ".pgm")
    os.remove(tmp + ".pgm")
    dark = [sum(1 for v in r[::3] if v < 200) * 3 for r in rows]
    ink = [y for y, d in enumerate(dark) if d]
    top, bottom = ink[0], ink[-1]
    span = bottom - top
    # The header and the footer each sit behind a full-width rule
    widest = max(dark)
    rules = [y for y in range(top, bottom + 1) if dark[y] > 0.6 * widest and dark[y] > 300]
    up = [y for y in rules if y < top + 0.14 * span]
    down = [y for y in rules if y > bottom - 0.16 * span]
    if up: top = up[-1] + 2
    else: top = top + int(0.03 * span)
    # Footer text starts at SUBJECT TO DOE; with no rule, cut the last 7 percent
    bottom = down[0] - 2 if down else bottom - int(0.07 * span)
    rows = rows[top:bottom]
    cols = [x for x in range(len(rows[0])) if any(r[x] < 200 for r in rows[::4])]
    left, right = max(cols[0] - 6, 0), cols[-1] + 6
    ink = [y for y, r in enumerate(rows) if min(r) < 200]
    rows = [r[left:right] for r in rows[max(ink[0] - 6, 0):ink[-1] + 6]]
    write_gray4(out, rows)
    return fid

SYSTEM = ["State the purpose of the {s}.", "Identify the {s} boundaries and interfaces.", "Identify the major components of the {s}.",
          "Explain {s} operation.", "Describe the {s} controls and indications.", "Explain the {s} automatic features and interlocks.",
          "Apply operating procedures for the {s}.", "Diagnose abnormal conditions in the {s}.", "Explain the safety significance of the {s}.",
          "Address technical specifications and administrative controls for the {s}."]
EVENT = ["State the event initiator and safety-analysis assumptions.", "Identify the challenged safety functions and acceptance criteria.",
         "Describe the event chronology.", "Predict key parameter trends.", "Identify automatic protective actions.",
         "Recognize the event from alarms and indications.", "Select and apply the appropriate procedure.", "Verify operation of credited equipment.",
         "Respond to failure of an automatic or mitigating function.", "Establish and verify the required end state.",
         "Explain the consequences of delayed or incorrect actions.", "Relate operator actions to the event's technical basis."]

def compile_file(path):
    errs = []
    lesson = dict(concepts=[], summary=[], passages=[], examples=[], word_sequence=[], blend_notes=[], facts=[], status="Draft")
    pages, objs, page, table = [], [], None, None
    def where(anchor, n):
        c = locate(anchor, pages)
        if c is None: errs.append(f"{os.path.basename(path)}:{n}: not found: {anchor[:90]}")
        return c
    for n, line in enumerate(open(path, encoding="utf8"), 1):
        line = line.strip()
        if not line or line.startswith(";"): continue
        code, _, rest = line.partition(" ")
        rest = rest.strip()
        body, _, anchor = rest.partition(" @@ ")
        anchor = anchor.strip()
        if code == "#":
            lesson["id"], lesson["title"], lesson["kind"], lesson["subject"] = [x.strip() for x in rest.split("|")]
        elif code == "range:":
            parts = rest.split()
            for a, b in zip(parts[::2], parts[1::2]):
                if a not in index or b not in index: errs.append(f"{path}:{n}: no page {a} or {b}"); continue
                pages += [i for i in range(index[a], index[b] + 1) if i in label]
        elif code == "intro:": lesson["intro"] = rest
        elif code == "sec:": lesson["sec_note"] = rest
        elif code == "obj:": objs.append(rest)
        elif code == "==":
            title, _, eo = rest.partition("|")
            page = dict(title=title.strip(), eo=[e.strip() for e in eo.split(",") if e.strip()], tag=None, body=[], checks=[])
            lesson["concepts"].append(page); table = None
        elif code == "S":
            page["body"].append(dict(t="p", text=body, anchor=anchor, cite=where(anchor, n)))
        elif code == "Q":
            c = where(rest, n)
            pid = f"P{len(lesson['passages']) + 1}"
            lesson["passages"].append(dict(id=pid, quote=rest, sec=(c or "").split(", ")[2] if c else "", cite=c))
            page["body"].append(dict(t="quote", p=pid))
        elif code == "L":
            page["body"].append(dict(t="list", items=[x.strip() for x in body.split(";;")], anchor=anchor, cite=where(anchor, n)))
        elif code == "T":
            table = dict(t="table", head=[x.strip() for x in rest.split("|")], rows=[])
            page["body"].append(table)
        elif code == "R":
            cells = [x.strip() for x in body.split("|")]
            if len(cells) != len(table["head"]): errs.append(f"{path}:{n}: row has {len(cells)} cells")
            table["rows"].append(dict(cells=cells, anchor=anchor, cite=where(anchor, n)))
        elif code == "N":
            page["body"].append(dict(t="note", text=rest))
        elif code == "F":
            i, cap = fig_page(rest, pages)
            if i is None: errs.append(f"{path}:{n}: no figure {rest}"); continue
            page["body"].append(dict(t="fig", id=render(rest, i), num=rest, cap=cap, alt=f"PSAR Rev 1 figure: {cap}",
                                     cite=f"PSAR Rev 1, ML25276A288, Sec. {section_at(i, 0)}, p. {label[i]}"))
        elif code == "K":
            f = [x.strip() for x in body.split(" | ")]
            if len(f) != 7 or f[5] not in "0123": errs.append(f"{path}:{n}: bad check"); continue
            opts, ans = f[1:5], int(f[5])
            # Spread correct answers over all four positions. A fixed turn per question keeps builds stable;
            # numeric option lists stay in the written order.
            if not all(o[0].isdigit() for o in opts):
                turn = zlib.crc32(f[0].encode()) % 4
                opts, ans = opts[-turn:] + opts[:-turn] if turn else opts, (ans + turn) % 4
            page["checks"].append(dict(q=f[0], o=opts, a=ans, x=f[6], anchor=anchor, cite=where(anchor, n), eo=",".join(page["eo"])))
        elif code == "Z":
            lesson["summary"].append(dict(text=body, anchor=anchor, cite=where(anchor, n)))
        else:
            errs.append(f"{path}:{n}: unknown line: {line[:50]}")
    kind, s = lesson["kind"], lesson["subject"]
    bank = SYSTEM if kind == "system" else EVENT if kind == "event" else objs
    taught = {e for c in lesson["concepts"] for e in c["eo"]}
    lesson["objectives"] = [dict(number=str(i + 1), text=o.replace("{s}", s), taught=str(i + 1) in taught) for i, o in enumerate(bank)]
    lesson["slug"] = "psar-" + lesson["id"].lower() + "-" + re.sub(r"[^a-z0-9]+", "-", lesson["title"].lower()).strip("-")
    for e in sorted(taught - {o["number"] for o in lesson["objectives"]}):
        errs.append(f"{path}: page teaches unknown objective {e}")
    return lesson, errs

def main():
    want = sys.argv[1:]
    bad = 0
    for path in sorted(glob.glob("work/psar/src/*.txt")):
        if want and not any(w in path for w in want): continue
        lesson, errs = compile_file(path)
        for e in errs: print(e)
        bad += len(errs)
        if not errs:
            old = glob.glob(f"work/psar/{lesson['id'].lower()}.json")
            json.dump(lesson, open(f"work/psar/{lesson['id'].lower()}.json", "w", encoding="utf8"), indent=1, ensure_ascii=False)
            n = sum(len(c["body"]) for c in lesson["concepts"]); k = sum(len(c["checks"]) for c in lesson["concepts"])
            print(f"ok {lesson['id']} {lesson['title']}: {len(lesson['concepts'])} pages, {n} blocks, {k} checks, gaps {[o['number'] for o in lesson['objectives'] if not o['taught']]}")
    sys.exit(1 if bad else 0)
if __name__ == "__main__": main()
