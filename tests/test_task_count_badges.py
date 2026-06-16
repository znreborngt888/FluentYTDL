import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fluentytdl.ui.task_count_badges import build_task_count_badges


def test_build_task_count_badges_formats_counts_for_filter_tabs():
    counts = {
        "all": 128,
        "running": 2,
        "queued": 14,
        "paused": 0,
        "quality_guard": 0,
        "completed": 109,
        "error": 3,
    }

    badges = build_task_count_badges(counts)

    assert badges == {
        "all": "全部任务 128",
        "running": "下载中 2",
        "queued": "排队中 14",
        "paused": "已暂停 0",
        "quality_guard": "质量守卫 0",
        "completed": "已完成 109",
        "error": "已失败 3",
    }


def test_build_task_count_badges_treats_missing_counts_as_zero():
    badges = build_task_count_badges({"all": 1})

    assert badges["all"] == "全部任务 1"
    assert badges["queued"] == "排队中 0"
