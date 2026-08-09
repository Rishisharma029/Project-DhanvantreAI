import sys
import pprint

sys.path.insert(0, '.')
from app.data.syndrome_kb import SYNDROME_KB
from scratch.batch_2_gi import BATCH_2_GI
from scratch.batch_2_neuro import BATCH_2_NEURO
from scratch.batch_2_id import BATCH_2_ID

# To prevent duplicates if run multiple times, check syndrome_id
existing_ids = {s['syndrome_id'] for s in SYNDROME_KB}

for s in BATCH_2_GI + BATCH_2_NEURO + BATCH_2_ID:
    if s['syndrome_id'] not in existing_ids:
        SYNDROME_KB.append(s)

with open('app/data/syndrome_kb.py', 'w') as f:
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
