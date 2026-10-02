import csv
import os
import re
import sys
from collections import Counter

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

# Load current draft as starting baseline
with open('_ag-content-filters/draft-tags.csv', encoding='utf-8') as f:
    draft_rows = {r['slug']: r for r in csv.DictReader(f)}

print(f"Loaded {len(draft_rows)} lessons from draft-tags.csv")
