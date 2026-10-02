import csv
import sys
import re

sys.stdout.reconfigure(encoding='utf-8')

with open('_ag-content-filters/draft-tags.csv', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

def inspect_author(author_slug):
    author_rows = [r for r in rows if r['source_slug'] == author_slug]
    print(f"\n=== {author_slug.upper()} ({len(author_rows)} lessons) ===")
    for r in author_rows:
        print(f"{r['slug']:38} | {r['format']:12} | {r['topics']:30} | {r['title']}")

# Let's inspect some authors
if __name__ == '__main__':
    target = sys.argv[1] if len(sys.argv) > 1 else 'gibson-biddle'
    inspect_author(target)
