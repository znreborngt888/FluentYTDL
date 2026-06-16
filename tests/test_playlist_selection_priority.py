import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src")))

from fluentytdl.ui.playlist_selection_priority import (
    selected_pending_detail_rows,
    should_auto_enqueue_playlist_details,
)


def test_selected_pending_detail_rows_only_returns_selected_unloaded_rows():
    rows = [
        {"selected": True},
        {"selected": False},
        {"selected": True},
        {"selected": True},
    ]

    assert selected_pending_detail_rows(rows, detail_loaded={0}) == [2, 3]


def test_selected_pending_detail_rows_can_limit_priority_burst():
    rows = [{"selected": True} for _ in range(10)]

    assert selected_pending_detail_rows(rows, detail_loaded=set(), limit=3) == [0, 1, 2]


def test_playlist_details_are_not_auto_enqueued_after_flat_parse():
    assert should_auto_enqueue_playlist_details() is False
