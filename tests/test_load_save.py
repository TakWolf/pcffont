import hashlib
import os
from pathlib import Path

from pcffont import PcfFont

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _file_sha256(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        return hashlib.sha256(file.read()).hexdigest()


def test_unifont(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'unifont', 'unifont-15.1.05.pcf')
    save_file_path = os.path.join(tmp_path, 'unifont-15.1.05.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_spleen_5_8(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'spleen', 'spleen-5x8.pcf')
    save_file_path = os.path.join(tmp_path, 'spleen-5x8.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_spleen_6_12(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'spleen', 'spleen-6x12.pcf')
    save_file_path = os.path.join(tmp_path, 'spleen-6x12.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_spleen_8_16(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'spleen', 'spleen-8x16.pcf')
    save_file_path = os.path.join(tmp_path, 'spleen-8x16.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_spleen_12_24(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'spleen', 'spleen-12x24.pcf')
    save_file_path = os.path.join(tmp_path, 'spleen-12x24.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_spleen_16_32(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'spleen', 'spleen-16x32.pcf')
    save_file_path = os.path.join(tmp_path, 'spleen-16x32.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_spleen_32_64(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'spleen', 'spleen-32x64.pcf')
    save_file_path = os.path.join(tmp_path, 'spleen-32x64.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_dweep(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'dweep', 'dweep.pcf')
    save_file_path = os.path.join(tmp_path, 'dweep.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_rock36(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'sgi', 'rock36.pcf')
    save_file_path = os.path.join(tmp_path, 'rock36.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_raize(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'raize', 'raize-normal-19.pcf')
    save_file_path = os.path.join(tmp_path, 'raize-normal-19.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_anorexia(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'artwiz', 'anorexia.pcf')
    save_file_path = os.path.join(tmp_path, 'anorexia.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_kates(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'artwiz', 'kates.pcf')
    save_file_path = os.path.join(tmp_path, 'kates.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_trisk(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'trisk', 'trisk.pcf')
    save_file_path = os.path.join(tmp_path, 'trisk.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_profont(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'profont-x11', 'ProFont_r400-29.pcf')
    save_file_path = os.path.join(tmp_path, 'ProFont_r400-29.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)
