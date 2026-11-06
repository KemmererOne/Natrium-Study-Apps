{\rtf1\ansi\ansicpg1252\cocoartf2907
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fswiss\fcharset0 Helvetica;}
{\colortbl;\red255\green255\blue255;}
{\*\expandedcolortbl;;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx720\tx1440\tx2160\tx2880\tx3600\tx4320\tx5040\tx5760\tx6480\tx7200\tx7920\tx8640\pardirnatural\partightenfactor0

\f0\fs24 \cf0 # Phone study apps\
\
## Purpose\
Two offline-capable study apps for one user, installed to a phone home screen\
as Progressive Web Apps (PWAs). Subject: fundamentals for a sodium-cooled fast\
reactor (Natrium, Kemmerer Unit 1) and generic NRC operator exam topics.\
\
## Apps\
- flashcards/index.html: flip-card review, filter by category, "Got it" /\
  "Review again" pile, review-missed round. Marks stay on the device in\
  localStorage, stored by card ID. Content is the CARDS array in\
  flashcards/cards.js; each card is [topic, question, answer, source, flag or null, figure or null, id].\
- quiz/index.html: four-choice questions with commit, then correct answer and\
  explanation, then Next. Content is the QS array in quiz/questions.js; each\
  question is \{ id, t: category, topic, q, o: four options, a: correct index,\
  x: explanation, src: source, optional flag, optional fig \}. A figure is\
  \{ f: file in the app's images/, alt, cap, at: "q" or "a" \}.\
\
## Item IDs and feedback\
- Every question (Q1, Q2, ...) and card (C1, C2, ...) stores a permanent ID, shown\
  on the item in the app. Never change or reuse an ID, even if the item is removed.\
  A new item takes the next unused number.\
- Each item has a report link that emails the ID and item details to the address\
  in feedback.js. After changing feedback.js, bump VERSION in both sw.js files.\
\
## Content rules\
- Do not change question or card wording, answer keys, or explanations unless\
  asked. Answer keys were checked against source material, but explanations are\
  drafts. Flag anything that looks wrong; do not silently edit it.\
- Keep the source attribution on each card and question.\
- A flag is a short note shown with the answer when a possible minor\
  discrepancy with the source exists. Do not remove flags unless asked.\
\
## Technical constraints\
- Plain HTML, CSS and JavaScript. No frameworks, no build step, no npm.\
- Each app must work offline after its first load.\
- Keep the Google Fonts links; cache them in the service worker.\
- After editing an app's index.html or content file, bump VERSION in its sw.js\
  so installed copies pick up the change.\
- After editing SOURCES.md or a content file, run node reference/generate.js so\
  the reference page stays in step. Never edit reference/index.html by hand.\
- Layout must work at phone width (about 390 px) with no horizontal scrolling.\
- Support light and dark mode through the existing CSS variables.\
\
## Done means\
- Each app has manifest.webmanifest, icons (192 and 512 px), and sw.js.\
- Each app installs from the phone browser's "Add to Home Screen" option.\
- Each app passes a manual check: flip or answer every item type, switch\
  categories, and reach the end-of-deck screen.\
\
## Lesson Build Rules\
These rules govern the lesson topics in topics/. Do not commit anything until\
the Step 1 manifest is approved.\
\
Inputs\
- sources/DOE-HDBK-10*.pdf: the fundamentals handbooks.\
- sources/*.docx: lesson storyboards. Some are duplicates and some are drafts.\
\
Build steps\
1. Manifest: work/manifest.json holds each handbook module's terminal and\
   enabling objectives, verbatim, with handbook, volume and page; each Word\
   file's section outline, duplicate flag and draft flag; a mapping from each\
   module to its Word files (modules with none are marked "handbook only"); and\
   a topic slug and status for each module (Draft, Reviewed or Approved; new\
   topics start as Draft). Stop and report the manifest for review.\
2. Extract: all source text is in work/text/ (pdftotext -layout for PDFs; the\
   Word text keeps the slide notes that sit in embedded chunks). work/text/ is in\
   .gitignore. Do not commit extracted text. The other lesson working files in work/\
   are committed, so lessons can be rebuilt.\
3. Content, in batches of 5 topics: write work/topics/<slug>.json with\
   objectives, verbatim; handbook passages, each with a verbatim quote and page\
   cite; Word sequence, each step with a slide or section cite; blend notes for\
   conflicts, duplicates and unsupported claims; and scope tags ("Water-system\
   only", "Needs sodium review", "Draft source", or none).\
4. Render: build topics/<slug>/index.html as one HTML file with multiple pages:\
   Objectives, Concepts (one page per concept group), Worked examples, Knowledge\
   checks, Summary and References.\
5. Checks and commit: run scripts/verify-quotes.py; the build fails if any quote\
   is unmatched. Check that every page cites a source and every topic link\
   works. Commit each batch of 5 topics as its own commit, with the landing page\
   and sw.js updated in the same commit. Stop after each batch and report topics\
   built, quotes removed, conflicts found, scope tags applied and open questions.\
\
Citation and source rules\
1. Every factual statement cites a source ID: "DOE-HDBK-1019/2-93 p.X",\
   "Word: <file>, <slide or section>", or both.\
2. Every quoted passage must pass scripts/verify-quotes.py against the extracted\
   text. A quote that fails is removed and logged in work/rejected-quotes.log.\
   Never paraphrase a failed quote into place.\
3. No outside knowledge. Topics with no Word file use handbook content only.\
4. Duplicate Word files: use one as the base and cite both wherever they differ.\
5. Draft Word files: use them, cite them, and mark the topic "Draft source."\
6. Where the handbook and a Word file conflict, report the conflict in the topic\
   JSON. Do not choose one silently.\
7. Unsupported claims in Word files are flagged in the topic JSON and left off\
   the page.\
\
Scope rules\
8. Reactor theory is for a sodium-cooled fast reactor with no moderator. Exclude\
   thermal-spectrum content: thermal utilization, resonance escape, thermal-flux\
   models and moderator-based examples. Keep a fast-spectrum equivalent only if\
   a cited source supports it. Otherwise tag the item "Needs sodium review."\
9. All other fundamentals apply to the sodium and salt systems.\
10. Water-specific material may be used only in topics about water heat\
    transfer, tagged "Water-system only." It must never appear on sodium or salt\
    pages.\
11. Gap topics (material science, engineering prints, classical physics, diesel\
    and miscellaneous mechanical components) use handbook content only.\
\
Rendering rules\
- Use the same styles and phone layout as the existing apps. No external CDN,\
  all CSS and JS inline.\
- Every page has a visible link back to the main landing page.\
- Each statement shows its citation inline.\
- Insert knowledge checks after the section that teaches the objective, not all\
  at the end.\
- Show a "Draft source" or scope tag on the page where it applies.\
\
Knowledge checks and question export\
- Each knowledge check has one correct answer, distractors, an explanation and a\
  source cite.\
- Export each check to quiz/questions.js and each key fact to flashcards/cards.js.\
  Each item gets a src field and a topic field.\
- Do not duplicate items already in the quiz or flashcard files. Check by\
  question text.\
\
Launch and navigation\
- The main index.html is the single landing page, with a Fundamentals Lesson Plans button\
  and a PSAR Lesson Plans button, like the Flashcards and Quiz buttons. The first opens\
  lessons/index.html and the second opens psar/index.html.\
- lessons/index.html lets the user pick a plan from a drop selector, grouped under\
  the handbook headings. Each option shows its status, and the chosen plan shows its\
  title, handbook volume, status and a start button.\
- Topics marked Draft, or with open scope tags, show that status in the selector.\
- A "References" link goes to reference/index.html, which lists every source used\
  across all topics, with its file name and page or slide list.\
- Add all new topic URLs to sw.js and bump the cache version.\
- Generate the selector from the manifest, so no topic appears without its page.\
  Topics not yet built show as "In progress" and cannot be selected.\
- Lesson progress stays on the device in localStorage (natrium-lessons-progress), stored by\
  topic slug. Last page is saved automatically. Completed is marked by the user.\
- Screen layout uses CSS width (900 px and up), not device or browser detection. Wide screens\
  get the side page list and the full lesson list. Phones keep the single column and selector.\
\
Approved decisions (Step 1 review, Nov 5, 2026)\
- CH-03 and CH-04 are built, tagged "Water-system only."\
- Cold Traps, Plugging Temperature Indicators and Sodium Leak Detectors each get\
  an added sodium topic (NA-01 to NA-03). Variable Frequency Drives supports ES-12.\
- Fast-spectrum equivalents may also cite the NRC fast reactor training slides and\
  the PSAR, both listed in SOURCES.md.\
- Thermal or moderator objectives stay verbatim, tagged "Needs sodium review."\
- Root sw.js covers the landing page, reference page and topics/. It leaves\
  flashcards/ and quiz/ to their own service workers.\
- Topic pages load no web fonts; they use the existing fallback font stacks.\
- Content in slide pictures is not used. Check any quote with an exponent against\
  the source, because extraction flattens exponents.\
- A knowledge check already in the quiz is reused by its ID, not copied.\
- Water in battery chemistry (ES-04) is normal and takes no scope tag. Rule 10 is for\
  water-system material.\
- Lessons include handbook figures, embedded in the page as images so each lesson\
  stays one file. Each figure has alt text and a page citation.\
\
Batch 5 decisions (Nov 5, 2026)\
- Water-system only can be a page tag. Steam, boiling, two-phase flow, steam hammer and\
  flow oscillation pages carry it inside HT-01 to HT-03. Generic examples that merely use\
  water as the fluid stay untagged.\
- Worked examples and checks tied to PWR or BWR reactor coolant systems are left out,\
  including PWR natural circulation checks. Sodium indications are used instead.\
- Decay heat right after shutdown is the handbook's 7%. The Word file's 6% is not shown.\
- Objective sub-items show their letters only, with no bullets.\
\
Batch 8 decisions (Nov 5, 2026)\
- PR-03 Figure 13 stays off the page. PR-04 Figure 15 stays on the page.\
- Open questions are collected in work/open-questions.md and taken up together when all\
  batches are done. Each batch report still lists what it added.\
\
Batch 9 decisions (Nov 5, 2026)\
- MS-03 and MS-04 teach the general vessel material only. PWR-specific items (pressurizer\
  spray line, ECCS injection, cold makeup water) stay off the pages. Objectives stay\
  verbatim, and any objective that cannot be fully taught is tagged Needs sodium review.\
- The MS-04 minimum pressurization-temperature section uses the handbook's general text\
  without Figures 4 and 5, and its page is tagged Needs sodium review.\
\
Batch 11 decisions (Nov 5, 2026)\
- Prompt neutron release time uses the handbook's 10^-13 seconds. The Word file's 10^-14 seconds is not shown.\
- NP-04 shows no starting decay heat value, only less than 1% at one hour. The 5 to 6% and 7% question is held in\
  work/open-questions.md.\
\
Batch 12 decisions (Nov 5, 2026)\
- NA-03 Sodium Leak Detectors also uses the NRC training slides and the PSAR, because its Word file has\
  only two knowledge checks in text. Its ammeter check stays off, since the question text is missing.\
- NA-01 shows the RVC filter range of 350 to 550 F from slide 1.28. The other range on slide 1.29 is held in\
  archive/unresolved-items.md.\
\
Open question decisions (Nov 5, 2026)\
- Decay heat right after shutdown is 7% everywhere (HT-02). NP-04 stays silent on the starting value, and Q56 is\
  flagged, not changed.\
- Q303, Q304 and Q467 to Q474 are retired from the quiz. Their IDs are never reused.\
- PSAR statements may supplement NA-02 and MS-05 pages.\
- Word file errors go to the lesson plan owner list in archive/unresolved-items.md. Lessons stay as built.\
\
Audit decisions (Nov 6, 2026)\
- DOE handbooks are the primary source, and the PSAR is also reputable. For fundamentals, a handbook beats a Word\
  file on any conflict. PSAR items follow the PSAR strictly.\
- No ECI: nothing about the Natrium design may come from a Word lesson plan. Plant design facts cite the PSAR or stay off.\
- Reactor theory items use no thermal neutron or moderator information. Retired items are listed in\
  archive/audit-2026-11.md. Their IDs are never reused.\
- All lessons are status Reviewed, not Draft. Draft source tags stay where a Word source is itself a draft.\
\
PSAR lesson plans (Nov 6, 2026)\
- psar/ holds 43 lessons written from scratch as introductory information, not for NRC exam preparation. Only PSAR Rev 1 is used\
  (work/text/ML25276A288.txt, PSAR pages only). No Word file, handbook or outside content.\
- Systems use the ten standard objectives and design basis events use the twelve event objectives.\
  Where the PSAR cannot teach an objective, the lesson says so. It does not fill the gap.\
- Lessons are written in work/psar/src/*.txt. Run python3 scripts/psar-author.py, then the normal\
  lesson build. Never edit psar/ pages by hand. Quotes and statement anchors must match the PSAR.\
- Progress shares natrium-lessons-progress, with slugs starting psar-. Root sw.js also covers psar/.\
- The Natrium control rod count may be shown with its PSAR cite: nine primary and four secondary assemblies\
  (Secs. 1.1.4.1.9, 7.1.1.3.1, 7.2.5.1). This replaces the Nov 5 decision that kept the count off.\
- PSAR lesson checks export to quiz/questions.js with t "PSAR design basis" and a "PSAR: group" topic. PSAR key facts\
  are not exported to the flashcards.\
\
PSAR acronym popups (Nov 6, 2026)\
- PSAR lessons, PSAR flashcards and PSAR quiz questions underline each PSAR acronym. Hover, tap or Enter shows its\
  description and PSAR page. Fundamentals items are not tagged. psar/acronyms/ lists every term with a search box.\
- Terms and descriptions are word for word from the PSAR List of Acronyms and Abbreviations (pp. iv to xvii). Terms the\
  list omits but the PSAR text defines are in EXTRA in scripts/psar-glossary.py, each checked against its page.\
- SSC, STS and CRS popups follow context. SSC is structure, system, or component, or Seismic Source Characterization in\
  seismic source material. Plain seismic is not a cue. STS is static transfer switch, or Steam Turbine System in steam\
  material. CRS is Control Room Supervisor, or Core Restraint System in core material. Rules are in CONTEXT in\
  scripts/psar-glossary.py. The PSAR spells out Control Room Supervisor but does not abbreviate it.\
- Abbreviations the PSAR does not define are left alone. Codes such as RRS-ISPL-BL are not tagged.\
- A term spelled out in a question or choice, or in a card's answer, stays plain until the student answers or flips.\
- Run python3 scripts/psar-glossary.py, then the lesson build. The build writes glossary.js, which the quiz and flashcards\
  load, and bumps their sw.js versions when it changes. Lessons carry their own terms inline. Never edit glossary.js by hand.\
\
Device sync (Nov 6, 2026)\
- Flashcard marks and lesson progress can sync across a user's devices under a private 16-character code, with no\
  account, name or email. Quiz results are still not kept. Sync is off until the user turns it on.\
- sync.js is the client, and scripts/sync-worker.js is the Cloudflare Worker with one KV namespace bound as SYNC. Set\
  SYNC_URL in sync.js to the Worker address. While it is empty, sync stays hidden.\
- The apps still save to localStorage. sync.js finds changes, gives each item a time, and the latest change wins.\
- The landing page and the flashcards app each show the sync box, because a phone may keep installed apps' data apart.\
- The lesson build copies sync.js into each lesson. Plan pages, the landing page and flashcards load it as a file.\
- After changing sync.js, run the lesson build and bump VERSION in flashcards/sw.js.\
- Test with node scripts/test-sync.js. The preview "sync" runs the Worker locally for localhost pages.\
\
Page checkmarks (Nov 6, 2026)\
- A lesson page gets a checkmark when the user moves on with Next. A knowledge check page gets one when every check on it\
  is answered. The last page gets one when opened. A lesson marked complete shows every page checked.\
- Each finished page is an entry "<slug>.<page id>" with a done date in natrium-lessons-progress, stored like a lesson, so\
  sync.js and the Worker need no change. Code that counts lessons must skip keys containing a dot.\
- A lesson opened with no page named resumes at the last page unless complete. If another device moved on while a lesson\
  sat open, the lesson offers that page and does not jump.\
\
PSAR notice and shuffled checks (Nov 6, 2026)\
- scripts/psar-notice.js holds the notice that PSAR Rev 1 is the public NRC version and that this is introductory information,\
  not for use in NRC exam preparation. It shows on the PSAR plans page, each PSAR lesson's References page and reference/.\
- Lesson knowledge check choices shuffle each time a lesson opens, as the quiz does. Answer keys in the data do not change.\
\
Stop and report, do not guess, if:\
- A source file is missing or unreadable.\
- A Word file cannot be parsed.\
- A handbook and a Word file conflict on a value.\
- A topic needs a scope decision that these rules don't cover.}