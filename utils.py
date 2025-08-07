from PyQt6.QtWidgets import QApplication

from settings import COLLAPSED_WIDTH, COLLAPSED_HEIGHT


def get_window_start_pos():
    SCREEN_GEOMETRY = QApplication.primaryScreen().availableGeometry()
    screen_right = SCREEN_GEOMETRY.right()
    screen_bottom = SCREEN_GEOMETRY.bottom()
    start_x = screen_right - COLLAPSED_WIDTH
    start_y = screen_bottom - COLLAPSED_HEIGHT + 2
    return start_x, start_y
