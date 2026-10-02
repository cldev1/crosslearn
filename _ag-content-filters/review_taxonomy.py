import csv

with open('_ag-content-filters/draft-tags.csv', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if any(k in r['slug'] for k in ['236', '240', '241', '242', '243', '218', '219', '220', '221', '244']):
            print(f"{r['slug']:40} | {r['source_slug']:20} | {r['source_author']}")
