from pathlib import Path

from pcffont import PcfFont


def test_unifont(assets_dir: Path):
    pcf_bytes = assets_dir.joinpath('unifont', 'unifont-16.0.02.pcf').read_bytes()
    font = PcfFont.parse(pcf_bytes)
    assert font.dump_to_bytes() == pcf_bytes
