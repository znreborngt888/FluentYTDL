from __future__ import annotations

TASK_COUNT_LABELS: dict[str, str] = {
    "all": "全部任务",
    "running": "下载中",
    "queued": "排队中",
    "paused": "已暂停",
    "quality_guard": "质量守卫",
    "completed": "已完成",
    "error": "已失败",
}


def build_task_count_badges(counts: dict[str, int]) -> dict[str, str]:
    """Return compact filter labels with live task counts."""

    return {key: f"{label} {int(counts.get(key, 0) or 0)}" for key, label in TASK_COUNT_LABELS.items()}
