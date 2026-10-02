import csv
import glob
import os
import re

def load_lessons():
    catalog_dir = '.'
    dirs = [d for d in os.listdir(catalog_dir) if re.match(r'^\d{2,3}-[a-z0-9-]+$', d, re.I)]
    dirs.sort(key=lambda s: int(s.split('-')[0]))

    lessons = {}
    for slug in dirs:
        p_readme = os.path.join(slug, 'README.md')
        p_html = os.path.join(slug, 'index.html')
        is_html = not os.path.exists(p_readme) and os.path.exists(p_html)
        fpath = p_html if is_html else p_readme

        with open(fpath, encoding='utf-8', errors='ignore') as f:
            content = f.read()

        title = ''
        if is_html:
            m_h1 = re.search(r'<h1>([^<]+)</h1>', content)
            if m_h1: title = m_h1.group(1).strip()
        else:
            m_h1 = re.search(r'^#\s+(.+)$', content, re.M)
            if m_h1: title = m_h1.group(1).strip()

        claim = ''
        m_c = re.search(r'##\s+What it claims\s*\n+([\s\S]*?)(?=\n##|\n#|$)', content)
        if not m_c: m_c = re.search(r'<h2>What it claims</h2>\s*<p>([\s\S]*?)</p>', content)
        if m_c: claim = re.sub(r'<[^>]+>', '', m_c.group(1)).strip()

        why = ''
        m_w = re.search(r'##\s+Why it matters for a PO\s*\n+([\s\S]*?)(?=\n##|\n#|$)', content)
        if not m_w: m_w = re.search(r'<h2>Why it matters for a PO</h2>\s*<p>([\s\S]*?)</p>', content)
        if m_w: why = re.sub(r'<[^>]+>', '', m_w.group(1)).strip()

        takeaways = ''
        m_t = re.search(r'##\s+3 takeaways\s*\n+([\s\S]*?)(?=\n##|\n#|$)', content)
        if not m_t: m_t = re.search(r'<h2>3 takeaways</h2>\s*([\s\S]*?)(?=<h2>|$)', content)
        if m_t: takeaways = re.sub(r'<[^>]+>', '', m_t.group(1)).strip()

        author_str = ''
        m_s = re.search(r'<strong>Source:</strong>\s*([^<\n]+)', content)
        if m_s: author_str = m_s.group(1).strip()
        else:
            m_s2 = re.search(r'\*\*Source:\*\*\s*([^\n]+)', content)
            if m_s2: author_str = m_s2.group(1).strip()

        lessons[slug] = {
            'slug': slug,
            'order': int(slug.split('-')[0]),
            'title': title,
            'author_str': author_str,
            'claim': claim,
            'why': why,
            'takeaways': takeaways,
            'is_html': is_html,
            'content': content
        }
    return lessons

def load_draft():
    with open('_ag-content-filters/draft-tags.csv', encoding='utf-8') as f:
        return {r['slug']: r for r in csv.DictReader(f)}

if __name__ == '__main__':
    lessons = load_lessons()
    draft = load_draft()
    print(f"Loaded {len(lessons)} lessons and {len(draft)} draft tags.")
