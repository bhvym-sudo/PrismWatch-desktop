import subprocess
import threading
import queue
from typing import Optional
from .adb_controller import ADBController, ADBError

class ShellBackend:
    def __init__(self, adb_path: str = "./bin/adb", device_id: Optional[str] = None):
        self.adb = ADBController(adb_path, device_id)
        self.process = None
        self.output_queue = queue.Queue()
        self.running = False

    def start_interactive_shell(self):
        try:
            cmd = self.adb._build_adb_cmd("su", use_su=False)
            self.process = subprocess.Popen(
                cmd,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            self.running = True
            # Start output reader thread
            threading.Thread(
                target=self._read_output_loop,
                daemon=True
            ).start()
            return True
        except Exception as e:
            raise ADBError(f"Failed to start root shell: {str(e)}")

    def _read_output_loop(self):
        while self.running and self.process and self.process.poll() is None:
            try:
                line = self.process.stdout.readline()
                if line:
                    self.output_queue.put(line)
            except:
                break

    def get_output(self):
        outputs = []
        while not self.output_queue.empty():
            outputs.append(self.output_queue.get())
        return ''.join(outputs) if outputs else None

    def send_command(self, command: str):
        if not self.running or not self.process or self.process.poll() is not None:
            raise ADBError("Shell is not running")
        try:
            self.process.stdin.write(command + "\n")
            self.process.stdin.flush()
        except Exception as e:
            raise ADBError(f"Failed to send command: {str(e)}")

    def stop_shell(self):
        self.running = False
        if self.process:
            try:
                self.process.stdin.write("exit\n")
                self.process.stdin.flush()
            except:
                pass
            finally:
                self.process.terminate()
                self.process = None