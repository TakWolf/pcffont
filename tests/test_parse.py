import os
from pathlib import Path

from pcffont import PcfFont

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def test_unifont(tmp_path: Path):
    font = PcfFont.load(os.path.join(project_root_dir, 'assets', 'unifont', 'unifont-15.1.05.pcf'))
    font.save(os.path.join(tmp_path, 'unifont-15.1.05.pcf'))


def test_anorexia(tmp_path: Path):
    font = PcfFont.load(os.path.join(project_root_dir, 'assets', 'artwiz', 'anorexia.pcf'))
    font.save(os.path.join(tmp_path, 'anorexia.pcf'))


def test_kates(tmp_path: Path):
    font = PcfFont.load(os.path.join(project_root_dir, 'assets', 'artwiz', 'kates.pcf'))
    font.save(os.path.join(tmp_path, 'kates.pcf'))


def test_dweep(tmp_path: Path):
    font = PcfFont.load(os.path.join(project_root_dir, 'assets', 'dweep', 'dweep.pcf'))
    font.save(os.path.join(tmp_path, 'dweep.pcf'))
