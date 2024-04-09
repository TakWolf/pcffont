import io
import os

from pcffont import table_registry, font
from pcffont.header import PcfHeader
from pcffont.internal.stream import Buffer

project_root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))


def _execute_dump(file_name: str):
    file_path = os.path.join(project_root_dir, 'assets', file_name)
    with open(file_path, 'rb') as file:
        buffer_in = Buffer(file)
        buffer_in.skip(4)
        buffer_out = Buffer(io.BytesIO())
        buffer_out.write(font._MAGIC_STRING)

        headers = PcfHeader.parse(buffer_in)
        buffer_out.write_int32_le(len(headers))
        for header in headers.values():
            header.dump(buffer_out)
        headers_size = 4 + 4 + (4 * 4) * len(headers)
        buffer_in.seek(0)
        buffer_out.seek(0)
        headers_data_in = buffer_in.read(headers_size)
        headers_data_out = buffer_out.read(headers_size)
        assert headers_data_in == headers_data_out

        for header_in in headers.values():
            table = table_registry.parse_table(buffer_in, header_in)
            if table is None:
                continue
            header_out = table.dump(buffer_out, header_in.table_type, header_in.table_offset)
            assert header_in.table_format == header_out.table_format
            assert header_in.table_size == header_out.table_size
            buffer_in.seek(header_in.table_offset)
            buffer_out.seek(header_out.table_offset)
            table_data_in = buffer_in.read(header_in.table_size)
            table_data_out = buffer_out.read(header_out.table_size)
            assert table_data_in == table_data_out


def test_unifont():
    _execute_dump('unifont/unifont-15.1.05.pcf')


def test_anorexia():
    _execute_dump('artwiz/anorexia.pcf')


def test_kates():
    _execute_dump('artwiz/kates.pcf')


def test_dweep():
    _execute_dump('dweep/dweep.pcf')
