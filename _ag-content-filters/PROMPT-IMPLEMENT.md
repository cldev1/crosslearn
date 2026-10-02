# IMPLEMENT: Apply content filters to ALL CrossLearn lessons

You already planned this. Read:
- C:\Users\san\Projects\crosslearn\_ag-content-filters\PLAN.md
- C:\Users\san\Projects\crosslearn\_ag-content-filters\draft-tags.csv
- C:\Users\san\Projects\crosslearn\_ag-content-filters\validate_tags.py

CONTENT ONLY. Do NOT touch Expo / LearnFeed mobile UI. Do NOT publish to GitHub Pages.

## Goals
1. Editorial-fix draft tags while applying (do NOT blindly trust draft):
   - Fix obvious topic mistakes (examples: 06-explore-expand-extract is strategy NOT positioning; 13-one-growth-lane is strategy/growth NOT discovery; 14-seven-lenses-for-an-idea is strategy/discovery NOT ai-product; 04-three-levels is leadership-org or strategy+delivery, not only delivery).
   - Rebalance format: draft over-labeled `principle` (~217). Named models/matrices → `framework`; numbered checklists/rituals → `playbook`; pathology/trap diagnoses → `anti-pattern`. Keep `principle` for heuristics/maxims without a named multi-part schema.
   - Max 2 topics per lesson; exactly 1 format; exactly 1 source slug (kebab-case). Vocabulary from PLAN.md.
   - Update draft-tags.csv to match final applied tags.

2. Apply filters to EVERY lesson folder (264):
   - README.md lessons: prepend YAML frontmatter:
     ---
     filters:
       topic:
         - <slug>
       format: <slug>
       source: <slug>
     ---
     Preserve all existing prose/images/headings. Do not rewrite bodies.
   - index.html-only lessons: prepend HTML comment YAML (NO README.md sidecar — that would break Learnfeed ingest):
     <!--
     filters:
       topic:
         - <slug>
       format: <slug>
       source: <slug>
     -->
     immediately before <!DOCTYPE html>. Zero changes to lesson prose.

3. Prefer a reliable bulk apply script (Python/Node/PowerShell) driven by the corrected CSV, then spot-check 15–20 lessons by reading content. Fix validate_tags.py if incomplete.

4. Write permanent docs:
   - C:\Users\san\Projects\crosslearn\docs\content-filters.md
     Include: groups, allowed values, examples, frontmatter + HTML comment schemas, how LearnFeed/Expo should consume later (manifest.filters), omit rejected dimensions (effort/skill_level chips) with rationale.
   - Also copy/adapt the same doc into C:\Users\san\Projects\learnfeed\docs\content-filters.md when you sync (or leave a note that learnfeed copy lands after sync). Prefer writing crosslearn docs now; learnfeed docs after ingest update.

5. Run validate_tags.py — must report 264/264 valid. Fix any failures.

6. Git on crosslearn (C:\Users\san\Projects\crosslearn):
   - Do NOT commit _catalog-skim.csv, _ag-content-filters/ working scratch if huge logs — either gitignore _ag-content-filters/ or commit only useful artifacts (PLAN.md, final tags csv, validate script) under docs/ or scripts/. Prefer: keep validate script + taxonomy in docs/; put apply tooling under scripts/content-filters/ if useful; gitignore _ag-content-filters/*.log and _catalog-skim.csv.
   - Commit with a clear message about content filters taxonomy + tagging all lessons.
   - git push origin main (continuous push required). Do NOT trigger Pages publish workflows beyond normal push to private/main content.

7. After crosslearn push succeeds, update LearnFeed ingest so filters survive sync:
   - C:\Users\san\Projects\learnfeed\packages\content\scripts\lib\parse-lessons.mjs — parse YAML frontmatter from README and HTML comment filters from index.html; attach `filters` on lesson meta; strip frontmatter from generated markdown body (so reader doesn't show --- filters ---).
   - C:\Users\san\Projects\learnfeed\packages\content\src\types.ts — add optional/required filters schema (topic string[], format string, source string) with zod.
   - Update tests if present.
   - Point CROSSLEARN_ROOT at C:\Users\san\Projects\crosslearn OR run content:sync carefully (sync.mjs resets vendor from origin — after push, sync is fine). Prefer: set CROSSLEARN_ROOT=C:\Users\san\Projects\crosslearn and run npm run content:ingest from learnfeed root so generated manifest includes filters without fighting vendor.
   - Commit + push learnfeed generated updates + ingest/type changes + docs/content-filters.md.

8. Final report file: C:\Users\san\Projects\crosslearn\_ag-content-filters\REPORT.md with taxonomy, counts tagged, commit SHAs both repos, sample frontmatter, any untagged leftovers.

Work autonomously end-to-end. Use --dangerously-skip-permissions already granted. High quality over speed on classification.
