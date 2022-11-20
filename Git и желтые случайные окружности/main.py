import sys
import random

from PyQt5 import uic
from PyQt5.QtGui import QPainter, QColor
from PyQt5.QtWidgets import QWidget, QApplication


class Example(QWidget):
    MINIMAL_DIAMETER = 10

    def __init__(self):
        super().__init__()
        uic.loadUi("UI.ui", self)
        self.pushButton.clicked.connect(self.click)
        self.is_draw = False

    def paintEvent(self, event):
        if self.is_draw:
            qp = QPainter()
            qp.begin(self)
            self.draw_circle(qp)
            qp.end()

    def click(self):
        self.is_draw = True
        self.update()

    def draw_circle(self, qp):
        color = QColor(*[random.randint(0, 255) for _ in range(3)])
        diameter = random.randint(self.MINIMAL_DIAMETER,
                                  min(self.width(), self.height()) // 2)
        qp.setBrush(color)
        x = random.randint(0, self.width() - diameter)
        y = random.randint(0, self.height() - diameter)
        qp.drawEllipse(x, y, diameter, diameter)


def my_exception_hook(exctype, value, traceback):
    print(exctype, value, traceback)
    sys._excepthook(exctype, value, traceback)
    sys.exit(1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    sys._excepthook = sys.excepthook
    sys.excepthook = my_exception_hook
    ex = Example()
    ex.show()
    sys.exit(app.exec())
