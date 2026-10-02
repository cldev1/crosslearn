import csv
import json
import os
import re
from collections import Counter

# Load lessons
catalog_dir = '.'
dirs = [d for d in os.listdir(catalog_dir) if re.match(r'^\d{2,3}-[a-z0-9-]+$', d, re.I)]
dirs.sort(key=lambda s: int(s.split('-')[0]))

lessons = []
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

    practice = ''
    m_p = re.search(r'##\s+Practice this week\s*\n+([\s\S]*?)(?=\n##|\n#|$)', content)
    if not m_p: m_p = re.search(r'<h2>Practice this week</h2>\s*<p>([\s\S]*?)</p>', content)
    if m_p: practice = re.sub(r'<[^>]+>', '', m_p.group(1)).strip()

    author_str = ''
    m_s = re.search(r'<strong>Source:</strong>\s*([^<\n]+)', content)
    if m_s: author_str = m_s.group(1).strip()
    else:
        m_s2 = re.search(r'\*\*Source:\*\*\s*([^\n]+)', content)
        if m_s2: author_str = m_s2.group(1).strip()

    lessons.append({
        'slug': slug,
        'order': int(slug.split('-')[0]),
        'title': title,
        'author_str': author_str,
        'claim': claim,
        'why': why,
        'takeaways': takeaways,
        'practice': practice,
        'is_html': is_html,
        'content': content
    })

def resolve_source(slug, author_str):
    a = author_str.lower()
    if 'shreyas' in a: return 'shreyas-doshi'
    if 'cutler' in a: return 'john-cutler'
    if 'samsonov' in a: return 'pavel-samsonov'
    if 'dunford' in a: return 'april-dunford'
    if 'george' in a or 'nurijanian' in a: return 'george-nurijanian'
    if 'zhuo' in a: return 'julie-zhuo'
    if 'scrum' in a or 'jocham' in a or 'deneir' in a or 'wolpers' in a or 'iqbal' in a: return 'scrum-org'
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

print("Engine base ready. Analyzing taxonomy...")
