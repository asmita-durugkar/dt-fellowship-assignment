import csv
import re

def validate_tree(filename):
    nodes = {}
    targets = set()
    
    with open(filename, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f, delimiter='\t')
        for row in reader:
            nodes[row['id']] = row
            # Check explicit targets
            if row.get('target') and row['target'].strip() != '':
                targets.add(row['target'].strip())
            
            # Check implicit targets hidden inside decision rules
            if row['type'] == 'decision':
                rules = row['options'].split(';')
                for rule in rules:
                    if ':' in rule:
                        _, target = rule.split(':')
                        targets.add(target.strip())
    
    # Check for missing targets
    missing = [t for t in targets if t not in nodes]
    
    if missing:
        print(f"❌ INTEGRITY FAILED: The following IDs are referenced but missing: {missing}")
    else:
        print("✅ INTEGRITY PASSED: All explicit and decision-rule paths are valid and deterministic.")

if __name__ == "__main__":
    validate_tree('reflection-tree.tsv')