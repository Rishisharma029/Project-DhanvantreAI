import re
import ast

def normalize_string(val: str) -> str:
    """Normalize general text strings: strip whitespace and reduce double spaces."""
    if not val or not isinstance(val, str):
        return ""
    val = val.strip()
    val = re.sub(r'\s+', ' ', val)
    return val

def standardize_unit_and_strength(strength_str: str, unit_str: str = "") -> tuple:
    """
    Standardize strength and dosage units consistently:
    - 500mg -> (500.0, 'mg')
    - 0.5 g -> (500.0, 'mg')
    - 1000 mcg -> (1.0, 'mg')
    - 5 ml -> (5.0, 'ml')
    """
    text = f"{strength_str} {unit_str}".strip().lower()
    if not text:
        return (None, "")

    # Match patterns like "0.5 g", "500 mg", "1000mcg", "5ml"
    match = re.search(r'([\d\.]+)\s*(mg|g|mcg|microgram|gram|ml|l|iu|%|v/v|w/v)?', text)
    if not match:
        return (None, unit_str.strip().lower())

    val = float(match.group(1))
    u = (match.group(2) or unit_str).strip().lower()

    if u in ('g', 'gram', 'grams'):
        return (val * 1000.0, 'mg')
    elif u in ('mcg', 'microgram', 'micrograms'):
        return (val / 1000.0, 'mg')
    elif u in ('l', 'liter', 'liters'):
        return (val * 1000.0, 'ml')
    elif u in ('mg', 'milligram', 'milligrams'):
        return (val, 'mg')
    elif u in ('ml', 'milliliter', 'milliliters'):
        return (val, 'ml')
    else:
        return (val, u)

def get_canonical_medicine_key(name: str) -> str:
    """
    Generate a canonical deduplication key for medicine names.
    Examples:
    - 'Paracetamol 500mg Tablet' -> 'paracetamol 500 mg'
    - 'Paracetamol Tablet 500 mg' -> 'paracetamol 500 mg'
    - 'Paracetamol Tab 500mg'    -> 'paracetamol 500 mg'
    """
    if not name or not isinstance(name, str):
        return ""

    s = name.strip().lower()
    # Replace dosage abbreviations
    s = re.sub(r'\b(tab|tablet|tablets|cap|capsule|capsules|syrup|syr|inj|injection|susp|suspension|drop|drops|gel|cream|ointment)\b', '', s)
    # Normalize strength spaces e.g. 500mg -> 500 mg
    s = re.sub(r'(\d+)\s*(mg|g|mcg|ml|iu|%)', r'\1 \2', s)
    # Remove punctuation except numbers and letters
    s = re.sub(r'[^\w\s]', '', s)
    # Sort remaining tokens to handle order variations (e.g. Paracetamol 500mg vs 500mg Paracetamol)
    tokens = sorted([t for t in s.split() if t])
    return " ".join(tokens)

def parse_composition(comp_str: str) -> list:
    """
    Parse composition strings like:
    - 'Amoxycillin (500mg) + Clavulanic Acid (125mg)'
    - 'Paracetamol 500 mg, Phenylephrine 10 mg'
    Returns a list of dicts: [{'ingredient': 'Amoxycillin', 'strength': 500.0, 'unit': 'mg'}, ...]
    """
    if not comp_str or not isinstance(comp_str, str):
        return []

    results = []
    # Split by '+' or ',' or '/'
    parts = re.split(r'[\+\,\/]', comp_str)
    for part in parts:
        part = part.strip()
        if not part: continue
        
        # Match 'Ingredient (500mg)' or 'Ingredient 500 mg'
        match = re.search(r'([A-Za-z0-9\s\-]+?)\s*\(?\s*([\d\.]+)\s*(mg|g|mcg|ml|iu|%)?\s*\)?', part)
        if match:
            ing_name = normalize_string(match.group(1))
            st_val = match.group(2)
            u_val = match.group(3) or ''
            st_num, st_unit = standardize_unit_and_strength(st_val, u_val)
            if ing_name and len(ing_name) > 1:
                results.append({
                    'ingredient': ing_name,
                    'strength': st_num,
                    'unit': st_unit
                })
        else:
            clean_ing = normalize_string(part)
            if clean_ing and len(clean_ing) > 1:
                results.append({
                    'ingredient': clean_ing,
                    'strength': None,
                    'unit': ''
                })
    return results

def classify_interaction_severity(desc: str) -> tuple:
    """
    Classify interaction description into severity: Major, Moderate, Minor, Unknown
    Returns (severity_string, indicator_emoji)
    """
    if not desc:
        return ('Unknown', '⚪')
    
    d_lower = desc.lower()
    if any(k in d_lower for k in ['life-threatening', 'fatal', 'severe', 'avoid', 'contraindicated', 'major', 'increase photosensitizing', 'toxic', 'risk of bleeding']):
        return ('Major', '🔴 Dangerous')
    elif any(k in d_lower for k in ['moderate', 'decrease efficacy', 'monitor', 'caution', 'alter', 'adjust dose', 'increase concentration']):
        return ('Moderate', '🟡 Caution')
    elif any(k in d_lower for k in ['minor', 'slight', 'minimal', 'unlikely']):
        return ('Minor', '🟢 Safe')
    else:
        return ('Moderate', '🟡 Caution')

def clean_price(price_str) -> float:
    """Extract float value from price string."""
    if not price_str:
        return 0.0
    try:
        clean_str = re.sub(r'[^\d\.]', '', str(price_str))
        val = float(clean_str) if clean_str else 0.0
        return val if val > 0 else 0.0
    except (ValueError, TypeError):
        return 0.0

def clean_boolean(val) -> bool:
    """Convert text/int to boolean."""
    if isinstance(val, bool):
        return val
    if not val:
        return False
    val_str = str(val).strip().upper()
    return val_str in ('TRUE', '1', 'YES', 'Y')

def parse_list_str(val: str) -> list:
    """Parse string representations of Python lists e.g. \"['item1', 'item2']\"."""
    if not val:
        return []
    val = val.strip()
    if val.startswith('[') and val.endswith(']'):
        try:
            parsed = ast.literal_eval(val)
            if isinstance(parsed, list):
                return [normalize_string(str(item)) for item in parsed if item]
        except Exception:
            pass
    return [normalize_string(item) for item in val.split(',') if item.strip()]

def clean_symptom_name(symptom: str) -> str:
    """Standardize symptom names (strip underscores, lowercase)."""
    if not symptom:
        return ""
    s = symptom.strip().replace('_', ' ').lower()
    s = re.sub(r'\s+', ' ', s)
    return s

def clean_disease_name(disease: str) -> str:
    """Standardize disease names."""
    if not disease:
        return ""
    d = disease.strip()
    d = re.sub(r'\s+', ' ', d)
    return d.title()
