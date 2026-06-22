import os
import sys
import types
import importlib.util
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

fluentytdl_pkg = types.ModuleType("fluentytdl")
fluentytdl_pkg.__path__ = [str(SRC_DIR / "fluentytdl")]
youtube_pkg = types.ModuleType("fluentytdl.youtube")
youtube_pkg.__path__ = [str(SRC_DIR / "fluentytdl" / "youtube")]
sys.modules.setdefault("fluentytdl", fluentytdl_pkg)
sys.modules.setdefault("fluentytdl.youtube", youtube_pkg)

core_pkg = types.ModuleType("fluentytdl.core")
config_manager_mod = types.ModuleType("fluentytdl.core.config_manager")
config_manager_mod.config_manager = types.SimpleNamespace(get=lambda *a, **k: None)
errors_mod = types.ModuleType("fluentytdl.models.errors")


class YtDlpExecutionError(Exception):
    pass


errors_mod.YtDlpExecutionError = YtDlpExecutionError
paths_mod = types.ModuleType("fluentytdl.utils.paths")
paths_mod.config_path = lambda *a, **k: ""
paths_mod.find_bundled_executable = lambda *a, **k: None
paths_mod.frozen_internal_dir = lambda *a, **k: None
paths_mod.get_clean_env = lambda *a, **k: {}
paths_mod.is_frozen = lambda *a, **k: False
paths_mod.locate_runtime_tool = lambda *a, **k: ""
sys.modules.setdefault("fluentytdl.core", core_pkg)
sys.modules.setdefault("fluentytdl.core.config_manager", config_manager_mod)
sys.modules.setdefault("fluentytdl.models.errors", errors_mod)
sys.modules.setdefault("fluentytdl.utils.paths", paths_mod)

_logger = types.SimpleNamespace(
    debug=lambda *a, **k: None,
    info=lambda *a, **k: None,
    warning=lambda *a, **k: None,
    error=lambda *a, **k: None,
)
sys.modules.setdefault("loguru", types.SimpleNamespace(logger=_logger))

spec = importlib.util.spec_from_file_location(
    "fluentytdl.youtube.yt_dlp_cli",
    SRC_DIR / "fluentytdl" / "youtube" / "yt_dlp_cli.py",
)
assert spec is not None and spec.loader is not None
yt_dlp_cli = importlib.util.module_from_spec(spec)
sys.modules["fluentytdl.youtube.yt_dlp_cli"] = yt_dlp_cli
spec.loader.exec_module(yt_dlp_cli)
ydl_opts_to_cli_args = yt_dlp_cli.ydl_opts_to_cli_args
_inject_language_into_format = yt_dlp_cli._inject_language_into_format


def test_ydl_opts_to_cli_args_passes_playlist_items_range():
    args = ydl_opts_to_cli_args({"playlist_items": "1:"})

    assert "--playlist-items" in args
    assert args[args.index("--playlist-items") + 1] == "1:"


def test_ydl_opts_to_cli_args_passes_playlist_end_without_default_limit():
    args = ydl_opts_to_cli_args({"playlistend": 136})

    assert "--playlist-end" in args
    assert args[args.index("--playlist-end") + 1] == "136"


def test_ydl_opts_to_cli_args_passes_no_playlist_for_single_video_tasks():
    args = ydl_opts_to_cli_args({"noplaylist": True})

    assert "--no-playlist" in args


def test_language_injection_does_not_prioritize_low_resolution_muxed_fallback():
    fmt = "bv*[height<=2160]+ba/b[height<=2160]"

    result = _inject_language_into_format(fmt, ["lang:en", "res"])

    assert result == "bv[height<=2160]+ba[language=en]/bv[height<=2160]+ba/b[height<=2160]"
    assert "bv*[height<=2160]+ba[language=en]" not in result
    assert "b[height<=2160][language=en]" not in result
