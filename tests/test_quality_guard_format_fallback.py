import sys
import types
import importlib.util
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

fluentytdl_pkg = types.ModuleType("fluentytdl")
fluentytdl_pkg.__path__ = [str(SRC_DIR / "fluentytdl")]
download_pkg = types.ModuleType("fluentytdl.download")
download_pkg.__path__ = [str(SRC_DIR / "fluentytdl" / "download")]
core_pkg = types.ModuleType("fluentytdl.core")
config_manager_mod = types.ModuleType("fluentytdl.core.config_manager")
config_manager_mod.config_manager = types.SimpleNamespace(get=lambda key, default=None: default)
utils_pkg = types.ModuleType("fluentytdl.utils")
logger_mod = types.ModuleType("fluentytdl.utils.logger")
logger_mod.logger = types.SimpleNamespace(
    debug=lambda *a, **k: None,
    info=lambda *a, **k: None,
    warning=lambda *a, **k: None,
    error=lambda *a, **k: None,
)

sys.modules.setdefault("fluentytdl", fluentytdl_pkg)
sys.modules.setdefault("fluentytdl.download", download_pkg)
sys.modules.setdefault("fluentytdl.core", core_pkg)
sys.modules.setdefault("fluentytdl.core.config_manager", config_manager_mod)
sys.modules.setdefault("fluentytdl.utils", utils_pkg)
sys.modules.setdefault("fluentytdl.utils.logger", logger_mod)

spec = importlib.util.spec_from_file_location(
    "fluentytdl.download.quality_guard",
    SRC_DIR / "fluentytdl" / "download" / "quality_guard.py",
)
assert spec is not None and spec.loader is not None
quality_guard = importlib.util.module_from_spec(spec)
sys.modules["fluentytdl.download.quality_guard"] = quality_guard
spec.loader.exec_module(quality_guard)
resolve_format_with_guard = quality_guard.resolve_format_with_guard
soften_exact_format_for_download = quality_guard.soften_exact_format_for_download


def test_resolve_format_replaces_unavailable_exact_pair_with_height_fallback():
    formats = [
        {"format_id": "137", "height": 1080, "vcodec": "avc1.640028", "acodec": "none"},
        {"format_id": "140", "vcodec": "none", "acodec": "mp4a.40.2"},
    ]

    final_format, final_opts, intent, verdict = resolve_format_with_guard(
        "137+140-drc",
        {},
        formats_list=formats,
        intent_max_height=1080,
        intent_preset_id="1080p",
        download_type="video_audio",
        source_path="test",
    )

    assert final_format == "bv[height<=1080]+ba/b[height<=1080]"
    assert intent.target_format_ids == ["137", "140-drc"]
    assert final_opts["__fluentytdl_quality_intent"]["target_height"] == 1080
    assert verdict is None or verdict.passed


def test_resolve_format_keeps_available_exact_pair():
    formats = [
        {"format_id": "137", "height": 1080, "vcodec": "avc1.640028", "acodec": "none"},
        {"format_id": "140", "vcodec": "none", "acodec": "mp4a.40.2"},
    ]

    final_format, _, intent, _ = resolve_format_with_guard(
        "137+140",
        {},
        formats_list=formats,
        intent_max_height=1080,
        intent_preset_id="1080p",
        download_type="video_audio",
        source_path="test",
    )

    assert final_format == "137+140"
    assert intent.target_format_ids == ["137", "140"]


def test_resolve_audio_only_replaces_unavailable_exact_audio_with_best_audio():
    formats = [
        {"format_id": "140", "vcodec": "none", "acodec": "mp4a.40.2"},
    ]

    final_format, _, intent, _ = resolve_format_with_guard(
        "140-drc",
        {},
        formats_list=formats,
        intent_max_height=None,
        intent_preset_id="audio",
        download_type="audio_only",
        source_path="test",
    )

    assert final_format == "bestaudio/best"
    assert intent.target_format_ids == ["140-drc"]


def test_soften_exact_format_replaces_persisted_fixed_video_audio_pair():
    assert (
        soften_exact_format_for_download("137+140")
        == "bv[height<=1080]+ba/b[height<=1080]"
    )
    assert (
        soften_exact_format_for_download(
            "137+140[language=zh-hans]/137+140[language=en]/137+140"
        )
        == "bv[height<=1080]+ba/b[height<=1080]"
    )


def test_soften_exact_format_preserves_generic_format():
    assert (
        soften_exact_format_for_download("bv[height<=720]+ba/b[height<=720]")
        == "bv[height<=720]+ba/b[height<=720]"
    )
