from functools import partial
import logging

from PyQt6.QtCore import QPropertyAnimation, QEasingCurve, QRect
from PyQt6.QtGui import QEnterEvent, QMouseEvent
from PyQt6.QtWidgets import (
    QMainWindow,
    QBoxLayout,
    QPushButton,
    QSizePolicy, QWidget,
)

from core.loader import load_plugins
from settings import (
    ANIMATION_DURATION,
    COLLAPSED_HEIGHT,
    COLLAPSED_WIDTH,
    EXPANDED_HEIGHT,
    EXPANDED_WIDTH,
    HOVERED_HEIGHT,
    HOVERED_WIDTH,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    TASKBAR_HEIGHT,
)
from ui_init.ui_main_window import UiMainWindow


_logger = logging.getLogger(__name__)


class MainWindowView(QMainWindow, UiMainWindow):
    """
    Main application window supporting hover and expand/collapse animations,
    and dynamic plugin loading.
    """

    def __init__(self) -> None:
        super().__init__()
        self.setupUi(self)
        self._is_expanded = False
        self._active_plugins: dict[str, QWidget] = {}
        self._current_plugin: str | None = None
        self._hovered_height = HOVERED_HEIGHT
        self._animation: QPropertyAnimation | None = None

        self._apply_default_style()
        self._connect_signals()
        self._populate_plugins()

    def _apply_default_style(self) -> None:
        """
        Loads a QSS stylesheet if available, otherwise applies a base style and informs the user.
        """
        try:
            with open("style.qss", "r", encoding="utf-8") as sheet:
                self.setStyleSheet(sheet.read())
        except FileNotFoundError:
            _logger.warning("style.qss not found, using default style.")
            self.label_info.setText(
                "⚠️ style.qss не найден. Применяется базовый стиль."
            )
            self.setStyleSheet("background-color: #111; border: 2px solid cyan;")

    def _connect_signals(self) -> None:
        """
        Connects QPushButton signals to their respective slots.
        """
        self.pushButton_expand.clicked.connect(self.toggle_expand)
        self.pushButton_close.clicked.connect(self.close)

    def _populate_plugins(self) -> None:
        """
        Dynamically loads plugins and inserts navigation buttons.
        """
        for name, widget in load_plugins():
            if name not in self._active_plugins:
                self._active_plugins[name] = widget
                btn = QPushButton(f"{name[0].capitalize()}{name[-1].capitalize()}")
                btn.setFixedSize(30, 30)
                btn.clicked.connect(partial(self._on_plugin_selected, name))
                widget.info_signal.connect(self._set_info_text)
                self.boxLayout_navigation.insertWidget(1, btn)
                self._hovered_height += btn.height() + self.boxLayout_navigation.spacing()
            else:
                _logger.warning(f"a plugin named {name} already exists")
                self._set_info_text("⚠️ Имя плагина {name} уже занято", True)

    def _set_info_text(self, text, filling=False):
        if filling:
            self.label_info.setText(f"{self.label_info.toPlainText()}\n{text}")
        else:
            self.label_info.setText(text)

    def _on_plugin_selected(self, plugin_name: str) -> None:
        """
        Displays the selected plugin widget, removing any previously shown plugin.
        """
        if self._current_plugin:
            prev_widget = self._active_plugins[self._current_plugin]
            self.verticalLayout_widget.removeWidget(prev_widget)
            prev_widget.setParent(None)

        self._current_plugin = plugin_name
        self.verticalLayout_widget.addWidget(self._active_plugins[plugin_name])

        if not self._is_expanded:
            self.toggle_expand()

    def enterEvent(self, event: QEnterEvent) -> None:
        """
        Expands window on hover if not already expanded.
        """
        if not self._is_expanded:
            self._animate_to(
                x=SCREEN_WIDTH - HOVERED_WIDTH-40,
                width=HOVERED_WIDTH,
                height=self._hovered_height,
            )
            self.frame_navigate.show()
            self.frame_info.show()
        super().enterEvent(event)

    def leaveEvent(self, event: QMouseEvent) -> None:
        """
        Collapses window on hover leave if not expanded.
        """
        if not self._is_expanded:
            self._animate_to(
                x=SCREEN_WIDTH - COLLAPSED_WIDTH,
                width=COLLAPSED_WIDTH,
                height=COLLAPSED_HEIGHT,
            )
            self.frame_navigate.hide()
            self.frame_info.hide()
        super().leaveEvent(event)

    def toggle_expand(self) -> None:
        """
        Toggles between expanded and collapsed states.
        """
        if self._is_expanded:
            # Collapse
            self._animate_to(
                x=SCREEN_WIDTH - COLLAPSED_WIDTH,
                width=COLLAPSED_WIDTH,
                height=COLLAPSED_HEIGHT,
            )
            self.boxLayout_navigation.setDirection(
                QBoxLayout.Direction.TopToBottom
            )
            self.frame_widget.hide()
            self.frame_navigate.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        else:
            # Expand
            self._animate_to(
                x=SCREEN_WIDTH - EXPANDED_WIDTH,
                width=EXPANDED_WIDTH,
                height=EXPANDED_HEIGHT,
            )
            self.boxLayout_navigation.setDirection(
                QBoxLayout.Direction.LeftToRight
            )
            self.frame_widget.show()
            self.frame_navigate.setSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Minimum)

        # Toggle state
        self._is_expanded = not self._is_expanded

    def _animate_to(self, x: int, width: int, height: int) -> None:
        """
        Animates window geometry to the specified dimensions.

        :param x: Target X position
        :param width: Target width
        :param height: Target height
        """
        start_rect = self.geometry()
        y = SCREEN_HEIGHT - height - TASKBAR_HEIGHT

        self._animation = QPropertyAnimation(self, b"geometry")
        self._animation.setDuration(ANIMATION_DURATION)
        self._animation.setEasingCurve(QEasingCurve.Type.OutExpo)
        self._animation.setStartValue(start_rect)
        self._animation.setEndValue(QRect(x, y, width, height))
        self._animation.start()
