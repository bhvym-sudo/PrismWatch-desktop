import re
from typing import Dict, List, Tuple

class PackageAnalyzer:
    def __init__(self, adb):
        self.adb = adb

    def get_installed_apps(self) -> List[Tuple[str, str]]:
        output = self.adb.execute_command("pm list packages -U")
        return [
            (parts[0].split(":")[1], parts[1].split(":")[1])
            for line in output.splitlines()
            if line.startswith("package:")
            for parts in [line.split()]
            if len(parts) >= 2
        ]

    def get_package_info(self, package_name: str) -> Dict:
        raw_output = self.adb.execute_command(f"dumpsys package {package_name}")
        return self._parse_package_info(raw_output, package_name)

    def _parse_package_info(self, raw_output: str, package_name: str) -> Dict:
        permissions = self._extract_permissions(raw_output)

        info = {
            'package': package_name,
            'permissions': permissions,
            'activities': self._extract_activities(raw_output, package_name),
            'services': self._extract_components(raw_output, "Service", package_name),
            'receivers': self._extract_components(raw_output, "Receiver", package_name),
        }
        return info

    def _extract_permissions(self, text: str) -> Dict[str, List[str]]:
        permissions = {
            'requested': [],
            'granted': [],
            'dangerous': []  # (can add later)
        }

        # Requested permissions
        requested_match = re.search(r'requested permissions:(.*?)(^\S|\Z)', text, re.DOTALL | re.MULTILINE)
        if requested_match:
            requested_block = requested_match.group(1)
            requested = [
                line.strip().rstrip(':') for line in requested_block.splitlines()
                if (line.strip().startswith('android.permission') or line.strip().startswith('com.'))
            ]
            permissions['requested'] = requested

        # Granted permissions
        granted_match = re.search(r'grantedPermissions:(.*?)(^\S|\Z)', text, re.DOTALL | re.MULTILINE)
        if granted_match:
            granted_block = granted_match.group(1)
            granted = [
                line.strip().rstrip(':') for line in granted_block.splitlines()
                if (line.strip().startswith('android.permission') or line.strip().startswith('com.'))
            ]
            permissions['granted'] = granted

        return permissions

    def _extract_activities(self, text: str, package_name: str) -> List[str]:
        activities = set()

        pattern = re.compile(r"^\s*[a-f0-9]+\s+(" + re.escape(package_name) + r"/[^\s]+)\s+filter", re.MULTILINE)
        activities.update(pattern.findall(text))

        std_pattern = re.compile(r"Activity\{[0-9a-f]+\s+(" + re.escape(package_name) + r"/[^\s]+)")
        activities.update(std_pattern.findall(text))

        return sorted(activities)

    def _extract_components(self, text: str, comp_type: str, package_name: str) -> List[str]:
        pattern = re.compile(
            r"(?:^\s*[a-f0-9]+\s+|" + comp_type + r"\{[0-9a-f]+\s+)(" +
            re.escape(package_name) + r"/[^\s/]+)")
        return sorted(set(pattern.findall(text)))
