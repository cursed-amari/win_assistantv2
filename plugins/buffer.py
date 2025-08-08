from typing import List
import time
import logging
import datetime

from PyQt6.QtCore import pyqtSignal
from PyQt6.QtWidgets import QApplication

from plugins.ui_init.buffer_frame import BufferFrame
from plugins.ui_init.page_buffer_init import PageBufferInit

import keyboard

_logger = logging.getLogger(__name__)


class Buffer(PageBufferInit):
    info_signal = pyqtSignal(str, bool)
    copy_signal = pyqtSignal()
    paste_signal_1 = pyqtSignal(int)
    paste_signal_2 = pyqtSignal(int)
    paste_signal_3 = pyqtSignal(int)
    paste_signal_4 = pyqtSignal(int)
    paste_signal_5 = pyqtSignal(int)

    MAX_BUFFERS = 5

    def __init__(self) -> None:
        super().__init__()
        self.clipboard = QApplication.clipboard()
        self._buffers: List[BufferFrame] = []
        self._setup_hotkeys()
        self._connect_signals()

    def create_buffer_frame(self, content: str) -> None:
        if not self._can_add_buffer():
            return

        buffer = BufferFrame(self.scrollAreaWidgetContents_buffer, content)
        buffer.label.mouseDoubleClickEvent = lambda _, txt=buffer.label.toPlainText(): self._set_clipboard(txt)
        buffer.checkBox_pin.clicked.connect(self._reorder_buffers)
        buffer.label_notification.setText(str(datetime.datetime.now().strftime("%d.%m.%y %H:%M")))

        self._buffers.append(buffer)
        self.verticalLayout_scrollArea.addWidget(buffer.get_frame())
        self.info_signal.emit(f"Буфер: {buffer.label.toPlainText()} создан", False)

    def on_ctrl_c_pressed(self) -> None:
        time.sleep(0.005)  # slight delay for clipboard update
        mime_data = self.clipboard.mimeData()

        if mime_data.hasText():
            self.create_buffer_frame(mime_data.text())
        elif mime_data.hasUrls():
            self.create_buffer_frame(mime_data.urls()[0].toString())

    def _reorder_buffers(self) -> None:
        self._buffers.sort(key=lambda buf: not buf.checkBox_pin.isChecked())
        self._refresh_buffer_layout()

    def _refresh_buffer_layout(self) -> None:
        self._clear_buffer_layout()
        for buffer in self._buffers:
            self.verticalLayout_scrollArea.addWidget(buffer.get_frame())

    def _clear_buffer_layout(self) -> None:
        for buffer in self._buffers:
            self.verticalLayout_scrollArea.removeWidget(buffer.get_frame())

    def _can_add_buffer(self) -> bool:
        if len(self._buffers) >= self.MAX_BUFFERS:
            for buffer in self._buffers:
                if not buffer.checkBox_pin.isChecked():
                    self._buffers.remove(buffer)
                    buffer.get_frame().deleteLater()
                    break
            else:
                return False
        return True

    def _set_clipboard(self, content: str) -> None:
        self.clipboard.setText(content)
        self.info_signal.emit(f"Буфер: {content} в буфере обмена", False)

    def _setup_hotkeys(self) -> None:
        keyboard.add_hotkey("ctrl+c", lambda: self.copy_signal.emit())
        keyboard.add_hotkey(f"alt+1", lambda _: self.paste_signal_1.emit(1))
        keyboard.add_hotkey(f"alt+2", lambda _: self.paste_signal_2.emit(2))
        keyboard.add_hotkey(f"alt+3", lambda _: self.paste_signal_3.emit(3))
        keyboard.add_hotkey(f"alt+4", lambda _: self.paste_signal_4.emit(4))
        keyboard.add_hotkey(f"alt+5", lambda _: self.paste_signal_5.emit(5))

    def _connect_signals(self) -> None:
        self.copy_signal.connect(self.on_ctrl_c_pressed)
        self.paste_signal_1.connect(lambda _: self._set_clipboard(self._buffers[1].context))
        self.paste_signal_2.connect(lambda _: self._set_clipboard(self._buffers[2].context))
        self.paste_signal_3.connect(lambda _: self._set_clipboard(self._buffers[3].context))
        self.paste_signal_4.connect(lambda _: self._set_clipboard(self._buffers[4].context))
        self.paste_signal_5.connect(lambda _: self._set_clipboard(self._buffers[5].context))


def get_widget():
    return Buffer()


def get_name():
    return "Buffer"

