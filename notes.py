import sys ,pathlib, argparse
from typing import Optional
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout
from PyQt5.QtCore import QTimer, QSaveFile, Qt


class FloatingNote(QTextEdit):
    """A frameless, always‑on‑top sticky note you can type into and drag around."""

    def __init__(self, save_path: str | pathlib.Path,color: Optional[str] = None, fontcolour: Optional[str] = None,pernament: Optional[bool]=None,x: int = 100, y: int = 100, w: int = 200, h: int = 200, parent=None):
        super().__init__()
        self.color = color
        self.fontcolour = fontcolour
        self.pernament = pernament
        perna=self.pernament or False
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        bg = self.color  or "#fff9a0"
        fg = self.fontcolour or "#000"
        self.setStyleSheet(f"""
            FloatingNote {{
                background: {bg};
                border: 2px solid #000;
                color: {fg};
                font: 12pt "Arial";
            }}
        """)

        self.setPlaceholderText("Type your note…")
        self.setAcceptRichText(False)
        if perna :
            save_path= f"tmp/{save_path}"
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
    parser = argparse.ArgumentParser(description="Floating note app")

    parser.add_argument("--name")
    parser.add_argument("--color")
    parser.add_argument("--fontcolour")
    parser.add_argument("--pernament")
    args = parser.parse_args()
    app = QApplication(sys.argv)
    note = FloatingNote(args.name,args.color,args.fontcolour,args.pernament)
    sys.exit(app.exec_())
