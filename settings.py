import configparser

config = configparser.ConfigParser()
config.read('settings.ini')

PLUGINS_PATH = config["settings"]["plugins_path"]

TASKBAR_HEIGHT = int(config["settings"]["taskbar_height"])
COLLAPSED_WIDTH = int(config["settings"]["collapsed_width"])
HOVERED_WIDTH = int(config["settings"]["hovered_width"])
EXPANDED_WIDTH = int(config["settings"]["expanded_width"])
COLLAPSED_HEIGHT = int(config["settings"]["collapsed_height"])
HOVERED_HEIGHT = int(config["settings"]["hovered_height"])
EXPANDED_HEIGHT = int(config["settings"]["expanded_height"])
ANIMATION_DURATION = int(config["settings"]["animation_duration"])
SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080
