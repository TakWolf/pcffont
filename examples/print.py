import os

from examples import assets_dir
from pcffont import PcfFont


def _print_pcf(file_name: str):
    print(f'##### {file_name}')
    font = PcfFont.load(os.path.join(assets_dir, file_name))
    # TODO


def main():
    _print_pcf('unifont/unifont-15.1.05.pcf')


if __name__ == '__main__':
    main()
