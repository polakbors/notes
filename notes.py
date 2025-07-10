import sys
from PyQt5.QtWidgets import QApplication, QWidget
from PyQt5.QtCore import Qt

class FloatingSquare(QWidget):
    def __init__(self):
        super().__init__()

        # Frameless & always-on-top window
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)

        # Starting size & position
        self.resize(200, 200)
        self.move(100, 100)

        # Make the background translucent so our paintEvent shows the RGBA fill
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.show()

    def paintEvent(self, event):
        from PyQt5.QtGui import QPainter, QColor, QPen
        painter = QPainter(self)
        # Semi-transparent red fill
        painter.setBrush(QColor(255, 0, 0, 128))
        # Black border, 2px wide
        pen = QPen(QColor(0, 0, 0))
        pen.setWidth(2)
        painter.setPen(pen)
        painter.drawRect(self.rect())

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Ask Qt to start a native window drag
            win_handle = self.windowHandle()
            if win_handle is not None:
                win_handle.startSystemMove()
            event.accept()
        else:
            super().mousePressEvent(event)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    square = FloatingSquare()
    sys.exit(app.exec_())
