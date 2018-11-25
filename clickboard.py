import random

import sys
import os

from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QHBoxLayout,
    QVBoxLayout
)
from PyQt5.QtGui import QCursor, QPainter
from PyQt5.QtCore import Qt, QPoint, QEvent


class Window(QMainWindow):
    def __init__(self):
        super().__init__()

        self.currentChoice = Chooser()
        self.setCentralWidget(self.currentChoice)

        self.currentChoice.installEventFilter(self)

        self.setWindowOpacity(0.3)
        self.showFullScreen()

        self.originalCursorPosition = QCursor.pos()

        self.centerCursor()

    def keyPressEvent(self, event):
        direction = None
        key = event.key()
        if key == Qt.Key_Escape:
            QCursor.setPos(self.originalCursorPosition)
            sys.exit()
        elif key == Qt.Key_Space:
            self.close()
            # TODO Do this nicer ...
            os.system('xdotool click 1')
        elif key == Qt.Key_H:
            direction = 'horizontal'
            choice = 0
        elif key == Qt.Key_L:
            direction = 'horizontal'
            choice = 1
        elif key == Qt.Key_K:
            direction = 'vertical'
            choice = 0
        elif key == Qt.Key_J:
            direction = 'vertical'
            choice = 1

        if direction:
            self.currentChoice.removeEventFilter(self)
            self.currentChoice = self.currentChoice.split(direction, choice)
            self.currentChoice.installEventFilter(self)

    def eventFilter(self, target, event):
        if event.type() == QEvent.Resize:
            self.centerCursor()

        return True

    def centerCursor(self):
        center = self.currentChoice.size() / 2
        QCursor.setPos(self.currentChoice.parentWidget().mapToGlobal(
            self.currentChoice.pos()
            + QPoint(center.width(), center.height())
        ))


class Chooser(QWidget):
    def __init__(self):
        super().__init__()

        self.isSplit = False

    # TODO There should be an easier way to get a mono-colored view
    #   If you delete this, remember to get rid of the flag as well
    def paintEvent(self, event):
        # TODO Pick nicer colors
        #   In particular you might want to think about visibility issues
        # TODO Think about a better visualization
        #   Maybe the window could actually become smaller
        painter = QPainter()
        painter.begin(self)
        if self.isSplit:
            painter.fillRect(event.rect(), Qt.red)
        else:
            painter.fillRect(event.rect(), Qt.white)
        super().paintEvent(event)
        painter.end()

    def split(self, direction, choice):
        self.isSplit = True

        choice1 = Chooser()
        choice2 = Chooser()

        layout = Chooser._layouts[direction]()
        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)

        layout.addWidget(choice1)
        layout.addWidget(choice2)

        self.setLayout(layout)

        choice = (choice1, choice2)[choice]

        choice.show()
        return choice

    _layouts = {'horizontal': QHBoxLayout, 'vertical': QVBoxLayout}


if __name__ == '__main__':
    app = QApplication([])
    window = Window()
    app.exec()
