import os
import sys ,pathlib, argparse
from typing import Optional
from PyQt5.QtWidgets import QApplication, QTextEdit, QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import QTimer, QSaveFile, Qt
from PyQt5.QtGui import QGuiApplication, QIcon

class FloatingNote(QTextEdit):
    """A frameless, always‑on‑top sticky note you can type into and drag around."""

    def __init__(self, save_path: str | pathlib.Path,color: Optional[str] = None, fontcolour: Optional[str] = None,pernament: Optional[bool]=None,
                 sizex: Optional[int] = 300, sizey: Optional[int] = 300, fontsize: Optional[int] = 12, txtin: Optional[str] = "",
                 resize: Optional[bool] = False, x: int = 100, y: int = 100):
        super().__init__()
        print(resize, "resize")
        self.resized = resize
        self.color = color
        self.fontcolour = fontcolour
        self.pernament = pernament
        self.sizex = sizex
        self.sizey = sizey
        self.fontsize = fontsize
        self.txtin = txtin
        perna=self.pernament or False
        self.setWindowTitle(save_path)
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
        self.setText(txtin)
        self.setFontPointSize(fontsize)
        self.setLineWrapMode(QTextEdit.WidgetWidth)
        if not perna :
            save_path= f"/tmp/{save_path}"
        self._path = pathlib.Path(save_path)
        self._timer = QTimer(self, interval=1_000, singleShot=True)
        self._timer.timeout.connect(self._flush_to_disk)

        self.textChanged.connect(self._timer.start)
        print(self.resized)
        if self.resized:
            self.setMinimumSize(self.sizex, self.sizey)
            self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            self.setWindowFlags(self.windowFlags() | Qt.Window )  # Add normal window frame for resizing
        else:
            self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
            self.setFixedSize(sizex, sizey)
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
    parser.add_argument("--pernament", action="store_true", help="...")
    parser.add_argument("--sizex", type=int, default=100, help="X position of the note")
    parser.add_argument("--sizey", type=int, default=100, help="Y position of the note")
    parser.add_argument("--fontsize", type=int, default=12, help="Font size of the note")
    parser.add_argument("--txtin", type=str, default="", help="Initial text in the note")
    parser.add_argument("--resize", action="store_true", help="Enable note resizing")
    args = parser.parse_args()
    print(args.name, args.color, args.fontcolour, args.pernament, args.sizex, args.sizey, args.fontsize, args.txtin, args.resize)
    app = QApplication(sys.argv)
    app.setApplicationName(args.name)           
    app.setApplicationDisplayName(args.name)    
    QGuiApplication.setDesktopFileName(f"{args.name}") 

    # set the icon once for the whole app
    #to fix #icon_path = "/home/borysrzepa/notes/notes/clippy.png"
    #app.setWindowIcon(QIcon(icon_path))
    note = FloatingNote(args.name,args.color,args.fontcolour,args.pernament , args.sizex, args.sizey, args.fontsize, args.txtin, args.resize)
    sys.exit(app.exec_())
