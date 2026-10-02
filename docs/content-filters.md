# CrossLearn Content Taxonomy & Filters

This document defines the filter taxonomy, schema specifications, and downstream consumption patterns for tagging the 264 CrossLearn micro-lessons.

---

## 1. Filter Dimensions & Controlled Vocabulary

All filter values use lowercase `kebab-case`.

### A. `topic` (Multi-select, 1 to 2 values per lesson)
High-level thematic domain of the lesson. Every lesson is assigned at least 1 and at most 2 topics.

| Topic Slug | Description & Scope | Example Concepts |
| :--- | :--- | :--- |
| `strategy` | High-level bets, vision, GLEE, DHM, strategic trade-offs, competitive advantage, market choices, business models. | *Eigenquestion*, *Kent Beck's 3X*, *GLEE vision*, *One growth lane* |
| `delivery-execution` | Sprint cadence, tech debt, shipping, user stories (INVEST), dual-track agile, feature factory avoidance, WIP limits, deprecation. | *INVEST user stories*, *Deprecation*, *Refinement continuous*, *WIP limits* |
| `roadmaps-prioritization` | Roadmaps (70/20/10, branching, now-next-later), backlog grooming, feature buckets, rejection registers, bet sizing, force-ranking. | *70/20/10 roadmap*, *Branching roadmaps*, *Rejection register*, *Three feature buckets* |
| `leadership-org` | Managing up, influencing executives, team health/trust, org design, hiring, giving away Legos, burnout, conflict, team autonomy. | *Pre-mortems*, *Three levels of product work*, *Giving away Legos*, *Director ceiling* |
| `positioning` | Market categories, competitive alternatives, differentiated value, B2B sales narrative/storytelling, pitch decks. | *5 components of positioning*, *Value themes*, *Market category assumptions* |
| `metrics-analytics` | OKRs, outcomes vs outputs, Goodhart's law, leading indicators, North Star, proxy delusion, measurement under uncertainty. | *Eight metric questions*, *Proxy delusion*, *Five data values*, *A/B testing* |
| `ai-product` | AI-native product development, evals as PM craft, LLM UX patterns, AI operating models, automated delivery bets. | *Evals core PM craft*, *Ship incomplete bets*, *Inputs → chat → outputs*, *AI fluency* |
| `discovery` | Customer interviews, assumption testing, user research, Opportunity Solution Trees (OST), observing vs asking, prototype learning. | *OST specific stories*, *Assumption tests*, *Customer Problem Stack Ranking*, *Issue trees* |
| `career-habits` | Personal effectiveness, high agency, LNO framework, 14 PM habits, time allocation, 30-60-90, eng-to-PM transition. | *14 PM habits*, *LNO framework*, *High agency*, *First 30-60-90 days* |

### B. `format` (Single-select, exactly 1 value per lesson)
The pedagogical archetype / learning posture of the lesson.

| Format Slug | Description & Criteria | Examples in Corpus |
| :--- | :--- | :--- |
| `principle` | Core philosophy, heuristic, mental model, counter-intuitive maxim, or mindset shift without a named multi-part schema or step-by-step ritual. | *Steering, not rowing*; *High agency*; *Opposite of a good idea can also be good*; *Data is not a trust proxy* |
| `framework` | Named conceptual model, matrix (2x2), formula, multi-part schema, or structured lifecycle/stages. | *Kent Beck's 3X*; *DHM stack*; *70/20/10*; *LNO framework*; *5 components of positioning*; *Three levels of product work* |
| `anti-pattern` | Pathology diagnosis, trap, fallacy, organizational dysfunction, anti-goal, symptom of failure, or cautionary tale. | *Feature factory*; *PO as backlog secretary*; *Proxy delusion*; *Hero culture*; *The build trap*; *Ship all our bad ideas* |
| `playbook` | Step-by-step ritual, operational script, diagnostic scorecard/questions, or concrete checklist. | *Pre-mortem protocol (Tigers/Elephants)*; *Ten tests for PMF*; *Rejection register*; *Eight metric questions*; *Evals setup* |

### C. `source` (Single-select, exactly 1 value per lesson)
The canonical kebab-case author slug representing the primary thinker behind the lesson.

- `shreyas-doshi` (47 lessons)
- `john-cutler` (35 lessons)
- `pavel-samsonov` (31 lessons)
- `april-dunford` (25 lessons)
- `lenny-rachitsky` (23 lessons)
- `george-nurijanian` (21 lessons)
- `julie-zhuo` (13 lessons)
- `scrum-org` (12 lessons)
- `melissa-perri` (10 lessons)
- `gibson-biddle` (8 lessons)
- `itamar-gilad` (6 lessons)
- `molly-graham` (6 lessons)
- `teresa-torres` (5 lessons)
- `janna-bastow` (4 lessons)
- `pawel-huryn` (2 lessons)
- `claire-vo` (2 lessons)
- `cat-wu` (1 lesson)
- `adam-nash` (1 lesson)
- `des-traynor` (1 lesson)
- `alejandro-vivanco` (1 lesson)
- `grant-lee` (1 lesson)
- `jason-spielman` (1 lesson)
- `guillermo-rauch` (1 lesson)
- `jen-abel` (1 lesson)
- `nan-yu` (1 lesson)
- `martin-tobias` (1 lesson)
- `sajith-pai` (1 lesson)
- `geoff-charles` (1 lesson)
- `marty-cagan` (1 lesson)
- `ryan-stein` (1 lesson)

---

## 2. In-File Schemas

Lessons in CrossLearn exist in two file layouts: Markdown (`README.md`) and static HTML (`index.html`).

### A. Markdown Lessons (`README.md`)
Filters are embedded as standard YAML frontmatter at the very top of `README.md`, enclosed by `---`:

```yaml
---
filters:
  topic:
    - strategy
    - ai-product
  format: framework
  source: lenny-rachitsky
---

# Ship incomplete bets, then wait for the model
...
```

### B. HTML-Only Lessons (`index.html`)
For the 65 lessons stored as HTML without Markdown, filters are embedded as a YAML comment block immediately preceding `<!DOCTYPE html>`:

```html
<!--
filters:
  topic:
    - strategy
    - leadership-org
  format: framework
  source: george-nurijanian
-->
<!DOCTYPE html>
<html lang="en">
...
```

> [!IMPORTANT]
> **No `README.md` Sidecar Files for HTML Lessons:**
> LearnFeed's ingest script checks `existsSync(readmePath) ? readFileSync(...) : html ? ...`.
> Adding a metadata-only `README.md` to an HTML lesson folder would shadow `index.html` and drop the lesson body. Therefore, metadata is stored directly inside `index.html`.

---

## 3. Rationale for Omitted Dimensions

During taxonomy design, three candidate dimensions were evaluated and rejected:

1. **`skill_level` (Rejected):**
   - Over 77% of the corpus resides in the intermediate practitioner zone. True "beginner" lessons make up under 5% (12 lessons), while the boundary between intermediate and advanced is subjective. An imbalanced filter where 80% of items sit in one chip produces poor UX.
2. **`duration` / `effort` (Rejected):**
   - Word count variance across the 264 lessons is extremely narrow: median reading time is ~65 seconds (259 words), 90th percentile is ~120 seconds (490 words), and 100% can be read in under 3 minutes. Labeling a 1-minute read as "quick" and a 2.5-minute read as "deep dive" violates user expectations.
3. **`audience` (Omitted from Primary Filters):**
   - Every lesson includes a `## Why it matters for a PO` section, so 100% of the corpus targets product practitioners / POs. Sub-audiences (leaders, founders) exist for only ~30% of lessons; adding a 4th chip group would crowd mobile screens.

---

## 4. Downstream Consumption in LearnFeed / Expo

When LearnFeed ingests CrossLearn lessons:
1. `parse-lessons.mjs` parses the `filters` block from Markdown frontmatter or HTML comments.
2. The frontmatter is stripped from the generated markdown bodies in `generated/lessons/*.md` so the reader view displays clean prose without raw YAML blocks.
3. The parsed filter object is attached to each lesson in `manifest.json`:
   ```json
   {
     "id": "01-ship-incomplete-bets",
     "slug": "01-ship-incomplete-bets",
     "title": "Ship incomplete bets, then wait for the model",
     "order": 1,
     "path": "01-ship-incomplete-bets/README.md",
     "illustrationUrl": "...",
     "githubUrl": "...",
     "summary": "...",
     "filters": {
       "topic": ["strategy", "ai-product"],
       "format": "framework",
       "source": "lenny-rachitsky"
     }
   }
   ```
4. The Expo mobile UI consumes `manifest.filters` directly to power filtering by Topic (multi-select / pills), Format (single-select toggle), and Source (author filter).
