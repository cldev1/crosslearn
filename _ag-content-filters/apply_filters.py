import csv
import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

# Load the corrected draft-tags.csv
with open('_ag-content-filters/draft-tags.csv', encoding='utf-8') as f:
    tags = {r['slug']: r for r in csv.DictReader(f)}

print(f"Applying filters to {len(tags)} lessons...")

updated_md = 0
updated_html = 0

for slug, data in sorted(tags.items(), key=lambda x: int(x[0].split('-')[0])):
    readme_path = os.path.join(slug, 'README.md')
    html_path = os.path.join(slug, 'index.html')
    has_readme = os.path.exists(readme_path)
    has_html = os.path.exists(html_path)

    topics = data['topics'].split(';')
    fmt = data['format']
    source = data['source_slug']

    # Build YAML snippet
    yaml_lines = ["filters:", "  topic:"]
    for t in topics:
        yaml_lines.append(f"    - {t}")
    yaml_lines.append(f"  format: {fmt}")
    yaml_lines.append(f"  source: {source}")
    yaml_body = "\n".join(yaml_lines)

    # Retired lessons are redirect stubs; leave their filters (retired/redirect_to) alone.
    if not has_readme and has_html:
        with open(html_path, 'r', encoding='utf-8') as f:
            if 'name="crosslearn-retired"' in f.read():
                continue

    if has_readme:
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # If already has frontmatter, replace it
        if content.startswith('---'):
            content = re.sub(r'^---\r?\n[\s\S]*?\r?\n---\r?\n', '', content)

        new_content = f"---\n{yaml_body}\n---\n\n{content.lstrip()}"
        with open(readme_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)
        updated_md += 1

    elif has_html:
        with open(html_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # If already has HTML comment filters, replace it
        if content.startswith('<!--'):
            content = re.sub(r'^<!--\r?\n[\s\S]*?\r?\n-->\r?\n', '', content)

        new_content = f"<!--\n{yaml_body}\n-->\n{content.lstrip()}"
        with open(html_path, 'w', encoding='utf-8', newline='\n') as f:
            f.write(new_content)
        updated_html += 1
    else:
        print(f"ERROR: {slug} has neither README.md nor index.html!")

print(f"Done! Updated {updated_md} README.md files and {updated_html} index.html files. Total: {updated_md + updated_html}")
