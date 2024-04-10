import hashlib
import os
from pathlib import Path

from pcffont import PcfFont
from pcffont.header import PcfTableType, PcfHeader
from pcffont.internal.buffer import Buffer

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _compat_bdf_accelerators_header_table_size_error(file_path: str):
    """ TODO """
    with open(file_path, 'r+b') as file:
        buffer = Buffer(file)
        headers = PcfHeader.parse(buffer)

        headers_map = {header.table_type: header for header in headers}
        headers_map[PcfTableType.BDF_ACCELERATORS].table_size = headers_map[PcfTableType.ACCELERATORS].table_size

        PcfHeader.dump(buffer, headers)


def _file_sha256(file_path: str) -> str:
    with open(file_path, 'rb') as file:
        return hashlib.sha256(file.read()).hexdigest()


def test_unifont(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'unifont', 'unifont-15.1.05.pcf')
    save_file_path = os.path.join(tmp_path, 'unifont-15.1.05.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    _compat_bdf_accelerators_header_table_size_error(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_anorexia(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'artwiz', 'anorexia.pcf')
    save_file_path = os.path.join(tmp_path, 'anorexia.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    _compat_bdf_accelerators_header_table_size_error(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_kates(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'artwiz', 'kates.pcf')
    save_file_path = os.path.join(tmp_path, 'kates.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    _compat_bdf_accelerators_header_table_size_error(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)


def test_dweep(tmp_path: Path):
    load_file_path = os.path.join(project_root_dir, 'assets', 'dweep', 'dweep.pcf')
    save_file_path = os.path.join(tmp_path, 'dweep.pcf')
    font = PcfFont.load(load_file_path)
    font.save(save_file_path)
    _compat_bdf_accelerators_header_table_size_error(save_file_path)
    assert _file_sha256(load_file_path) == _file_sha256(save_file_path)
