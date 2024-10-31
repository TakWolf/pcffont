from pathlib import Path

from pcffont import PcfFont


def test_unifont(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('unifont', 'unifont-16.0.02.pcf')
    save_path = tmp_path.joinpath('unifont-16.0.02.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_spleen_5_8(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('spleen', 'spleen-5x8.pcf')
    save_path = tmp_path.joinpath('spleen-5x8.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_spleen_6_12(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('spleen', 'spleen-6x12.pcf')
    save_path = tmp_path.joinpath('spleen-6x12.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_spleen_8_16(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('spleen', 'spleen-8x16.pcf')
    save_path = tmp_path.joinpath('spleen-8x16.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_spleen_12_24(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('spleen', 'spleen-12x24.pcf')
    save_path = tmp_path.joinpath('spleen-12x24.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_spleen_16_32(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('spleen', 'spleen-16x32.pcf')
    save_path = tmp_path.joinpath('spleen-16x32.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_spleen_32_64(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('spleen', 'spleen-32x64.pcf')
    save_path = tmp_path.joinpath('spleen-32x64.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_demo_lsbyte_lsbit_p4_u2(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('demo', 'demo-lsbyte-lsbit-p4-u2.pcf')
    save_path = tmp_path.joinpath('demo-lsbyte-lsbit-p4-u2.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_demo_lsbyte_msbit_p4_u2(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('demo', 'demo-lsbyte-msbit-p4-u2.pcf')
    save_path = tmp_path.joinpath('demo-lsbyte-msbit-p4-u2.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_demo_msbyte_lsbit_p4_u2(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('demo', 'demo-msbyte-lsbit-p4-u2.pcf')
    save_path = tmp_path.joinpath('demo-msbyte-lsbit-p4-u2.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_demo_msbyte_msbit_p4_u2(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('demo', 'demo-msbyte-msbit-p4-u2.pcf')
    save_path = tmp_path.joinpath('demo-msbyte-msbit-p4-u2.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_demo_lsbyte_lsbit_p2_u4(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('demo', 'demo-lsbyte-lsbit-p2-u4.pcf')
    save_path = tmp_path.joinpath('demo-lsbyte-lsbit-p2-u4.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_demo_lsbyte_msbit_p2_u4(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('demo', 'demo-lsbyte-msbit-p2-u4.pcf')
    save_path = tmp_path.joinpath('demo-lsbyte-msbit-p2-u4.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_demo_msbyte_lsbit_p2_u4(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('demo', 'demo-msbyte-lsbit-p2-u4.pcf')
    save_path = tmp_path.joinpath('demo-msbyte-lsbit-p2-u4.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_demo_msbyte_msbit_p2_u4(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('demo', 'demo-msbyte-msbit-p2-u4.pcf')
    save_path = tmp_path.joinpath('demo-msbyte-msbit-p2-u4.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_demo(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('demo', 'demo.pcf')
    save_path = tmp_path.joinpath('demo.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()


def test_demo_2(assets_dir: Path, tmp_path: Path):
    load_path = assets_dir.joinpath('demo', 'demo-2.pcf')
    save_path = tmp_path.joinpath('demo-2.pcf')
    font = PcfFont.load(load_path)
    font.save(save_path)
    assert load_path.read_bytes() == save_path.read_bytes()
