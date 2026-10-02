import csv

with open('_ag-content-filters/draft-tags.csv', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        num = int(r['slug'].split('-')[0])
        if 108 <= num <= 128:
            print(f"{r['slug']:35} | {r['source_slug']:18} | {r['source_author']}")
