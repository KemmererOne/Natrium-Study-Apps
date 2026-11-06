// Shows what PSAR acronyms mean. Each one gets a dotted underline. Hover, tap or press Enter on it
// to open a small popup with the PSAR's description and page. Used by the PSAR lessons, flashcards and quiz.
(function () {
  const T = window.PSAR_TERMS || {}, MORE = window.PSAR_TERMS_PAGE;
  const SKIP = ".term,a,cite,script,style,h1,.count,.meta,.tags,.top,.pager,.verdict,.letter";
  const find = w => T[w] ? w : w.endsWith("s") && T[w.slice(0, -1)] ? w.slice(0, -1) : null;
  const isLine = w => /^DL\d/.test(w) && T.DL;

  // Finds the terms in a string as [start, end, term]. Codes such as RRS-ISPL-BL or DHP-LOOP-4
  // are names of their own, so a listed term inside one is left alone. DL3 is Defense Line 3.
  function spans(text) {
    const out = [];
    for (const m of text.matchAll(/[A-Za-z0-9&]+(?:[-/][A-Za-z0-9&]+)*/g)) {
      const hit = find(m[0]);
      if (hit) { out.push([m.index, m.index + m[0].length, hit]); continue; }
      let at = m.index;
      for (const piece of m[0].split("/")) {
        const whole = find(piece);
        if (whole) out.push([at, at + piece.length, whole]);
        else {
          const parts = piece.split("-");
          const code = parts.some(p => /^[A-Z0-9]/.test(p) && !find(p) && !isLine(p));
          let pos = at;
          parts.forEach((p, i) => {
            if (isLine(p) && (i === 0 || !code)) out.push([pos, pos + p.replace(/^(DL\d+).*$/, "$1").length, "DL"]);
            else if (!code && find(p)) out.push([pos, pos + p.length, find(p)]);
            pos += p.length + 1;
          });
        }
        at += piece.length + 1;
      }
    }
    return out;
  }

  // Some terms have two meanings. The words around the term, and the rest of its question or card, pick one.
  function meaning(term, text) {
    const [d, page, alts] = T[term];
    const alt = (alts || []).find(a => new RegExp(a[2], "i").test(text));
    return alt ? [alt[0], alt[1]] : [d, page];
  }
  const around = node => {
    const block = node.parentElement.closest("li,p,td,tr,blockquote,figcaption,.check");
    return block ? block.textContent : node.nodeValue;
  };

  function tag(root, opt) {
    if (!root) return;
    const hide = opt && opt.hide, context = opt && opt.context || "", nodes = [];
    const walk = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
    while (walk.nextNode()) if (walk.currentNode.nodeValue.trim() && !walk.currentNode.parentElement.closest(SKIP)) nodes.push(walk.currentNode);
    for (const node of nodes) {
      const text = node.nodeValue, found = spans(text).filter(s => !hide || !hide.has(s[2]));
      if (!found.length) continue;
      const frag = document.createDocumentFragment(), near = context + " " + around(node);
      let at = 0;
      for (const [a, b, term] of found) {
        frag.append(text.slice(at, a));
        const el = document.createElement("abbr");
        el.className = "term";
        el.dataset.t = term;
        el.textContent = text.slice(a, b);
        const [d, page] = meaning(term, near);
        el.dataset.d = d;
        el.dataset.p = page;
        el.setAttribute("aria-label", text.slice(a, b) + ", " + d);
        if (!node.parentElement.closest("button")) el.tabIndex = 0;
        frag.append(el);
        at = b;
      }
      frag.append(text.slice(at));
      node.replaceWith(frag);
    }
  }

  // Terms that would give an answer away: the description is written out in the question or a choice
  function spoilers(strings) {
    const all = strings.join("\n").toLowerCase();
    return new Set(Object.keys(T).filter(t => [T[t][0], ...(T[t][2] || []).map(a => a[0])].some(d => all.includes(d.toLowerCase()))));
  }

  const style = document.createElement("style");
  style.textContent = `
abbr.term { text-decoration: underline dotted var(--accent, #8a5f00); text-decoration-thickness: 1.5px; text-underline-offset: 3px; cursor: help; }
abbr.term:focus-visible { outline: 2px solid var(--accent, #8a5f00); outline-offset: 1px; border-radius: 2px; }
#term-pop { position: fixed; z-index: 1000; box-sizing: border-box; width: max-content; max-width: min(320px, calc(100vw - 32px)); padding: 10px 12px; text-align: left;
  background: var(--card, #fff); color: var(--fg, #1c2230); border: 1px solid var(--accent, #8a5f00); border-radius: 10px; box-shadow: 0 4px 16px rgba(0, 0, 0, .25); font-size: .95rem; font-weight: 400; line-height: 1.4; }
#term-pop[hidden] { display: none; }
#term-pop b { display: block; font-weight: 600; }
#term-pop small { display: block; margin-top: 6px; color: var(--muted, #5a6376); font-size: .78rem; }
#term-pop a { color: var(--accent, #8a5f00); }`;
  document.head.append(style);

  const pop = document.createElement("div");
  pop.id = "term-pop";
  pop.setAttribute("role", "tooltip");
  pop.hidden = true;
  let current = null, pinned = false, timer = 0;

  function close() {
    clearTimeout(timer);
    pop.hidden = true;
    current = null;
    pinned = false;
  }
  function open(el, pin) {
    clearTimeout(timer);
    if (!pop.isConnected) document.body.append(pop);
    const d = el.dataset.d, page = el.dataset.p, listed = /^[ivx]+$/.test(page);
    pop.textContent = "";
    const name = document.createElement("b"), body = document.createElement("span"), cite = document.createElement("small");
    name.textContent = el.dataset.t;
    body.textContent = d;
    cite.textContent = "PSAR Rev 1, " + (listed ? "List of Acronyms and Abbreviations, " : "") + "p. " + page;
    if (MORE) {
      const a = document.createElement("a");
      a.href = MORE;
      a.textContent = "All terms";
      cite.append(". ", a);
    }
    pop.append(name, body, cite);
    pop.hidden = false;
    current = el;
    pinned = pin;
    const r = el.getClientRects()[0] || el.getBoundingClientRect(), w = pop.offsetWidth, h = pop.offsetHeight;
    pop.style.left = Math.max(16, Math.min(r.left, innerWidth - w - 16)) + "px";
    pop.style.top = (r.bottom + 6 + h > innerHeight && r.top - 6 - h > 0 ? r.top - 6 - h : r.bottom + 6) + "px";
  }
  const term = e => e.target.closest ? e.target.closest("abbr.term") : null;

  // These run in the capture phase, so a tap on a term never picks an answer or flips a card.
  document.addEventListener("click", e => {
    const el = term(e);
    if (el) {
      e.preventDefault();
      e.stopPropagation();
      if (current === el && pinned) close(); else open(el, true);
    } else if (!pop.contains(e.target)) close();
  }, true);
  document.addEventListener("keydown", e => {
    if (e.key === "Escape") return close();
    const el = term(e);
    if (el && (e.key === "Enter" || e.key === " ")) {
      e.preventDefault();
      e.stopPropagation();
      if (current === el && pinned) close(); else open(el, true);
    }
  }, true);
  document.addEventListener("pointerover", e => {
    if (e.pointerType !== "mouse") return;
    const el = term(e);
    if (el && !pinned) open(el, false);
    else if (el || pop.contains(e.target)) clearTimeout(timer);
  });
  document.addEventListener("pointerout", e => {
    if (e.pointerType === "mouse" && !pinned && (term(e) || pop.contains(e.target))) timer = setTimeout(close, 250);
  });
  document.addEventListener("focusin", e => { const el = term(e); if (el && el.matches(":focus-visible")) open(el, false); });
  document.addEventListener("focusout", e => { if (term(e) && !pinned) close(); });
  addEventListener("scroll", () => { if (!pop.hidden) close(); }, true);
  addEventListener("resize", close);
  addEventListener("hashchange", close);

  window.Terms = { tag, spoilers, close };
})();
