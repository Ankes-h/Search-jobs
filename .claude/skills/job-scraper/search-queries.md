# Search Queries for Job Scraper

## Installed portal CLIs (primary for `/scrape`)

`/scrape` discovers every portal skill under `.agents/skills/*/SKILL.md` and runs its CLI first. Shipped country-agnostic CLIs include `linkedin-search` and `freehire-search`. You do **not** need a matching `site:` line below for those CLIs to run.

The `site:` query templates in this file are the **WebSearch fallback** — for portals without a CLI, company career pages, or when a CLI fails.

**Language scope:** Queries target English and Hindi job markets (the primary professional language for technical and AI job listings in India is English).

## Search Sites

Primary:
- **linkedin.com/jobs** - LinkedIn job listings (filter: India / Remote / Delhi NCR / Bengaluru / Mohali); also queried via `linkedin-search` CLI
- **freehire-search** - Remote developer and AI job listings
- **naukri.com** - Major Indian employment portal
- **internshala.com** - Leading internship board for students in India

Secondary (company career pages via Google):
- Direct Google searches with `site:` filters for AI startups and technology companies

## Query Categories

### Priority 1: AI / Machine Learning & Junior AI Developer

These match Ankesh's primary career direction in Artificial Intelligence and Machine Learning.

```
site:linkedin.com/jobs "AI intern" India
site:linkedin.com/jobs "Machine Learning intern" India
site:linkedin.com/jobs "Junior AI Developer" India
site:linkedin.com/jobs "AI/ML intern" Remote India
site:internshala.com/internships "Artificial Intelligence"
site:naukri.com "Machine Learning Intern"
```

### Priority 2: Prompt Engineering & Generative AI

These match domain expertise in prompt engineering, LLM evaluation, and agentic workflows.

```
site:linkedin.com/jobs "Prompt Engineer" India
site:linkedin.com/jobs "Prompt Engineering Intern" India
site:linkedin.com/jobs "Generative AI intern" India
site:linkedin.com/jobs "LLM intern" India
site:linkedin.com/jobs "Prompt Engineer" Remote
```

### Priority 3: Technical Content Writing & AI Research

Adjacent roles leveraging Ankesh's technical blogging and publication experience.

```
site:linkedin.com/jobs "Technical Content Writer" AI India
site:linkedin.com/jobs "Technical Writer" "Artificial Intelligence" India
site:linkedin.com/jobs "AI Content Writer" Remote
site:internshala.com/internships "Technical Writing"
```

### Priority 4: Broader Python & Software Development

Wider net for foundational programming roles in Python, React, and software engineering.

```
site:linkedin.com/jobs "Python intern" India
site:linkedin.com/jobs "Junior Python Developer" India
site:linkedin.com/jobs "React Developer intern" India
site:internshala.com/internships "Python Developer"
```

## Location Filter

When evaluating results, verify the job location matches Ankesh's geographic scope:
- **Ideal:** Remote (work from anywhere in India)
- **Acceptable:** Delhi/NCR (Noida, Gurugram, New Delhi), Chandigarh / Mohali / Patiala (near university campus), Bengaluru, Hyderabad, Pune, Mumbai
- **Too far / Excluded:** Permanent relocation outside India at this stage

## Language Filter

Candidate works in English (fluent / professional) and Hindi (native). Technical postings in English are a clean PASS.

## Date Filter

Only include jobs posted within the last 14 days, or with an open application deadline.
