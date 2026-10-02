import os, glob, re, csv, sys
from collections import Counter, defaultdict

sys.stdout.reconfigure(encoding='utf-8')

with open('_catalog-skim.csv', encoding='utf-8') as f:
    rows = list(csv.reader(f))[1:]

lessons = []
for r in rows:
    slug, title, src = r[0].strip(), r[1].strip(), r[2].strip()
    p_readme = os.path.join(slug, 'README.md')
    p_html = os.path.join(slug, 'index.html')
    text = ''
    ftype = 'readme' if os.path.exists(p_readme) else 'html'
    fpath = p_readme if ftype == 'readme' else p_html
    if os.path.exists(fpath):
        with open(fpath, encoding='utf-8', errors='ignore') as f:
            text = f.read()

    if ftype == 'html':
        h1 = re.search(r'<h1>([^<]+)</h1>', text)
        if h1: title = h1.group(1).strip()
    
    author = src
    if not author or not author.strip():
        m_src = re.search(r'<strong>Source:</strong>\s*([^<]+)', text)
        if m_src: author = m_src.group(1).strip()
        else:
            m_src2 = re.search(r'\*\*Source:\*\*\s*([^\n]+)', text)
            if m_src2: author = m_src2.group(1).strip()

    claim = ''
    m = re.search(r'##\s+What it claims\s*\n+([\s\S]*?)(?=\n##|\n#|$)', text)
    if not m: m = re.search(r'<h2>What it claims</h2>\s*<p>([\s\S]*?)</p>', text)
    if m: claim = re.sub(r'<[^>]+>', '', m.group(1)).strip()

    why = ''
    m_why = re.search(r'##\s+Why it matters for a PO\s*\n+([\s\S]*?)(?=\n##|\n#|$)', text)
    if not m_why: m_why = re.search(r'<h2>Why it matters for a PO</h2>\s*<p>([\s\S]*?)</p>', text)
    if m_why: why = re.sub(r'<[^>]+>', '', m_why.group(1)).strip()

    takeaways = ''
    m_t = re.search(r'##\s+3 takeaways\s*\n+([\s\S]*?)(?=\n##|\n#|$)', text)
    if not m_t: m_t = re.search(r'<h2>3 takeaways</h2>\s*([\s\S]*?)(?=<h2>|$)', text)
    if m_t: takeaways = re.sub(r'<[^>]+>', '', m_t.group(1)).strip()

    full_text = f"{title} {claim} {why} {takeaways}".lower()
    words = len(text.split())

    lessons.append({
        'slug': slug,
        'title': title,
        'author': author,
        'ftype': ftype,
        'claim': claim,
        'why': why,
        'words': words,
        'text': full_text
    })

def normalize_author(author):
    a = author.lower()
    if 'shreyas' in a: return 'shreyas-doshi'
    if 'cutler' in a: return 'john-cutler'
    if 'samsonov' in a: return 'pavel-samsonov'
    if 'dunford' in a: return 'april-dunford'
    if 'lenny' in a: return 'lenny-rachitsky'
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
    if 'abel' in a: return 'jen-abel'
    if 'rauch' in a: return 'guillermo-rauch'
    if 'claire vo' in a or 'vo' in a: return 'claire-vo'
    if 'cat wu' in a or 'wu' in a: return 'cat-wu'
    if 'nash' in a: return 'adam-nash'
    if 'cagan' in a: return 'marty-cagan'
    if 'spielman' in a: return 'jason-spielman'
    if 'vivanco' in a: return 'alejandro-vivanco'
    if 'grant lee' in a: return 'grant-lee'
    if 'tobias' in a: return 'martin-tobias'
    if 'pai' in a: return 'sajith-pai'
    if 'charles' in a: return 'geoff-charles'
    if 'stein' in a: return 'ryan-stein'
    if 'nan yu' in a: return 'nan-yu'
    return 'other'

def classify_format(l):
    t = l['text']
    title = l['title'].lower()
    
    if any(k in title for k in ['test', 'tests', 'checklist', 'questions before', 'signals of a', 'commandments', 'habits']):
        return 'playbook'
    if any(k in title for k in ['how to', 'script', 'pre-mortem', 'register', 'walkthrough-five-moves', 'forced order', 'practice this week']):
        return 'playbook'
    if any(k in title for k in ['anti-pattern', 'paradox', 'delusion', 'trap', 'fallacy', 'wounds', 'factory', 'snake oil', 'dysfunction', 'theatre', 'theater', 'false predictability', 'bad ideas', 'armchair', 'not a metric', 'hurts hiring']):
        return 'anti-pattern'
    if any(k in t for k in ['anti-pattern', 'preventable problem paradox', 'proxy delusion', 'feature factory', 'build trap']):
        return 'anti-pattern'
    if any(k in title for k in ['framework', 'matrix', 'model', '3x', 'dhm', 'gem', 'glee', 'lno', 'invest', 'cpsr', 'five components', '70/20/10', 'three levels', 'shapes of work', 'four modes', 'inputs → chat → outputs', 'two fits']):
        return 'framework'
    if any(k in t for k in ['dhm stack', 'gem framework', 'lno framework', '70/20/10', 'explore, expand, extract']):
        return 'framework'
    return 'principle'

topic_keywords = {
    'positioning': [
        'positioning', 'category', 'differentiated value', 'competitive alternative',
        'sales pitch', 'april dunford', 'position competitors', 'market category', 'value themes'
    ],
    'strategy': [
        'strategy', 'vision', 'glee', 'dhm', 'strategic', 'trade-offs', 'tradeoffs',
        'eigenquestion', 'cpsr', 'gorilla taxes', 'competitive advantage', 'bets', 'bet'
    ],
    'discovery': [
        'discovery', 'customer interview', 'interviews', 'assumption test', 'user research',
        'ost', 'opportunity solution', 'ux research', 'observe first', 'proxies not research',
        'teresa torres', 'jtbd', 'opportunity mapping'
    ],
    'roadmaps-prioritization': [
        'roadmap', 'roadmaps', 'prioritization', 'prioritize', 'backlog', 'feature buckets',
        '70/20/10', 'branching roadmaps', 'rejection register', 'force-rank', 'ranking', 'prio'
    ],
    'delivery-execution': [
        'delivery', 'sprint', 'sprints', 'tech debt', 'feature factory', 'scrum',
        'user stories', 'invest', 'dual-track', 'shipping', 'deprecation', 'backlog secretary',
        'build trap', 'execution', 'wip limits', 'refinement'
    ],
    'metrics-analytics': [
        'metric', 'metrics', 'okr', 'okrs', 'goodhart', 'proxy delusion', 'measurement',
        'data-informed', 'north star', 'outcomes vs', 'leading indicator', 'nps', 'a/b test'
    ],
    'leadership-org': [
        'leadership', 'manager', 'executives', 'influence exec', 'org', 'culture',
        'hiring', 'team trust', 'spare capacity', 'hero culture', 'conflict',
        'giving away your legos', 'molly graham', 'managing up', 'director'
    ],
    'career-habits': [
        'habits', 'high agency', 'lno', 'time principles', 'career', 'intuition',
        'first 30-60-90', 'eng-turned-pm', 'ic to pm', 'operator / craftsperson', 'burnout'
    ],
    'ai-product': [
        'ai', 'llm', 'llms', 'gpt', 'anthropic', 'openai', 'eval', 'evals',
        'agi', 'agent', 'use-case map before ask agent', 'bad ideas', 'ai-path', 'inputs → chat'
    ]
}

def classify_topics(l):
    text = l['text']
    title = l['title'].lower()
    author = l['author'].lower()
    
    if 'dunford' in author:
        return ['positioning'] if 'strategy' not in title else ['positioning', 'strategy']
    
    scores = {}
    for topic, kws in topic_keywords.items():
        score = 0
        for kw in kws:
            if len(kw) <= 3:
                pattern = r'\b' + re.escape(kw) + r'\b'
                if re.search(pattern, title): score += 4
                elif re.search(pattern, text): score += 1.5
            else:
                if kw in title: score += 3
                elif kw in text: score += 1
        scores[topic] = score
    
    ranked = sorted([(t, s) for t, s in scores.items() if s >= 2.5], key=lambda x: x[1], reverse=True)
    if not ranked:
        ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    selected = [ranked[0][0]]
    if len(ranked) > 1 and ranked[1][1] >= 3.0:
        selected.append(ranked[1][0])
    return selected

output_file = os.path.join('_ag-content-filters', 'draft-tags.csv')
with open(output_file, 'w', encoding='utf-8', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['slug', 'title', 'source_author', 'source_slug', 'format', 'topics', 'file_type'])
    for l in lessons:
        s_slug = normalize_author(l['author'])
        fmt = classify_format(l)
        topics = classify_topics(l)
        writer.writerow([l['slug'], l['title'], l['author'], s_slug, fmt, ';'.join(topics), l['ftype']])

print(f"Draft tags CSV generated successfully: {output_file} ({len(lessons)} rows)")
