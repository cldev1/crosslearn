import csv
from test_author_mapping import get_source_slug

with open('_ag-content-filters/draft-tags.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

lenny_lessons = [r['slug'] for r in rows if get_source_slug(r['slug'], r['source_author']) == 'lenny-rachitsky']
print(f"Lenny lessons ({len(lenny_lessons)}):", lenny_lessons)
