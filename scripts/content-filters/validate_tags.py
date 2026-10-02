"""
Validation harness for CrossLearn content filters.
Checks all 264 lessons for valid filters and vocabulary conformance.
Zero external dependencies (does not require pyyaml).

Priority rule (matches LearnFeed ingest):
- If README.md exists (199 lessons), check YAML frontmatter in README.md.
- If only index.html exists (65 lessons), check YAML HTML comment in index.html.
"""

import os
import re
import sys

sys.stdout.reconfigure(encoding='utf-8')

VALID_TOPICS = {
    'strategy',
    'positioning',
    'discovery',
    'roadmaps-prioritization',
    'delivery-execution',
    'metrics-analytics',
    'leadership-org',
    'career-habits',
    'ai-product'
}

VALID_FORMATS = {
    'principle',
    'framework',
    'anti-pattern',
    'playbook'
}

def parse_simple_yaml_filters(yaml_str):
    """Parses simple filters YAML block without requiring PyYAML."""
    filters = {}
    lines = [line.rstrip() for line in yaml_str.splitlines() if line.strip() and not line.strip().startswith('#')]
    
    current_key = None
    in_filters = False

    for line in lines:
        stripped = line.strip()
        if stripped == 'filters:':
            in_filters = True
            continue
        if not in_filters:
            continue
        
        # List item under current_key (e.g. "  - strategy")
        list_match = re.match(r'^\s*-\s+([a-z0-9-]+)', line)
        if list_match and current_key:
            val = list_match.group(1)
            if not isinstance(filters.get(current_key), list):
                filters[current_key] = []
            filters[current_key].append(val)
            continue
        
        # Inline array e.g. "  topic: [strategy, discovery]"
        inline_array_match = re.match(r'^\s*([a-z0-9_]+):\s*\[([^\]]*)\]', line)
        if inline_array_match:
            k = inline_array_match.group(1)
            raw_vals = inline_array_match.group(2)
            vals = [v.strip().strip("'\"") for v in raw_vals.split(',') if v.strip()]
            filters[k] = vals
            current_key = None
            continue

        # Key-value e.g. "  format: framework"
        kv_match = re.match(r'^\s*([a-z0-9_]+):\s*(.*)', line)
        if kv_match:
            k = kv_match.group(1)
            v = kv_match.group(2).strip().strip("'\"")
            if v:
                filters[k] = v
                current_key = None
            else:
                current_key = k
                filters[k] = []
            continue

    return filters

def extract_filters(file_path, is_html=False):
    with open(file_path, encoding='utf-8', errors='ignore') as f:
        content = f.read()

    if not is_html:
        match = re.match(r'^---\r?\n([\s\S]*?)\r?\n---', content)
        if not match:
            return None, "Missing YAML frontmatter (--- ... ---)"
        try:
            filters = parse_simple_yaml_filters(match.group(1))
            return filters, None
        except Exception as e:
            return None, f"YAML parse error: {e}"
    else:
        match = re.match(r'^<!--\r?\n([\s\S]*?)\r?\n-->', content)
        if not match:
            return None, "Missing HTML comment YAML block (<!-- ... -->)"
        try:
            filters = parse_simple_yaml_filters(match.group(1))
            return filters, None
        except Exception as e:
            return None, f"HTML comment parse error: {e}"

def validate_catalog(catalog_dir='.'):
    dirs = [d for d in os.listdir(catalog_dir) if re.match(r'^\d{2,3}-[a-z0-9-]+$', d, re.I)]
    dirs.sort(key=lambda s: int(s.split('-')[0]))

    print(f"Validating {len(dirs)} lesson directories...")
    errors = []
    validated = 0

    for slug in dirs:
        dir_path = os.path.join(catalog_dir, slug)
        readme_path = os.path.join(dir_path, 'README.md')
        html_path = os.path.join(dir_path, 'index.html')

        has_readme = os.path.exists(readme_path)
        has_html = os.path.exists(html_path)

        if not has_readme and not has_html:
            errors.append(f"[{slug}] Missing both README.md and index.html")
            continue

        # Ingest precedence: README.md if present, else index.html
        target_file = readme_path if has_readme else html_path
        is_html_target = not has_readme and has_html

        filters, err = extract_filters(target_file, is_html=is_html_target)

        if err:
            errors.append(f"[{slug}] {err}")
            continue

        if not filters:
            errors.append(f"[{slug}] Empty or missing 'filters' key")
            continue

        # Validate topics
        topics = filters.get('topic')
        if not isinstance(topics, list) or len(topics) < 1 or len(topics) > 2:
            errors.append(f"[{slug}] 'topic' must be a list of 1-2 values, got: {topics}")
        else:
            for t in topics:
                if t not in VALID_TOPICS:
                    errors.append(f"[{slug}] Invalid topic '{t}'. Allowed: {sorted(VALID_TOPICS)}")

        # Validate format
        fmt = filters.get('format')
        if not fmt or fmt not in VALID_FORMATS:
            errors.append(f"[{slug}] Invalid format '{fmt}'. Allowed: {sorted(VALID_FORMATS)}")

        # Validate source
        src = filters.get('source')
        if not src or not isinstance(src, str) or not re.match(r'^[a-z0-9-]+$', src):
            errors.append(f"[{slug}] Invalid source slug '{src}' (must be non-empty kebab-case)")

        validated += 1

    print(f"Validation completed: {validated}/{len(dirs)} lessons checked.")
    if errors:
        print(f"\nReported {len(errors)} validation notes (expected before tagging):")
        for e in errors[:5]:
            print(f"  - {e}")
        if len(errors) > 5:
            print(f"  ... and {len(errors) - 5} more.")
        return False
    else:
        print("ALL LESSONS PASSED VALIDATION! Schema and vocabulary are 100% compliant.")
        return True

if __name__ == '__main__':
    catalog_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    success = validate_catalog(catalog_path)
    sys.exit(0 if success else 1)
