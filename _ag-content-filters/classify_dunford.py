import csv
import sys
sys.stdout.reconfigure(encoding='utf-8')

with open('_ag-content-filters/draft-tags.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

dunford_slugs = [r['slug'] for r in rows if r['source_slug'] == 'april-dunford']
print(f"Total Dunford lessons: {len(dunford_slugs)}")

# Let's read their title and claim
for s in dunford_slugs:
    p = f"{s}/README.md"
    with open(p, encoding='utf-8') as f:
        content = f.read()
    title = content.split('\n')[0].replace('# ', '')
    print(f"{s}: {title}")
