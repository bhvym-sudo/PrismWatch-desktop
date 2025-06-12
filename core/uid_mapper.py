import re

class UIDMapper:
    def __init__(self, adb):
        self.adb = adb

    def get_uid_for_package(self, package_name: str) -> str:
        raw_output = self.adb.execute_command(f"dumpsys package {package_name}")

        match = re.search(r'userId=(\d+)', raw_output)
        if match:
            uid = match.group(1)
            return uid
        else:
            raise ValueError(f"Could not find UID for package: {package_name}")
