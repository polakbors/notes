import sys ,pathlib
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer, QSaveFile, Qt


class FloatingNote(QTextEdit):
    """A frameless, always‑on‑top sticky note you can type into and drag around."""

    def __init__(self, save_path: str | pathlib.Path,x: int = 100, y: int = 100, w: int = 200, h: int = 200, parent=None):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setStyleSheet(
            """
            FloatingNote {
                background: #fff9a0;      
                border: 2px solid #000;
                color: #000;
                font: 12pt "Arial";
            }
            """
        )
        self.setPlaceholderText("Type your note…")
        self.setAcceptRichText(False)
        self._path = pathlib.Path(save_path)
        self._timer = QTimer(self, interval=1_000, singleShot=True)
        self._timer.timeout.connect(self._flush_to_disk)

        self.textChanged.connect(self._timer.start)
        self.setFixedSize(w, h)
        self.move(x, y)
        self.show()

    def mousePressEvent(self, event):
        if (
            event.button() == Qt.LeftButton
            and not self.cursorForPosition(event.pos()).hasSelection()
        ):
            win_handle = self.windowHandle()
            if win_handle is not None:
                win_handle.startSystemMove()
            event.accept()
        else:
            super().mousePressEvent(event)
    
    def _flush_to_disk(self):
        data = self.toPlainText().encode("utf-8")

        # QSaveFile writes to a temp file first, then atomically renames → no
        # risk of ending up with half-written files if the app crashes.
        f = QSaveFile(str(self._path))
        if f.open(QSaveFile.WriteOnly | QSaveFile.Text):
            f.write(data)
            f.commit()




if __name__ == "__main__":
    app = QApplication(sys.argv)
    note = FloatingNote("note.txt")
    sys.exit(app.exec_())
