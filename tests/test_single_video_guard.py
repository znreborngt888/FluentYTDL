import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from fluentytdl.youtube.single_video_guard import force_single_video_download, single_video_url


def test_single_video_url_strips_playlist_context_from_watch_url():
    url = "https://www.youtube.com/watch?v=A4NasIa371c&list=PLKO4NZ&index=43"

    assert single_video_url(url) == "https://www.youtube.com/watch?v=A4NasIa371c"


def test_single_video_url_uses_entry_id_when_available():
    url = "https://www.youtube.com/shorts/not-the-id?list=PLKO4NZ"

    assert single_video_url(url, "realVideoId") == "https://www.youtube.com/watch?v=realVideoId"


def test_force_single_video_download_adds_no_playlist_flag():
    url, opts, changed = force_single_video_download(
        "https://www.youtube.com/watch?v=-ocfPuD_oqE&list=PLKO4NZ",
        {"format": "bestvideo+bestaudio/best"},
    )

    assert url == "https://www.youtube.com/watch?v=-ocfPuD_oqE"
    assert opts["noplaylist"] is True
    assert opts["format"] == "bestvideo+bestaudio/best"
    assert changed is True
