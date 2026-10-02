You are tagging CrossLearn lessons for LearnFeed mobile app filters. CONTENT ONLY — do NOT touch any Expo/React Native UI.

Workspace: C:\Users\san\Projects\crosslearn (source of truth). Catalog skim: _catalog-skim.csv (264 lessons). Lessons are folders NN-slug/ with README.md (most) or index.html only (older ~65).

## Phase: PLAN ONLY. Do not edit lesson files yet (writing PLAN.md is required).

1. Sample broadly across the corpus (early, mid, late numbers; multiple authors; README and HTML). Read enough titles + "What it claims" / body openings to propose a REAL taxonomy grounded in content — do not invent filters that don't fit.

2. Propose FILTER OPTION GROUPS (not one flat tag soup), mobile-friendly: few groups, clear chip values. Likely candidates to validate against corpus:
   - topic / domain (e.g. strategy, discovery, positioning, metrics, leadership, growth, AI/product, roadmaps, org/process, craft/habits…)
   - skill_level (beginner / intermediate / advanced) — only if distinguishable
   - format (framework, playbook, principle, anti-pattern, checklist, case…) — only if real
   - source_type or author/source family
   - duration/effort (quick read vs deep) — only if content length varies meaningfully
   - audience (IC PM, manager, founder, designer-facing…) — only if clear

3. Finalize a SMALL controlled vocabulary: merge synonyms, prefer kebab-case values, multi-select allowed within a group where natural (e.g. topic), single-select where exclusive (e.g. skill_level).

4. Propose frontmatter shape for README.md lessons, e.g.:
---
filters:
  topic: [strategy, discovery]
  skill_level: intermediate
  format: framework
  source: shreyas-doshi
  effort: quick
  audience: [ic-pm]
---
(or tags: structured by group — pick one schema and stick to it)

5. For HTML-only lessons without YAML frontmatter: propose how to tag (add README.md sidecar? HTML comment? convert?) — prefer an approach Learnfeed ingest can pick up later. Prefer NOT rewriting lesson prose.

6. Write the full proposed taxonomy + schema + HTML strategy to:
   C:\Users\san\Projects\crosslearn\_ag-content-filters\PLAN.md

Also include approximate value frequency estimates from your sampling.

Do NOT apply tags yet. Do NOT push. Do NOT touch learnfeed. End PLAN.md with a clear IMPLEMENT checklist.
