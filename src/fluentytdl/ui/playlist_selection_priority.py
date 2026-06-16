from __future__ import annotations

from collections.abc import Iterable, Sequence
from typing import Any


def selected_pending_detail_rows(
    rows: Sequence[dict[str, Any]],
    detail_loaded: Iterable[int],
    *,
    limit: int | None = None,
) -> list[int]:
    """Return selected playlist rows that still need detail extraction."""

    loaded = set(detail_loaded)
    pending = [i for i, row in enumerate(rows) if row.get("selected") and i not in loaded]
    if limit is None:
        return pending
    return pending[: max(0, limit)]


def should_auto_enqueue_playlist_details() -> bool:
    """Whether a flat playlist parse should automatically fetch per-video details."""

    return False
