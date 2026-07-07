#!/usr/bin/env python3
"""Build index.html (dataset inventory for MSc org psych / HRM projects) from datasets.json."""
import json, html, re
from pathlib import Path

HERE = Path(__file__).parent
DATA = json.loads((HERE / "datasets.json").read_text())

FAMILIES = [
    ("panel-survey", "Panel surveys", "Longitudinal individual/household data — supports change, within-person and lagged designs"),
    ("cross-sectional-survey", "Cross-sectional surveys", "Single- or repeated-wave surveys of individuals or establishments"),
    ("experience-sampling", "Experience sampling & diary", "Intensive repeated measures within days or weeks"),
    ("text-corpus", "Text corpora", "Employer reviews, job ads, judgments and other work-related text for NLP or content analysis"),
    ("qualitative", "Qualitative collections", "Interview transcripts, focus groups and ethnographic material"),
    ("occupational-database", "Occupational databases", "Occupation-level descriptors rather than individual respondents"),
    ("other", "Other sources", "Benchmark files, aggregate results and mixed formats"),
]
FAMILY_LABEL = {k: v for k, v, _ in FAMILIES}

ACCESS = {
    "open": ("Open download", "Direct download, at most a click-through licence"),
    "registration": ("Free registration", "Free account / end-user licence, typically same-day to a few days"),
    "application": ("Application needed", "Formal application (often via supervisor); allow weeks"),
}

def esc(s):
    return html.escape(str(s or ""), quote=True)

def card(d):
    fam = d["data_type"]
    acc = d["access"]
    meta_bits = [d.get("host", ""), d.get("countries", ""), d.get("years", "")]
    meta = " · ".join(esc(b) for b in meta_bits if b)
    q = d.get("example_question", "")
    search_blob = " ".join(str(d.get(k, "")) for k in
        ("name", "host", "description", "psych_variables", "sample", "countries", "years", "example_question")).lower()
    return f"""
<article class="card" data-family="{esc(fam)}" data-access="{esc(acc)}" data-search="{esc(search_blob)}">
  <div class="card-head">
    <h3><a href="{esc(d['url'])}" target="_blank" rel="noopener">{esc(d['name'])}</a></h3>
    <span class="pill pill-{esc(acc)}" title="{esc(ACCESS[acc][1])}">{esc(ACCESS[acc][0])}</span>
  </div>
  <p class="meta">{meta}</p>
  <p class="desc">{esc(d['description'])}</p>
  <p class="sample"><span class="lbl">Sample</span> {esc(d['sample'])}</p>
  <details>
    <summary>Variables &amp; project idea</summary>
    <p><span class="lbl">Psychological / work variables</span> {esc(d['psych_variables'])}</p>
    {f'<p><span class="lbl">Example question</span> {esc(q)}</p>' if q else ''}
  </details>
</article>"""

sections = []
for key, label, blurb in FAMILIES:
    members = [d for d in DATA if d["data_type"] == key]
    members.sort(key=lambda d: ({"open": 0, "registration": 1, "application": 2}.get(d["access"], 3), d["name"].lower()))
    if not members:
        continue
    cards = "\n".join(card(d) for d in members)
    sections.append(f"""
<section class="family" data-family="{key}">
  <div class="family-head">
    <h2>{esc(label)}</h2>
    <p class="family-blurb">{esc(blurb)}</p>
  </div>
  <div class="cards">{cards}</div>
</section>""")

n = len(DATA)
n_open = sum(1 for d in DATA if d["access"] == "open")
n_reg = sum(1 for d in DATA if d["access"] == "registration")
n_text = sum(1 for d in DATA if d["data_type"] == "text-corpus")
n_qual = sum(1 for d in DATA if d["data_type"] == "qualitative")

family_chips = "\n".join(
    f'<button class="chip" data-filter-family="{k}">{esc(l)} <span class="cnt">{sum(1 for d in DATA if d["data_type"]==k)}</span></button>'
    for k, l, _ in FAMILIES if any(d["data_type"] == k for d in DATA))
access_chips = "\n".join(
    f'<button class="chip" data-filter-access="{k}">{esc(v[0])} <span class="cnt">{sum(1 for d in DATA if d["access"]==k)}</span></button>'
    for k, v in ACCESS.items())

page = f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Datasets for MSc projects in organisational psychology &amp; HRM</title>
<meta name="description" content="A verified inventory of {n} secondary datasets — surveys, panels, text corpora and qualitative collections — for MSc dissertations in organisational/occupational psychology and HRM.">
<style>
:root {{
  --paper: #FAFBFC; --ink: #1C2530; --ink-soft: #4A5768; --line: #DCE2E9;
  --accent: #0F6B5C; --accent-ink: #0A5548; --card: #FFFFFF;
  --pill-open-bg: #E3F2EC; --pill-open-ink: #1D6A4E;
  --pill-reg-bg: #EAEEF3; --pill-reg-ink: #46566B;
  --pill-app-bg: #F7EEDD; --pill-app-ink: #8A6420;
  --chip-on-bg: #0F6B5C; --chip-on-ink: #F3FAF8;
}}
@media (prefers-color-scheme: dark) {{
  :root {{
    --paper: #151B22; --ink: #E4E9EE; --ink-soft: #9AA7B5; --line: #2A3542;
    --accent: #3FA08F; --accent-ink: #5FBCAC; --card: #1C242E;
    --pill-open-bg: #17342A; --pill-open-ink: #6FCBA4;
    --pill-reg-bg: #232D3A; --pill-reg-ink: #A6B5C7;
    --pill-app-bg: #372C17; --pill-app-ink: #D6AC5C;
    --chip-on-bg: #3FA08F; --chip-on-ink: #0E1A17;
  }}
}}
:root[data-theme="light"] {{
  --paper: #FAFBFC; --ink: #1C2530; --ink-soft: #4A5768; --line: #DCE2E9;
  --accent: #0F6B5C; --accent-ink: #0A5548; --card: #FFFFFF;
  --pill-open-bg: #E3F2EC; --pill-open-ink: #1D6A4E;
  --pill-reg-bg: #EAEEF3; --pill-reg-ink: #46566B;
  --pill-app-bg: #F7EEDD; --pill-app-ink: #8A6420;
  --chip-on-bg: #0F6B5C; --chip-on-ink: #F3FAF8;
}}
:root[data-theme="dark"] {{
  --paper: #151B22; --ink: #E4E9EE; --ink-soft: #9AA7B5; --line: #2A3542;
  --accent: #3FA08F; --accent-ink: #5FBCAC; --card: #1C242E;
  --pill-open-bg: #17342A; --pill-open-ink: #6FCBA4;
  --pill-reg-bg: #232D3A; --pill-reg-ink: #A6B5C7;
  --pill-app-bg: #372C17; --pill-app-ink: #D6AC5C;
  --chip-on-bg: #3FA08F; --chip-on-ink: #0E1A17;
}}
* {{ box-sizing: border-box; }}
body {{
  margin: 0; background: var(--paper); color: var(--ink);
  font: 16px/1.55 -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
}}
a {{ color: var(--accent-ink); }}
.wrap {{ max-width: 62rem; margin: 0 auto; padding: 0 1.25rem; }}
header.site {{ padding: 3rem 0 1.5rem; border-bottom: 1px solid var(--line); }}
h1, h2, .card h3 {{ font-family: Charter, "Bitstream Charter", Cambria, Georgia, serif; text-wrap: balance; }}
h1 {{ font-size: 2.1rem; line-height: 1.15; margin: 0 0 .6rem; font-weight: 700; }}
.standfirst {{ color: var(--ink-soft); max-width: 46rem; margin: 0 0 1.2rem; }}
.stats {{ display: flex; gap: 2rem; flex-wrap: wrap; margin: 0; padding: 0; list-style: none; }}
.stats b {{ display: block; font-size: 1.5rem; font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-variant-numeric: tabular-nums; color: var(--accent-ink); }}
.stats span {{ font-size: .8rem; text-transform: uppercase; letter-spacing: .06em; color: var(--ink-soft); }}
.toolbar {{
  position: sticky; top: 0; z-index: 5; background: var(--paper);
  border-bottom: 1px solid var(--line); padding: .8rem 0;
}}
.toolbar .row {{ display: flex; gap: .5rem; flex-wrap: wrap; align-items: center; }}
.toolbar .row + .row {{ margin-top: .5rem; }}
#search {{
  flex: 1 1 14rem; padding: .5rem .75rem; border: 1px solid var(--line); border-radius: 6px;
  background: var(--card); color: var(--ink); font: inherit;
}}
#search:focus {{ outline: 2px solid var(--accent); outline-offset: 1px; }}
.chip {{
  border: 1px solid var(--line); background: var(--card); color: var(--ink);
  border-radius: 999px; padding: .28rem .8rem; font-size: .85rem; cursor: pointer;
}}
.chip .cnt {{ color: var(--ink-soft); font-family: ui-monospace, Menlo, monospace; font-size: .78rem; }}
.chip[aria-pressed="true"] {{ background: var(--chip-on-bg); color: var(--chip-on-ink); border-color: var(--chip-on-bg); }}
.chip[aria-pressed="true"] .cnt {{ color: inherit; opacity: .75; }}
.chip:focus-visible, .pill:focus-visible, #theme:focus-visible {{ outline: 2px solid var(--accent); outline-offset: 1px; }}
.group-lbl {{ font-size: .72rem; text-transform: uppercase; letter-spacing: .08em; color: var(--ink-soft); margin-right: .25rem; }}
#shown {{ margin-left: auto; font-size: .85rem; color: var(--ink-soft); font-variant-numeric: tabular-nums; }}
#theme {{ border: 1px solid var(--line); background: var(--card); color: var(--ink); border-radius: 6px; padding: .28rem .6rem; cursor: pointer; font-size: .85rem; }}
section.family {{ padding: 2rem 0 .5rem; }}
.family-head h2 {{ font-size: 1.45rem; margin: 0; }}
.family-blurb {{ color: var(--ink-soft); margin: .25rem 0 1rem; font-size: .95rem; }}
.cards {{ display: grid; gap: 1rem; }}
.card {{
  background: var(--card); border: 1px solid var(--line); border-radius: 8px;
  padding: 1rem 1.15rem;
}}
.card-head {{ display: flex; gap: .75rem; align-items: baseline; justify-content: space-between; flex-wrap: wrap; }}
.card h3 {{ font-size: 1.12rem; margin: 0; font-weight: 600; }}
.card h3 a {{ text-decoration: none; }}
.card h3 a:hover {{ text-decoration: underline; }}
.pill {{
  font-size: .74rem; padding: .18rem .6rem; border-radius: 999px; white-space: nowrap;
  letter-spacing: .02em;
}}
.pill-open {{ background: var(--pill-open-bg); color: var(--pill-open-ink); }}
.pill-registration {{ background: var(--pill-reg-bg); color: var(--pill-reg-ink); }}
.pill-application {{ background: var(--pill-app-bg); color: var(--pill-app-ink); }}
.meta {{
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: .78rem;
  color: var(--ink-soft); margin: .2rem 0 .6rem; font-variant-numeric: tabular-nums;
}}
.desc {{ margin: 0 0 .6rem; max-width: 48rem; }}
.sample {{ font-size: .88rem; margin: 0 0 .4rem; color: var(--ink-soft); }}
.lbl {{
  font-size: .7rem; text-transform: uppercase; letter-spacing: .07em;
  color: var(--accent-ink); margin-right: .3rem; font-weight: 600; font-family: -apple-system, sans-serif;
}}
details {{ border-top: 1px dashed var(--line); margin-top: .5rem; padding-top: .5rem; }}
summary {{ cursor: pointer; font-size: .85rem; color: var(--accent-ink); }}
details p {{ font-size: .9rem; max-width: 48rem; }}
footer.site {{ border-top: 1px solid var(--line); margin-top: 3rem; padding: 1.5rem 0 3rem; color: var(--ink-soft); font-size: .87rem; }}
footer.site p {{ max-width: 48rem; }}
.hidden {{ display: none; }}
@media (prefers-reduced-motion: no-preference) {{
  .card {{ transition: border-color .15s ease; }}
  .card:hover {{ border-color: var(--accent); }}
}}
</style>
</head>
<body>
<header class="site">
  <div class="wrap">
    <h1>Datasets for MSc projects in organisational psychology &amp; HRM</h1>
    <p class="standfirst">A curated, link-checked inventory of {n} secondary datasets containing psychological and work-related variables — occupational choices, satisfaction, personality, ability, wellbeing, discrimination — spanning large surveys, panels, text corpora and genuinely qualitative collections. Every entry's landing page, variables and access route were independently verified in July&nbsp;2026.</p>
    <ul class="stats">
      <li><b>{n}</b><span>datasets</span></li>
      <li><b>{n_open}</b><span>open download</span></li>
      <li><b>{n_reg}</b><span>free registration</span></li>
      <li><b>{n_text}</b><span>text corpora</span></li>
      <li><b>{n_qual}</b><span>qualitative</span></li>
    </ul>
  </div>
</header>
<nav class="toolbar" aria-label="Filter datasets">
  <div class="wrap">
    <div class="row">
      <input id="search" type="search" placeholder="Search names, variables, populations… (e.g. Big Five, burnout, nurses)" aria-label="Search datasets">
      <button id="theme" title="Toggle colour theme" aria-label="Toggle colour theme">◐</button>
    </div>
    <div class="row"><span class="group-lbl">Type</span>{family_chips}</div>
    <div class="row"><span class="group-lbl">Access</span>{access_chips}<span id="shown"></span></div>
  </div>
</nav>
<main class="wrap">
{''.join(sections)}
</main>
<footer class="site">
  <div class="wrap">
    <p><strong>How this list was compiled.</strong> Candidate datasets were gathered from major survey archives (GESIS, UK Data Service, ICPSR), research data repositories (OSF, Zenodo, Kaggle, Dataverse), open-data papers in occupational psychology journals, and expert suggestion. Each entry was then independently verified: the landing page was fetched, claimed variables were checked against documentation, and the stated access route was confirmed. Details can still change — always confirm licence terms and variable availability in the official documentation before committing to a dissertation design.</p>
    <p>Access labels: <em>open download</em> = immediate; <em>free registration</em> = free account or end-user licence, usually granted within days; <em>application needed</em> = formal request, often requiring a supervisor — allow several weeks. Compiled July 2026.</p>
  </div>
</footer>
<script>
(function () {{
  var famFilter = null, accFilter = null, q = "";
  var cards = Array.prototype.slice.call(document.querySelectorAll(".card"));
  var sections = Array.prototype.slice.call(document.querySelectorAll("section.family"));
  var shown = document.getElementById("shown");

  function apply() {{
    var visible = 0;
    cards.forEach(function (c) {{
      var ok = (!famFilter || c.dataset.family === famFilter) &&
               (!accFilter || c.dataset.access === accFilter) &&
               (!q || c.dataset.search.indexOf(q) !== -1);
      c.classList.toggle("hidden", !ok);
      if (ok) visible++;
    }});
    sections.forEach(function (s) {{
      var any = s.querySelector(".card:not(.hidden)");
      s.classList.toggle("hidden", !any);
    }});
    shown.textContent = "Showing " + visible + " of {n}";
  }}

  document.querySelectorAll("[data-filter-family]").forEach(function (b) {{
    b.setAttribute("aria-pressed", "false");
    b.addEventListener("click", function () {{
      famFilter = famFilter === b.dataset.filterFamily ? null : b.dataset.filterFamily;
      document.querySelectorAll("[data-filter-family]").forEach(function (x) {{
        x.setAttribute("aria-pressed", String(x.dataset.filterFamily === famFilter));
      }});
      apply();
    }});
  }});
  document.querySelectorAll("[data-filter-access]").forEach(function (b) {{
    b.setAttribute("aria-pressed", "false");
    b.addEventListener("click", function () {{
      accFilter = accFilter === b.dataset.filterAccess ? null : b.dataset.filterAccess;
      document.querySelectorAll("[data-filter-access]").forEach(function (x) {{
        x.setAttribute("aria-pressed", String(x.dataset.filterAccess === accFilter));
      }});
      apply();
    }});
  }});
  document.getElementById("search").addEventListener("input", function (e) {{
    q = e.target.value.trim().toLowerCase();
    apply();
  }});

  var root = document.documentElement;
  var stored = null;
  try {{ stored = localStorage.getItem("theme"); }} catch (e) {{}}
  if (stored) root.setAttribute("data-theme", stored);
  document.getElementById("theme").addEventListener("click", function () {{
    var dark = root.getAttribute("data-theme") === "dark" ||
      (!root.getAttribute("data-theme") && window.matchMedia("(prefers-color-scheme: dark)").matches);
    var next = dark ? "light" : "dark";
    root.setAttribute("data-theme", next);
    try {{ localStorage.setItem("theme", next); }} catch (e) {{}}
  }});

  apply();
}})();
</script>
</body>
</html>"""

(HERE / "index.html").write_text(page)
print(f"Wrote index.html: {n} datasets, {len(sections)} sections, {len(page)//1024} KB")
