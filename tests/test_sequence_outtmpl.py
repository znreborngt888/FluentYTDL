import sys
from pathlib import Path

SRC_DIR = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, str(SRC_DIR))

from fluentytdl.youtube.sequence_outtmpl import numbered_outtmpl


def test_numbered_outtmpl_prefixes_title_template_with_zero_padded_sequence():
    assert numbered_outtmpl(1, 47) == "001 - %(title)s.%(ext)s"
    assert numbered_outtmpl(47, 47) == "047 - %(title)s.%(ext)s"


def test_numbered_outtmpl_expands_padding_for_large_playlists():
    assert numbered_outtmpl(136, 136) == "136 - %(title)s.%(ext)s"
    assert numbered_outtmpl(7, 1200) == "0007 - %(title)s.%(ext)s"


def test_numbered_outtmpl_keeps_at_least_three_digits_for_small_batches():
    assert numbered_outtmpl(2, 2) == "002 - %(title)s.%(ext)s"
