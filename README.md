# Datasets for MSc projects in organisational psychology & HRM

A curated, link-checked inventory of **78 secondary datasets** with psychological and work-related variables — occupational choices, job satisfaction, personality, cognitive ability, wellbeing, engagement, discrimination — suitable for 3-month MSc dissertations in organisational/occupational psychology and HRM.

**Live site:** https://lukaswallrich.github.io/orgpsy-datasets/

## How the inventory was compiled

The list was built in July 2026 through a multi-agent search-and-verify pipeline (Claude Code workflow), with the OpenAI Codex CLI as an independent idea generator.

### 1. Search (six parallel finder agents, one per source modality)

Each agent searched the live web and returned candidates in a fixed schema (name, host, URL, psychological variables, sample, years, access level, example research question). The modalities:

| Modality | Sources searched |
|---|---|
| Major panel / social surveys | GSS, ESS, ISSP, Understanding Society, SOEP, HILDA, NLSY, MIDUS, EWCS, WERS, SHARE, LISS, cohort studies, and their archives (GESIS, UK Data Service, ICPSR) |
| Data repositories | ICPSR/openICPSR, UK Data Service catalogue, GESIS, OSF, Zenodo, Mendeley Data, figshare, Journal of Open Psychology Data |
| Open data alongside journal articles | OpenAlex queries over top OP/HRM journals (JAP, Personnel Psychology, JVB, JOOP, JOB, EJWOP, Work & Stress) plus targeted OSF searches |
| Text corpora | Employer-review corpora (Glassdoor-type), job-ad datasets, tribunal judgments, workplace email, Reddit — Kaggle, Zenodo, GitHub, government sources |
| Qualitative collections | UK Data Service QualiBank, Qualitative Data Repository (Syracuse), Timescapes, Finnish Social Science Data Archive, and repository-wide searches for interview transcripts on work/careers |
| Unusual sources | Open-Source Psychometrics raw data, SAPA, Project Implicit, O*NET, PIAAC, FEVS, NHS Staff Survey, Civil Service People Survey, experience-sampling archives |

Finder agents were required to fetch every candidate's landing page before returning it — no datasets from memory alone.

### 2. Independent idea generation (Codex CLI)

In parallel, the Codex CLI produced an 80-item candidate list from its own knowledge. After deduplication against the agents' findings, 11 promising Codex-only suggestions (e.g. UK Employment Tribunal decisions, Ask a Manager salary survey, Wisconsin Longitudinal Study, ESENER) went through the same verification as everything else; 10 survived.

### 3. Adversarial verification (one agent per candidate)

Every deduplicated candidate (84 from the finders + 11 Codex extras) was checked by a separate verification agent instructed to assume the entry might be fabricated or embellished. Each verifier:

1. fetched the URL (or resolved the DOI via DataCite/Crossref) and confirmed it describes the claimed dataset;
2. checked the claimed psychological variables against actual documentation, trimming unsupported claims;
3. confirmed the access level is realistic for an MSc student (open / free registration / formal application);
4. confirmed the data are real respondents or real documents, not synthetic (excluding, e.g., the ubiquitous fake "IBM HR Attrition" dataset and its clones);
5. sanity-checked sample sizes and years.

Outcomes: 33 entries were **corrected** (dead or wrong URLs replaced — including a HILDA DOI that resolved to the wrong file —, access levels fixed, sample sizes adjusted), and unverifiable candidates were **rejected**. A sample of verification verdicts was cross-checked against a stronger model (4/4 agreement, including the subtlest URL error) to validate the verifier setup.

### 4. Curation and page build

Cross-source duplicates were merged (keeping the richest verified entry), verifier meta-language was scrubbed from descriptions, and the static page was generated from the JSON.

## Repository contents

- `datasets.json` — all 78 entries, including each verifier's notes (`verify_notes`) and verdict
- `build_site.py` — generates `index.html` from `datasets.json` (no dependencies beyond Python 3)
- `index.html` — the site: client-side search, type/access filters, light/dark theme

To update: edit `datasets.json`, run `python3 build_site.py`, commit and push.

## Caveats

- Access conditions and licences change; the page states what was verified in **July 2026** — always confirm against the official documentation before committing to a dissertation design.
- Scraped text corpora (employer reviews, job ads) carry licence/ToS caveats noted in their descriptions.
- Six entries require formal applications (e.g. HILDA, SOEP, CLC-UKET) and are labelled accordingly — students should allow several weeks and involve their supervisor.
