from pathlib import Path

project_root_dir = Path(__file__).parent.joinpath('..').resolve()
assets_dir = project_root_dir.joinpath('assets')
build_dir = project_root_dir.joinpath('build')
