import sys
import pprint

sys.path.insert(0, '.')
from app.data.syndrome_kb import SYNDROME_KB

for s in SYNDROME_KB:
    new_diffs = []
    for d in s.get('differentials', []):
        if isinstance(d, str):
            new_diffs.append({
                "disease_name": d,
                "probability": 0.40,
                "status": "RULED_IN",
                "icd11_code": "UNKNOWN",
                "supporting": s.get('required_keywords', [])[:3],
                "missing": []
            })
        else:
            new_diffs.append(d)
    s['differentials'] = new_diffs

with open('app/data/syndrome_kb.py', 'w', encoding='utf-8') as f:
    f.write('"""\nAuraMed AI - Syndrome Knowledge Base\nHigh Quality Curated Entries\n"""\n')
    f.write('from typing import Dict, Any, List\n\n')
    f.write('SYNDROME_KB: List[Dict[str, Any]] = [\n')
    
    for i, s in enumerate(SYNDROME_KB):
        f.write('    ')
        # Format neatly
        f.write(pprint.pformat(s, indent=4, sort_dicts=False).replace('\n', '\n    '))
        if i < len(SYNDROME_KB) - 1:
            f.write(',\n')
        else:
            f.write('\n')
    f.write(']\n')
