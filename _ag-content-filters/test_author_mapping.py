import csv
import re
from collections import Counter

# Let's inspect the distribution of authors
with open('_ag-content-filters/draft-tags.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

# Map author string to canonical source slug
def get_source_slug(slug, author_str):
    a = author_str.lower()
    if 'shreyas' in a: return 'shreyas-doshi'
    if 'cutler' in a: return 'john-cutler'
    if 'samsonov' in a: return 'pavel-samsonov'
    if 'dunford' in a: return 'april-dunford'
    if 'george' in a or 'nurijanian' in a: return 'george-nurijanian'
    if 'zhuo' in a: return 'julie-zhuo'
    if 'scrum' in a or 'jocham' in a: return 'scrum-org'
    if 'perri' in a: return 'melissa-perri'
    if 'biddle' in a: return 'gibson-biddle'
    if 'gilad' in a: return 'itamar-gilad'
    if 'graham' in a: return 'molly-graham'
    if 'torres' in a: return 'teresa-torres'
    if 'bastow' in a: return 'janna-bastow'
    if 'huryn' in a: return 'pawel-huryn'
    if 'des traynor' in a or 'intercom' in a: return 'des-traynor'
    if 'claire vo' in a or 'vo' in a: return 'claire-vo'
    if 'cagan' in a: return 'marty-cagan'
    if 'charles' in a: return 'geoff-charles'
    if 'stein' in a: return 'ryan-stein'
    if 'cat wu' in a or 'wu' in a: return 'cat-wu'
    if 'nash' in a: return 'adam-nash'
    if 'vivanco' in a: return 'alejandro-vivanco'
    if 'grant lee' in a: return 'grant-lee'
    if 'spielman' in a: return 'jason-spielman'
    if 'rauch' in a: return 'guillermo-rauch'
    if 'abel' in a: return 'jen-abel'
    if 'nan yu' in a: return 'nan-yu'
    if 'tobias' in a: return 'martin-tobias'
    if 'pai' in a: return 'sajith-pai'
    if 'lenny' in a: return 'lenny-rachitsky'
    return 'unknown'

counts = Counter()
for r in rows:
    src = get_source_slug(r['slug'], r['source_author'])
    counts[src] += 1

print("Source slug counts:")
for s, c in counts.most_common():
    print(f"  {s:22}: {c}")
