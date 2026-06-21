import sys
import importlib.util
import types
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

fluentytdl_pkg = types.ModuleType("fluentytdl")
fluentytdl_pkg.__path__ = [str(SRC_DIR / "fluentytdl")]
youtube_pkg = types.ModuleType("fluentytdl.youtube")
youtube_pkg.__path__ = [str(SRC_DIR / "fluentytdl" / "youtube")]
sys.modules.setdefault("fluentytdl", fluentytdl_pkg)
sys.modules.setdefault("fluentytdl.youtube", youtube_pkg)

spec = importlib.util.spec_from_file_location(
    "fluentytdl.youtube.pot_startup",
    SRC_DIR / "fluentytdl" / "youtube" / "pot_startup.py",
)
assert spec is not None and spec.loader is not None
pot_startup = importlib.util.module_from_spec(spec)
sys.modules["fluentytdl.youtube.pot_startup"] = pot_startup
spec.loader.exec_module(pot_startup)
ensure_pot_provider_available = pot_startup.ensure_pot_provider_available


class FakePOTManager:
    def __init__(self, *, running=False, warm=True, start_ok=True):
        self._running = running
        self.is_warm = warm
        self.start_ok = start_ok
        self.started = 0
        self.waited = 0

    def is_running(self):
        return self._running

    def start_server(self):
        self.started += 1
        self._running = self.start_ok
        return self.start_ok

    def wait_until_ready(self, timeout=15):
        self.waited += 1
        self.is_warm = True
        return True


def test_ensure_pot_provider_starts_when_enabled_but_not_running():
    messages = []
    manager = FakePOTManager(running=False, warm=False, start_ok=True)

    ok = ensure_pot_provider_available(manager, messages.append, warm_timeout=3)

    assert ok is True
    assert manager.started == 1
    assert manager.waited == 1
    assert any("正在尝试启动" in message for message in messages)


def test_ensure_pot_provider_reports_failure_when_start_fails():
    messages = []
    manager = FakePOTManager(running=False, start_ok=False)

    ok = ensure_pot_provider_available(manager, messages.append)

    assert ok is False
    assert manager.started == 1
    assert any("启动失败" in message for message in messages)
