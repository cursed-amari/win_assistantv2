from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QBoxLayout, QPushButton, QLabel, QFrame, QSizePolicy

from settings import COLLAPSED_WIDTH, COLLAPSED_HEIGHT
from utils import get_window_start_pos


class UiMainWindow:
    def setupUi(self, main_window):
        self.centralWidget = QWidget()

        self.navigate_buttons_list = []

        main_window.setCentralWidget(self.centralWidget)
        main_window.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        main_window.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        main_window.setGeometry(*get_window_start_pos(), COLLAPSED_WIDTH, COLLAPSED_HEIGHT)

        self.verticalLayout_main = QVBoxLayout()
        self.verticalLayout_main.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.boxLayout_navigation = QBoxLayout(QBoxLayout.Direction.TopToBottom)
        self.verticalLayout_widget = QVBoxLayout()
        self.verticalLayout_info = QVBoxLayout()

        self.frame_navigate = QFrame()
        self.frame_navigate.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.frame_navigate.setLayout(self.boxLayout_navigation)

        self.frame_widget = QFrame()
        self.frame_widget.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)
        self.frame_widget.setLayout(self.verticalLayout_widget)

        self.frame_info = QFrame()
        self.frame_info.setLayout(self.verticalLayout_info)

        self.verticalLayout_main.addWidget(self.frame_navigate)
        self.verticalLayout_main.addWidget(self.frame_widget)
        self.verticalLayout_main.addWidget(self.frame_info)

        self.pushButton_expand = QPushButton("⤢")
        self.pushButton_expand.setFixedSize(30, 30)
        self.pushButton_close = QPushButton("✕")
        self.pushButton_close.setFixedSize(30, 30)
        self.label_info = QLabel("Info")
        self.label_info.setWordWrap(True)

        self.navigate_buttons_list.append(self.pushButton_expand)
        self.navigate_buttons_list.append(self.pushButton_close)

        self.boxLayout_navigation.addWidget(self.pushButton_expand)
        self.boxLayout_navigation.addWidget(self.pushButton_close)

        self.frame_navigate.hide()
        self.frame_widget.hide()
        self.frame_info.hide()

        self.verticalLayout_info.addWidget(self.label_info)

        self.centralWidget.setLayout(self.verticalLayout_main)

