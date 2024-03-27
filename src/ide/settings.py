import os
import yaml
from pathlib import Path

from PyQt5.QtWidgets import QAction
from PyQt5.QtGui import QPixmap
from PyQt5.QtGui import QIcon


SETTINGS_FOLDER = Path.home() / '.handy'
GUI_SETTINGS = SETTINGS_FOLDER / 'gui.yaml'
CONFIG_SETTINGS = SETTINGS_FOLDER / 'config.yaml'


def get_yaml_data(yaml_file):
    with open(yaml_file, 'r') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data


class Settings:
    def __init__(self):
        data = get_yaml_data(CONFIG_SETTINGS)
        self.install_dir = Path(data['install']['directory'])
        if not os.path.exists(self.install_dir):
            raise EnvironmentError(f'Install directory {self.install_dir} not found')
        self.gui_data = get_yaml_data(GUI_SETTINGS)


settings = Settings()


def get_icon(icon_name):
    return QIcon(str(settings.install_dir / 'media' / 'icons' / f'{icon_name}.svg'))


def get_pixmap(pixmap_name):
    return QPixmap(str(settings.install_dir / 'media' / 'icons' / f'{pixmap_name}.png'))


def get_all_actions(window, config_data=settings.gui_data):
    actions = config_data['Actions']
    qt_actions = {}
    for action in actions:
        # example: {'name': 'Open', 'icon': 'open', 'action': 'open-new-file'}
        name = action['name']
        if 'icon' in action:
            icon = get_icon(action['icon'])
            new_action = QAction(icon, name, window)
        else:
            new_action = QAction(name, window)
        if 'key' in action:
            new_action.setShortcut(action['key'])
        qt_actions[name] = new_action
    return qt_actions


def get_menu_setup(config_data=settings.gui_data):
    return config_data['Menus']


def get_toolbar_setup(config_data=settings.gui_data):
    return config_data['Toolbar']


if __name__ == '__main__':
    #gui_actions = get_all_actions(settings.gui_data, None)
    #print(gui_actions)
    menus = get_menu_setup(settings.gui_data)
    print(menus)
