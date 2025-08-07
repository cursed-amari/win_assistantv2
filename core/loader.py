import importlib
import os
from typing import List, Tuple
from PyQt6.QtWidgets import QWidget

from settings import PLUGINS_PATH


def load_plugins() -> List[Tuple[str, QWidget]]:
    plugins = []
    for name in os.listdir(PLUGINS_PATH):
        if name.endswith(".py") and name != "__init__.py":
            plugin_name = name[:-3]
            try:
                plugin = importlib.import_module(f"{PLUGINS_PATH}.{plugin_name}")
                widget = plugin.get_widget()
                name = plugin.get_name()
                plugins.append((name, widget))
            except Exception as e:
                print(f"Ошибка при загрузке виджета {plugin_name}: {e}")
    return plugins
