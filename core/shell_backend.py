# core/shell_backend.py
import subprocess
import os
import platform
from .adb_controller import ADBController, ADBError


class ShellBackend:
    def __init__(self):
        self.adb = ADBController()
        self.process =None

        # Make sure adb path is absolute and compatible
        adb_path = self.adb.adb_path
        if not os.path.isabs(adb_path):
            adb_path = os.path.abspath(adb_path)
        if platform.system() == "Windows" and not adb_path.endswith(".exe"):
            adb_path += ".exe"
        self.adb.adb_path = adb_path

    def start_shell(self):
        try:
            cmd = [self.adb.adb_path]
            if self.adb.device_id:
                cmd.extend(["-s", self.adb.device_id])
            cmd.append("shell")

            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            return self.process
        except Exception as e:
            raise ADBError(f"Failed to start ADB shell: {str(e)}")

    def send_input(self, command: str):
        if not self.process or self.process.poll() is not None:
            raise ADBError("ADB shell is not running")
        try:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
        except Exception as e:
            raise ADBError(f"Failed to send command: {str(e)}")

    def read_output_line(self):
        if not self.process or self.process.poll() is not None:
            return None
        try:
            return self.process.stdout.readline()
        except Exception:
            return None

    def stop_shell(self):
        if self.process:
            try:
                self.process.terminate()
                self.process.wait(timeout=1)
            except Exception:
                self.process.kill()
            self.process = None
