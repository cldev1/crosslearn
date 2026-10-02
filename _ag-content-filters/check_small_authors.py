import csv

with open('_ag-content-filters/draft-tags.csv', encoding='utf-8') as f:
    for r in csv.DictReader(f):
        if r['source_slug'] in ['other', 'cat-wu', 'adam-nash', 'alejandro-vivanco', 'grant-lee', 
                                'jason-spielman', 'guillermo-rauch', 'jen-abel', 'nan-yu', 
                                'martin-tobias', 'sajith-pai', 'pawel-huryn', 'claire-vo',
                                'marty-cagan', 'geoff-charles', 'ryan-stein']:
            print(f"{r['slug']:35} | {r['source_slug']:18} | {r['source_author']}")
