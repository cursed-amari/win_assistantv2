from PyQt6 import QtWidgets, QtCore
from PyQt6.QtWidgets import QWidget


class PageBufferInit(QWidget):
    def __init__(self):
        super().__init__()
        self.setObjectName("page_buffer")
        self.verticalLayout_frame = QtWidgets.QVBoxLayout(self)
        self.verticalLayout_frame.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_frame.setSpacing(0)
        self.verticalLayout_frame.setObjectName("verticalLayout_frame")
        self.scrollArea_buffer = QtWidgets.QScrollArea(self)
        self.scrollArea_buffer.setWidgetResizable(True)
        self.scrollArea_buffer.setObjectName("scrollArea_buffer")
        self.scrollAreaWidgetContents_buffer = QtWidgets.QWidget()
        self.scrollAreaWidgetContents_buffer.setGeometry(QtCore.QRect(0, 0, 396, 553))
        self.scrollAreaWidgetContents_buffer.setObjectName("scrollAreaWidgetContents_buffer")
        self.verticalLayout_scrollArea = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents_buffer)
        self.verticalLayout_scrollArea.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_scrollArea.setSpacing(0)
        self.verticalLayout_scrollArea.setObjectName("verticalLayout_scrollArea")
        self.scrollArea_buffer.setWidget(self.scrollAreaWidgetContents_buffer)
        self.verticalLayout_frame.addWidget(self.scrollArea_buffer)


def get_widget():
    return PageBufferInit()


def get_name():
    return "Buffer"
