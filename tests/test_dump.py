import io
import os

from pcffont.header import PcfHeader
from pcffont.internal import util
from pcffont.internal.buffer import Buffer

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _test_dump(file_name: str):
    file_path = os.path.join(project_root_dir, 'assets', file_name)
    with open(file_path, 'rb') as file:
        buffer_in = Buffer(file)
        buffer_out = Buffer(io.BytesIO())

        headers_in = PcfHeader.parse(buffer_in)
        PcfHeader.dump(buffer_out, headers_in)
        buffer_in.seek(0)
        buffer_out.seek(0)
        headers_data_size = 4 + 4 + (4 * 4) * len(headers_in)
        headers_data_in = buffer_in.read(headers_data_size)
        headers_data_out = buffer_out.read(headers_data_size)
        assert headers_data_in == headers_data_out

        for header_in in headers_in:
            table = util.parse_table(buffer_in, header_in)
            if table is None:
                continue
            table_offset = header_in.table_offset
            table_size = table.dump(buffer_out, table_offset)
            assert table_size == header_in.table_size
            buffer_in.seek(table_offset)
            buffer_out.seek(table_offset)
            table_data_in = buffer_in.read(table_size)
            table_data_out = buffer_out.read(table_size)
            assert table_data_in == table_data_out


def test_unifont():
    _test_dump('unifont/unifont-15.1.05.pcf')


def test_anorexia():
    _test_dump('artwiz/anorexia.pcf')


def test_kates():
    _test_dump('artwiz/kates.pcf')


def test_dweep():
    _test_dump('dweep/dweep.pcf')
