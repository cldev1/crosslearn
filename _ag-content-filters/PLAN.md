# Content Taxonomy & Filtering Plan for CrossLearn (LearnFeed)

This document defines the filter taxonomy, schema specifications, and implementation strategy for tagging the 264 CrossLearn micro-lessons for the LearnFeed mobile application.

---

## 1. Corpus Analysis & Sampling Insights

A complete audit of all 264 lessons in `C:\Users\san\Projects\crosslearn` was conducted across early, mid, late numbers, and both storage formats:
- **Total Lessons:** 264
- **Storage Breakdown:**
  - `README.md` lessons: 199 lessons (Slugs `01` through `200`)
  - `index.html` lessons: 65 lessons (Slugs `201` through `265`)
- **Lesson Length & Reading Time:**
  - Minimum length: 113 words (~30 seconds)
  - 25th percentile: 197 words (~50 seconds)
  - Median length: 259 words (~65 seconds)
  - 75th percentile: 394 words (~100 seconds)
  - 90th percentile: 490 words (~120 seconds)
  - Maximum length: 722 words (~180 seconds)
  - **Key Finding:** 100% of lessons are micro-lessons designed to be read in under 3 minutes.

### Author Distribution (100% of Corpus Accounted For)
The corpus features a concentrated set of world-class product thinkers, with the top 6 sources accounting for over 72% of all lessons:

| Source Slug | Author / Source Name | Lesson Count | % of Corpus | Format(s) Present |
| :--- | :--- | :---: | :---: | :--- |
| `shreyas-doshi` | Shreyas Doshi (@shreyas) | 47 | 17.8% | README.md |
| `john-cutler` | John Cutler (@johncutlefish) | 35 | 13.3% | README.md |
| `lenny-rachitsky` | Lenny Rachitsky (@lennysan) & Podcast | 32 | 12.1% | README.md + index.html |
| `pavel-samsonov` | Pavel A. Samsonov (@PavelASamsonov) | 31 | 11.7% | README.md |
| `april-dunford` | April Dunford (@aprildunford) | 25 | 9.5% | README.md |
| `george-nurijanian`| George / prodmgmt.world (@nurijanian) | 21 | 8.0% | index.html |
| `julie-zhuo` | Julie Zhuo (@joulee) | 13 | 4.9% | README.md |
| `scrum-org` | Scrum.org (@Scrumdotorg) / Ralph Jocham | 12 | 4.5% | README.md + index.html |
| `melissa-perri` | Melissa Perri (@lissijean) | 10 | 3.8% | README.md |
| `gibson-biddle` | Gibson Biddle (@gibsonbiddle) | 8 | 3.0% | README.md |
| `itamar-gilad` | Itamar Gilad (@itamargilad) | 6 | 2.3% | README.md |
| `molly-graham` | Molly Graham | 6 | 2.3% | index.html |
| `teresa-torres` | Teresa Torres (@ttorres) | 5 | 1.9% | README.md |
| `janna-bastow` | Janna Bastow (@simplybastow) | 4 | 1.5% | README.md |
| `pawel-huryn` | Paweł Huryn (@PawelHuryn) | 2 | 0.8% | README.md |
| *Guest / Curated* | Single-lesson authors (Jen Abel, Guillermo Rauch, Claire Vo, Cat Wu, Adam Nash, etc.) | 7 | 2.6% | README.md + index.html |
| **Total** | | **264** | **100.0%** | |

---

## 2. Filter Group Evaluation & Selection

Mobile filtering requires **high signal-to-noise**, **few filter groups**, and **crisp chip values** that do not crowd mobile viewports. We evaluated the 6 candidate dimensions against the real corpus:

### Dimension Verdicts:

1. **`topic` — RECOMMENDED (Primary Group)**
   - *Verdict:* Keep. Essential for thematic discovery.
   - *Behavior:* Multi-select (1 to 2 values per lesson).
   - *Corpus Grounding:* Content naturally clusters into 9 unambiguous product management domains.

2. **`source` — RECOMMENDED (Primary Group)**
   - *Verdict:* Keep. Author brand affinity is one of the highest-intent discovery paths for product managers.
   - *Behavior:* Single-select chip.
   - *Corpus Grounding:* 100% objective; every lesson has an explicit source attribution.

3. **`format` — RECOMMENDED (Primary Group)**
   - *Verdict:* Keep. Allows users to switch between learning mindsets: theoretical/heuristic ("principle"), structural ("framework"), tactical ("playbook"), or diagnostic ("anti-pattern").
   - *Behavior:* Single-select chip.
   - *Corpus Grounding:* Distinct editorial patterns across lessons.

4. **`skill_level` — NOT RECOMMENDED for Primary Mobile Chips**
   - *Corpus Evidence:* Over 77% of lessons sit in the intermediate practitioner zone. True "beginner" lessons make up only ~4.5% (12 lessons), while the boundary between "intermediate" and "advanced" is highly subjective.
   - *UX Impact:* Having an active filter chip where 80% of items are in one bucket creates an imbalanced filter experience on mobile.
   - *Recommendation:* Exclude from primary mobile chips. (If stored in metadata for future use, restrict strictly to `foundational` vs `practitioner`).

5. **`duration` / `effort` — REJECTED**
   - *Corpus Evidence:* Word counts have near-zero meaningful variance. Median length is 259 words (~1 minute), and 90% are under 490 words (~2 minutes). 100% of lessons can be read in under 3 minutes.
   - *UX Impact:* Labeling a 1-minute read as "quick" and a 2.5-minute read as "deep" violates user expectations of what a "deep dive" is.
   - *Recommendation:* Do NOT add a duration or effort tag.

6. **`audience` — OPTIONAL / SECONDARY**
   - *Corpus Evidence:* Every single lesson explicitly contains a `## Why it matters for a PO` section; therefore, 100% of the corpus addresses Individual Contributor PMs / Product Owners. Sub-audiences (`product-leader`, `founder-exec`, `cross-functional`) exist for ~30% of lessons, but adding this group to mobile chips risks cluttering the screen.
   - *Recommendation:* Keep secondary or omit from mobile filter bar to preserve clean 3-group filter UI.

---

## 3. Final Controlled Vocabulary

All values use lowercase `kebab-case`.

### A. Topic Vocabulary (9 values, multi-select, max 2 per lesson)

| Topic Slug | Description & Scope | Primary Authors | Frequency Est. |
| :--- | :--- | :--- | :---: |
| `strategy` | High-level bets, vision, GLEE, DHM, strategic trade-offs, competitive advantage, market choices, business models | Doshi, Biddle, Gilad, Perri | ~50 (19%) |
| `delivery-execution` | Sprint cadence, tech debt, shipping, user stories (INVEST), dual-track agile, feature factory avoidance, WIP limits | Scrum.org, Cutler, Nurijanian | ~50 (19%) |
| `roadmaps-prioritization` | Roadmaps (70/20/10, branching, now-next-later), backlog grooming, feature buckets, rejection registers, bet sizing | Cutler, Bastow, Samsonov, Nash | ~45 (17%) |
| `leadership-org` | Managing up, influencing executives, team health/trust, org design, hiring, giving away Legos, burnout, conflict | Perri, Graham, Cutler, Doshi | ~38 (14%) |
| `positioning` | Market categories, competitive alternatives, differentiated value, B2B sales narrative/storytelling, pitch decks | Dunford | ~38 (14%) |
| `metrics-analytics` | OKRs, outcomes vs outputs, Goodhart's law, leading indicators, North Star, proxy delusion, measurement under uncertainty | Zhuo, Cutler, Samsonov | ~30 (11%) |
| `ai-product` | AI-native product development, evals as PM craft, LLM UX patterns, AI operating models, automated delivery bets | Rachitsky, Vo, Wu, Scrum.org | ~28 (11%) |
| `discovery` | Customer interviews, assumption testing, user research, Opportunity Solution Trees (OST), observing vs asking | Torres, Samsonov, Doshi | ~25 (9%) |
| `career-habits` | Personal effectiveness, high agency, LNO framework, 14 PM habits, time allocation, 30-60-90, eng-to-PM transition | Doshi, Zhuo, Nurijanian | ~20 (8%) |

*Note: Frequencies sum to >100% because up to 2 topics can be assigned per lesson.*

### B. Format Vocabulary (4 values, single-select)

| Format Slug | Description & Criteria | Examples in Corpus | Frequency Est. |
| :--- | :--- | :--- | :---: |
| `principle` | Core philosophy, heuristic, mental model, counter-intuitive maxim, or mindset shift | *Steering, not rowing*; *High agency*; *Opposite of a good idea can also be good* | ~120 (45%) |
| `framework` | Named conceptual model, matrix, multi-component schema, or formula | *DHM stack*; *70/20/10*; *LNO framework*; *5 components of positioning*; *3X* | ~80 (30%) |
| `anti-pattern` | Pathology diagnosis, trap, fallacy, organizational dysfunction, or anti-goal | *Feature factory*; *PO as backlog secretary*; *Proxy delusion*; *Hero culture* | ~45 (17%) |
| `playbook` | Step-by-step ritual, operational script, diagnostic scorecard, or concrete checklist | *Pre-mortem protocol*; *10 tests for PMF*; *Rejection register*; *8 metric questions* | ~19 (8%) |

### C. Source Vocabulary (Single-select)

Primary controlled source slugs:
- `shreyas-doshi`
- `john-cutler`
- `lenny-rachitsky`
- `pavel-samsonov`
- `april-dunford`
- `george-nurijanian`
- `julie-zhuo`
- `scrum-org`
- `melissa-perri`
- `gibson-biddle`
- `itamar-gilad`
- `molly-graham`
- `teresa-torres`
- `janna-bastow`
- `pawel-huryn`
- `other` (or exact author slug: `jen-abel`, `guillermo-rauch`, `claire-vo`, `cat-wu`, `adam-nash`, etc.)

---

## 4. Frontmatter Schema Specification

### For Markdown Lessons (`README.md`)
The YAML frontmatter sits at the very beginning of `README.md`, enclosed by `---`.

```yaml
---
filters:
  topic:
    - strategy
    - roadmaps-prioritization
  format: framework
  source: shreyas-doshi
---
```

#### Schema Rules:
1. **Namespace:** All metadata resides under the top-level `filters` key.
2. **`topic`:** Required array of strings. Minimum 1, maximum 2 values from the topic vocabulary.
3. **`format`:** Required string. Exactly 1 value from the format vocabulary.
4. **`source`:** Required string. Exactly 1 value from the source vocabulary.
5. **LearnFeed Ingest Compatibility:**
   In `learnfeed/packages/content/scripts/lib/parse-lessons.mjs`, title extraction uses `/^#\s+(.+)$/m` (multiline). Adding frontmatter does not alter H1 matching or `summaryFromMarkdown`.

---

## 5. Strategy for HTML-Only Lessons (`index.html`)

There are 65 lessons (Slugs `201` through `265`) stored as `index.html` without markdown files.

### Evaluation of Approaches:

| Approach | Description | Pros | Cons | Recommendation |
| :--- | :--- | :--- | :--- | :--- |
| **Option A: YAML in HTML Comment** | Place `<!--\nfilters:\n  topic: [...]\n  format: ...\n  source: ...\n-->` at top of `index.html` | 100% identical YAML syntax to README.md; 0 changes to prose; ignored by HTML parsers; zero sidecar clutter | Custom HTML comment parsing in ingest | **RECOMMENDED (Primary)** |
| **Option B: HTML `<meta>` in `<head>`** | `<meta name="crosslearn:filters" content='...'>` | Standard HTML5 | JSON escaping inside attributes is awkward in git diffs | Alternative |
| **Option C: Sidecar file `filters.yaml`** | Add `filters.yaml` in each directory | Clean separation from HTML | Adds 65 extra files to repo; two files per lesson | Not Recommended |
| **Option D: Convert HTML to `README.md`** | Convert HTML lessons to markdown | Uniform format across all 264 | Violates "Prefer NOT rewriting lesson prose" constraint | Reject for Now |

> [!IMPORTANT]
> **Why NOT a `README.md` sidecar with only metadata?**
> In LearnFeed's `ingest.mjs`:
> ```javascript
> const readme = existsSync(readmePath) ? readFileSync(readmePath, 'utf8') : null;
> const html = readme == null && existsSync(htmlPath) ? readFileSync(htmlPath, 'utf8') : null;
> ```
> If a `README.md` sidecar is added to an HTML lesson directory, `ingest.mjs` will treat that `README.md` as the **entire lesson body** and completely drop the `index.html` content! Therefore, metadata must be embedded directly inside `index.html`.

### Proposed Standard for `index.html`:
Insert a clean YAML comment block at the very top of `index.html`, right before `<!DOCTYPE html>`:

```html
<!--
filters:
  topic:
    - delivery-execution
  format: playbook
  source: george-nurijanian
-->
<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8"/>...
```

#### How LearnFeed Ingest Will Extract This:
```javascript
export function parseFilters(content) {
  // Matches YAML frontmatter in README.md or top HTML comment in index.html
  const mdMatch = /^---\r?\n([\s\S]*?)\r?\n---/.exec(content);
  if (mdMatch) return yaml.parse(mdMatch[1])?.filters;

  const htmlMatch = /^<!--\r?\n([\s\S]*?)\r?\n-->/.exec(content);
  if (htmlMatch) return yaml.parse(htmlMatch[1])?.filters;

  return null;
}
```

---

## 6. End-to-End Implementation Checklist

When ready for the IMPLEMENT phase, follow this exact sequence:

- [ ] **Step 1: Automated Catalog Generation**
  - Run a classification script to generate a draft mapping for all 264 lessons (`_ag-content-filters/draft-tags.csv`) containing `slug`, `title`, `author`, `topic`, `format`, and `source`.
- [ ] **Step 2: Editorial Review & Spot-Check**
  - Review all ambiguous edge cases (e.g. lessons touching both strategy and execution).
  - Verify every single lesson has at least 1 topic, at most 2 topics, exactly 1 format, and exactly 1 source.
- [ ] **Step 3: Apply Frontmatter to 199 `README.md` Lessons**
  - Insert YAML frontmatter block at the top of each `README.md` file.
  - Preserve all existing headings, illustrations, and prose without reformatting.
- [ ] **Step 4: Apply HTML Metadata Comments to 65 `index.html` Lessons**
  - Prepend the comment block `<!--\nfilters:\n...\n-->` to each `index.html`.
  - Ensure zero changes to `<main>` tags or lesson prose.
- [ ] **Step 5: Automated Validation**
  - Run a validation script over all 264 directories to verify:
    - Every file parses valid YAML.
    - Every tag conforms strictly to the controlled vocabulary.
    - No `README.md` file was accidentally added to an `index.html` directory.
- [ ] **Step 6: Ingest Readiness Check**
  - Test LearnFeed's `parse-lessons.mjs` against the tagged lessons to confirm zero regressions in title or summary extraction.
