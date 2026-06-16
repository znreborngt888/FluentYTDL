from __future__ import annotations

from typing import Any
from urllib.parse import parse_qs, urlencode, urlparse, urlunparse


def single_video_url(url: str, video_id: str | None = None) -> str:
    """Return a watch URL that cannot be interpreted as a playlist download."""

    vid = (video_id or "").strip()
    parsed = urlparse(str(url or "").strip())
    query = parse_qs(parsed.query)

    if not vid:
        values = query.get("v") or []
        vid = str(values[0]).strip() if values else ""

    if vid:
        return f"https://www.youtube.com/watch?v={vid}"

    if "list" not in query and "index" not in query:
        return str(url or "").strip()

    query.pop("list", None)
    query.pop("index", None)
    query.pop("start_radio", None)
    return urlunparse(parsed._replace(query=urlencode(query, doseq=True)))


def force_single_video_download(
    url: str, ydl_opts: dict[str, Any], video_id: str | None = None
) -> tuple[str, dict[str, Any], bool]:
    """Normalize a row-level playlist task so yt-dlp downloads only one video."""

    next_url = single_video_url(url, video_id)
    next_opts = dict(ydl_opts or {})
    changed = next_url != str(url or "").strip()

    if not next_opts.get("noplaylist"):
        next_opts["noplaylist"] = True
        changed = True

    return next_url, next_opts, changed
