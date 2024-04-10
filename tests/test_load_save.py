import hashlib
import os
from pathlib import Path

from pcffont import PcfFont

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _file_sha256(file_path) -> str:
    with open(file_path, 'rb') as file:
        return hashlib.sha256(file.read()).hexdigest()


def test_unifont(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'unifont', 'unifont-15.1.05.pcf')
    save_file_path = os.path.join(tmp_path, 'unifont-15.1.05.pcf')
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


def test_dweep(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'dweep', 'dweep.pcf')
    save_file_path = os.path.join(tmp_path, 'dweep.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)
