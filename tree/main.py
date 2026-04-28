import csv
import re

class ReflectionAgent:
    def __init__(self, tsv_file):
        self.tree = {}
        self.state = {"answers": {}, "signals": {}}
        self._load_tree(tsv_file)

    def _load_tree(self, tsv_file):
        with open(tsv_file, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f, delimiter='\t')
            for row in reader:
                # GUARDRAIL: Sanitize None values caused by missing trailing tabs in the TSV
                for key in row:
                    if row[key] is None:
                        row[key] = ''
                self.tree[row['id']] = row

    def _get_child(self, parent_id):
        for node_id, node in self.tree.items():
            if node['parentId'] == parent_id:
                return node_id
        return None

    def run(self):
        print("--- Daily Reflection Tree Initiated ---\n")
        current_node_id = "START"
        
        while current_node_id and current_node_id in self.tree:
            node = self.tree[current_node_id]
            
            # --- 1. Track Psychological Signals ---
            signal_str = node.get('signal', '').strip()
            if signal_str and ':' in signal_str:
                axis, pole = signal_str.split(':')
                if axis not in self.state['signals']:
                    self.state['signals'][axis] = {}
                self.state['signals'][axis][pole] = self.state['signals'][axis].get(pole, 0) + 1
                
            # --- 2. Interpolate Previous Answers into Text ---
            text = node.get('text', '')
            for key, val in self.state['answers'].items():
                text = text.replace(f"{{{key}.answer}}", val)
            
            # --- 3. Process the Specific Node Type ---
            if node['type'] == 'start':
                print(f">> {text}")
                current_node_id = node.get('target', '').strip() or self._get_child(current_node_id)
                
            elif node['type'] == 'question':
                print(f"\n{text}")
                options = node['options'].split('|')
                for i, opt in enumerate(options, 1):
                    print(f"{i}. {opt}")
                
                try:
                    choice = int(input(f"\nSelect an option (1-{len(options)}): ")) - 1
                    if choice < 0 or choice >= len(options):
                        print("Invalid selection. Please try again.")
                        continue
                    
                    answer = options[choice]
                    self.state['answers'][node['id']] = answer
                    current_node_id = node.get('target', '').strip() or self._get_child(current_node_id)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    continue
                    
            elif node['type'] == 'decision':
                parent_id = node['parentId']
                parent_answer = self.state['answers'].get(parent_id, "")
                rules = node['options'].split(';')
                
                next_id = None
                for rule in rules:
                    if ':' not in rule: continue
                    conditions_str, target = rule.split(':')
                    conditions = [c.strip() for c in conditions_str.replace('answer=', '').split('|')]
                    
                    if parent_answer.strip() in conditions:
                        next_id = target.strip()
                        break
                        
                current_node_id = next_id or node.get('target', '').strip() or self._get_child(current_node_id)
                
            elif node['type'] in ['reflection', 'bridge']:
                print(f"\n>> {text}")
                if node['type'] == 'reflection':
                    input("\n(Press Enter to continue...)")
                current_node_id = node.get('target', '').strip() or self._get_child(current_node_id)
                
            elif node['type'] == 'summary':
                for axis, poles in self.state['signals'].items():
                    dominant = max(poles, key=poles.get) if poles else ""
                    text = text.replace(f"{{{axis}.dominant}}", dominant)
                text = re.sub(r'\{.*?\}', '', text)
                    
                print(f"\n--- Summary ---\n{text.strip()}")
                current_node_id = node.get('target', '').strip() or self._get_child(current_node_id)
                
            elif node['type'] == 'end':
                print(f"\n{text}")
                break
                
            else:
                current_node_id = self._get_child(current_node_id)

if __name__ == "__main__":
    try:
        agent = ReflectionAgent('reflection-tree.tsv')
        agent.run()
    except Exception as e:
        print(f"CRITICAL ERROR: {e}")