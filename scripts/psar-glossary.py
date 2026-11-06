#!/usr/bin/env python3
"""Builds work/psar/glossary/acronyms.json from PSAR Rev 1.

Terms and descriptions come word for word from the PSAR List of Acronyms and Abbreviations.
EXTRA holds the few terms the list omits but the PSAR defines in its text. Each one is checked
against the page it cites, and the build stops if the wording is not there.
"""
import json, re

raw = open("work/text/ML25276A288.txt", errors="ignore").read()
pages = raw.split("\f")
last = max(i for i, p in enumerate(pages) if "Kemmerer Unit 1 PSAR" in p[:400])

# Word for word from the PSAR text: term, description, the phrase that defines it
EXTRA = [
    ("MWt", "megawatt thermal", "megawatt thermal (MWt)"),
    ("MWe", "megawatts electric", "megawatts electric (MWe)"),
    ("VAC", "volts alternating current", "volts alternating current (VAC)"),
    ("NME", "Nuclear Island Major Maintenance Equipment", "Nuclear Island Major Maintenance Equipment (NME)"),
    ("EP", "emergency preparedness", "emergency preparedness (EP)"),
    ("VRLA", "Valve-Regulated Lead-Acid", "Valve-Regulated Lead-Acid (VRLA)"),
    ("ODCM", "Offsite Dose Calculation Manual", "Offsite Dose Calculation Manual (ODCM)"),
    ("HT9", "high chromium martensitic steel", "high chromium martensitic steel (HT9)"),
    ("STS", "static transfer switch", "static transfer switch (STS)"),
]
# Terms with two meanings. The popup uses the first meaning unless the text around the term matches "when".
# Plain "seismic" is not a cue for SSC: seismic design of an SSC still means a structure, system, or component.
CONTEXT = {
    "SSC": dict(default="structure, system, or component",
                alts=[dict(d="Seismic Source Characterization", when=r"seismic source|SSHAC|SSC model|logic tree|earthquake catalog")]),
    "STS": dict(default="static transfer switch",
                alts=[dict(d="Steam Turbine System", when=r"steam|turbine|condenser|feedwater")]),
    "CRS": dict(default="Control Room Supervisor", phrase="approval of the Control Room Supervisor",
                alts=[dict(d="Core Restraint System", when=r"core restraint|load pad|core barrel|core lock-up|core assembl")]),
}


def label(page):
    m = re.search(r"SUBJECT TO DOE COOPERATIVE\s+(\S+)", page)
    return m[1] if m else None


listed = []
for p in pages[: last + 1]:
    if "LIST OF ACRONYMS AND ABBREVIATIONS" not in p:
        continue
    for line in p.split("\n"):
        s = line.rstrip()
        if not s or s.startswith(" ") or re.match(r"(SUBJECT TO|AGREEMENT NO|Copyright|All Rights)", s):
            continue
        m = re.match(r"^(\S(?:.*?\S)?)\s{2,}(\S.*)$", s)
        if not m:
            raise SystemExit("Cannot read list line: " + s)
        listed.append(dict(term=m[1], d=m[2], page=label(p)))

extra = []
for term, d, phrase in EXTRA:
    hit = next((p for p in pages[: last + 1] if phrase in " ".join(p.split()) and label(p)), None)
    if not hit:
        raise SystemExit("Not found in the PSAR: " + phrase)
    extra.append(dict(term=term, d=d, page=label(hit)))

meaning = {(r["term"], r["d"]): r["page"] for r in listed + extra}
context = {}
for term, c in CONTEXT.items():
    page = meaning.get((term, c["default"]))
    if not page:  # Spelled out in the PSAR text, but not abbreviated there
        hit = next(p for p in pages[: last + 1] if c["phrase"] in " ".join(p.split()) and label(p))
        page = label(hit)
    context[term] = dict(d=c["default"], page=page, alts=[dict(a, page=meaning[(term, a["d"])]) for a in c["alts"]])

json.dump(dict(listed=listed, extra=extra, context=context),
          open("work/psar/glossary/acronyms.json", "w"), ensure_ascii=False, indent=1)
print(len(listed), "listed terms,", len(extra), "defined in text:", [(e["term"], e["page"]) for e in extra])
