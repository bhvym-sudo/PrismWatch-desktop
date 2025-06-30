# ui/live_behavior_tab.py
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QGroupBox, QTextEdit, QLabel
from PyQt5.QtCore import QThread, pyqtSignal
from core.adb_controller import ADBController
from core.uid_mapper import UIDMapper
import re


class LogcatWorker(QThread):
    log_output = pyqtSignal(str)

    def __init__(self, adb_controller: ADBController, package_name: str):
        super().__init__()
        self.adb = adb_controller
        self.package_name = package_name
        self._running = True
        self.process = None

    def run(self):
        try:
            shell_command = f"logcat | grep {self.package_name}"
            self.process = self.adb.stream_command(shell_command)

            while self._running and self.process.poll() is None:
                line = self.process.stdout.readline()
                if not line:
                    break
                self.log_output.emit(line.strip())

        except Exception as e:
            self.log_output.emit(f"[ERROR] {str(e)}")

        finally:
            if self.process:
                try:
                    self.process.terminate()
                    self.process.wait(timeout=1)
                except Exception:
                    self.process.kill()

    def stop(self):
        self._running = False
        if self.process:
            try:
                self.process.terminate()
            except:
                pass
        self.quit()
        self.wait()


class LiveBehaviorTab(QWidget):
    def __init__(self):
        super().__init__()
        self.adb = ADBController()
        self.uid_mapper = UIDMapper(self.adb)
        self.package_name = None
        self.worker = None
        self.init_ui()

    def init_ui(self):
        layout = QVBoxLayout(self)
        self.info_label = QLabel("No package selected")
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)

        group = QGroupBox("Live Background Activity")
        group_layout = QVBoxLayout(group)
        group_layout.addWidget(self.info_label)
        group_layout.addWidget(self.log_output)

        layout.addWidget(group)

    def load_live_activity(self, package_name):
        self.package_name = package_name
        self.info_label.setText(f"Monitoring: {package_name}")
        self.log_output.setHtml("<span style='color:gray;'>Starting live capture...</span><br>")

        if self.worker and self.worker.isRunning():
            self.worker.stop()
            self.worker.wait()
            self.worker = None

        self.worker = LogcatWorker(self.adb, package_name)
        self.worker.log_output.connect(self.append_log)
        self.worker.start()

    def append_log(self, text):
        highlighted = re.sub(
            r'^(\d{2}-\d{2} \d{2}:\d{2}:\d{2}\.\d{3})',
            r"<span style='color:cyan;'>\1</span>",
            text
        )
        self.log_output.append(highlighted)

    def closeEvent(self, event):
        if self.worker:
            self.worker.stop()
            self.worker = None
        event.accept()
