import os
import shutil

from pathlib import Path

SETTINGS_FOLDER = Path.home() / '.handy'

# ensure ~/.handy exists
# ensure it has gui.yaml installed
# ensure it also contains config.yaml


def create_directory():
    if not os.path.exists(SETTINGS_FOLDER):
        print(f'* Creating {str(SETTINGS_FOLDER)}')
        os.mkdir(SETTINGS_FOLDER)


def add_yaml_file(file):
    if not os.path.exists(file):
        print(f'* Error: File {str(file)} does not exist')
    else:
        shutil.copy(file, SETTINGS_FOLDER / file.name)


if __name__ == '__main__':
    create_directory()
    add_yaml_file(Path('./data/config.yaml'))
    add_yaml_file(Path('./data/gui.yaml'))
