import re
from typing import List, Dict, Optional
from collections import defaultdict

class ProcessAnalyzer:
    def __init__(self, adb):
        self.adb = adb

    def get_processes(self, filter_uid: Optional[str] = None) -> List[Dict]:
        raw_output = self.adb.execute_command("ps -A")
        processes = self._parse_process_output(raw_output)

        if filter_uid:
            processes = [p for p in processes if p['UID'] == filter_uid or p['USER'] == filter_uid]

        return processes

    def _parse_process_output(self, raw_output: str) -> List[Dict]:
        lines = raw_output.strip().splitlines()
        processes = []

        header_line = lines[0]
        headers = re.split(r'\s+', header_line.strip())

        
        if 'UID' not in headers and 'USER' in headers:
            headers = [h.replace('USER', 'UID') for h in headers]

        header_indices = {header: i for i, header in enumerate(headers)}

        for line in lines[1:]:
            columns = re.split(r'\s+', line.strip(), len(headers) - 1)
            if len(columns) < len(headers):
                continue

            try:
                process = {
                    'UID': columns[header_indices['UID']],
                    'PID': columns[header_indices['PID']],
                    'PPID': columns[header_indices['PPID']],
                    'NAME': columns[header_indices['NAME']],
                }
                processes.append(process)
            except Exception:
                continue

        return processes

    def build_process_tree(self, processes: List[Dict]) -> Dict:
        tree = defaultdict(list)
        for proc in processes:
            tree[proc['PPID']].append(proc)
        return tree

    def display_process_tree(self, tree: Dict, current_pid: str = '1', level: int = 0):
        children = tree.get(current_pid, [])
        for child in children:
            indent = '  ' * level
            print(f"{indent}- PID: {child['PID']} | PPID: {child['PPID']} | NAME: {child['NAME']}")
            self.display_process_tree(tree, child['PID'], level + 1)
