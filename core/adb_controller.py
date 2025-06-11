import subprocess
from typing import List, Optional
import os

class ADBController:
    def __init__(self, adb_path: str = "./bin/adb", device_id: Optional[str] = None):
        self.adb_path = adb_path
        self.device_id = device_id

    def _build_adb_cmd(self, command: str, use_su: bool = False) -> List[str]:
        cmd = [os.path.abspath(self.adb_path)]
        if self.device_id:
            cmd.extend(["-s", self.device_id])
        cmd.append("shell")
        if use_su:
            cmd.extend(["su", "-c", command])
        else:
            cmd.append(command)
        return cmd

    def execute_command(self, command: str, use_su: bool = False, timeout: Optional[int] = None) -> str:
        try:
            cmd = self._build_adb_cmd(command, use_su)
            result = subprocess.run(
                cmd,
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                timeout=timeout
            )
            return result.stdout.strip()
        except subprocess.SubprocessError as e:
            raise ADBError(f"ADB command failed: {str(e)}")

    def stream_command(self, command: str, use_su: bool = False):
        try:
            cmd = self._build_adb_cmd(command, use_su)
            process = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            return process
        except Exception as e:
            raise ADBError(f"Failed to start streaming ADB command: {str(e)}")

class ADBError(Exception):
    pass
