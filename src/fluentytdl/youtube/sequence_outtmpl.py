from __future__ import annotations


def numbered_outtmpl(sequence: int, total: int) -> str:
    """Build a yt-dlp output template prefixed with a stable download order."""

    width = max(3, len(str(max(1, int(total)))))
    number = max(1, int(sequence))
    return f"{number:0{width}d} - %(title)s.%(ext)s"
