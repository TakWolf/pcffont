import hashlib
from pathlib import Path

from pcffont import PcfFont

project_root_dir = Path(__file__).parent.joinpath('..').resolve()


def _file_sha256(file_path: Path) -> str:
    return hashlib.sha256(file_path.read_bytes()).hexdigest()


def test_unifont(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'unifont', 'unifont-15.1.05.pcf')
    save_file_path = tmp_path.joinpath('unifont-15.1.05.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_spleen_5_8(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'spleen', 'spleen-5x8.pcf')
    save_file_path = tmp_path.joinpath('spleen-5x8.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_spleen_6_12(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'spleen', 'spleen-6x12.pcf')
    save_file_path = tmp_path.joinpath('spleen-6x12.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_spleen_8_16(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'spleen', 'spleen-8x16.pcf')
    save_file_path = tmp_path.joinpath('spleen-8x16.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_spleen_12_24(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'spleen', 'spleen-12x24.pcf')
    save_file_path = tmp_path.joinpath('spleen-12x24.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_spleen_16_32(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'spleen', 'spleen-16x32.pcf')
    save_file_path = tmp_path.joinpath('spleen-16x32.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_spleen_32_64(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'spleen', 'spleen-32x64.pcf')
    save_file_path = tmp_path.joinpath('spleen-32x64.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_demo_lsbyte_lsbit_p4_u2(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'demo', 'demo-lsbyte-lsbit-p4-u2.pcf')
    save_file_path = tmp_path.joinpath('demo-lsbyte-lsbit-p4-u2.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_demo_lsbyte_msbit_p4_u2(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'demo', 'demo-lsbyte-msbit-p4-u2.pcf')
    save_file_path = tmp_path.joinpath('demo-lsbyte-msbit-p4-u2.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_demo_msbyte_lsbit_p4_u2(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'demo', 'demo-msbyte-lsbit-p4-u2.pcf')
    save_file_path = tmp_path.joinpath('demo-msbyte-lsbit-p4-u2.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_demo_msbyte_msbit_p4_u2(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'demo', 'demo-msbyte-msbit-p4-u2.pcf')
    save_file_path = tmp_path.joinpath('demo-msbyte-msbit-p4-u2.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_demo_lsbyte_lsbit_p2_u4(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'demo', 'demo-lsbyte-lsbit-p2-u4.pcf')
    save_file_path = tmp_path.joinpath('demo-lsbyte-lsbit-p2-u4.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_demo_lsbyte_msbit_p2_u4(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'demo', 'demo-lsbyte-msbit-p2-u4.pcf')
    save_file_path = tmp_path.joinpath('demo-lsbyte-msbit-p2-u4.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_demo_msbyte_lsbit_p2_u4(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'demo', 'demo-msbyte-lsbit-p2-u4.pcf')
    save_file_path = tmp_path.joinpath('demo-msbyte-lsbit-p2-u4.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_demo_msbyte_msbit_p2_u4(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'demo', 'demo-msbyte-msbit-p2-u4.pcf')
    save_file_path = tmp_path.joinpath('demo-msbyte-msbit-p2-u4.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_demo(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'demo', 'demo.pcf')
    save_file_path = tmp_path.joinpath('demo.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_demo_2(tmp_path: Path):
    load_file_path = project_root_dir.joinpath('assets', 'demo', 'demo-2.pcf')
    save_file_path = tmp_path.joinpath('demo-2.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)
