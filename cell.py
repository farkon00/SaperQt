from PyQt5 import QtCore, QtGui, QtWidgets


class Cell(QtWidgets.QPushButton):
    def __init__(self, x, y, grid, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self._x = x
        self._y = y

        self.grid = grid 

        self.is_bomb = self.is_revealed = self.is_flagged = False

        self.clicked.connect(self.on_click)

    def paintEvent(self, event):
        """
        Renders cell
        """
        p = QtGui.QPainter(self)
        p.setRenderHint(QtGui.QPainter.RenderHint.Antialiasing)
        r = event.rect()
        outer, inner = QtCore.Qt.GlobalColor.gray, QtCore.Qt.GlobalColor.lightGray
        p.fillRect(r, QtGui.QBrush((inner if not self.is_bomb else QtCore.Qt.GlobalColor.red) if self.is_revealed else outer))
        pen = QtGui.QPen(outer)
        pen.setWidth(1)
        p.setPen(pen)
        p.drawRect(r)

        around = self.grid.count_mines_around(self._x, self._y)
        if self.is_revealed and not self.is_bomb and around > 0:
            self.setStyleSheet("color: black; font-weight: bold;")
            p.drawText(r, QtCore.Qt.AlignmentFlag.AlignCenter, str(around))

        if self.is_revealed and self.is_bomb:
            self.setStyleSheet("color: black; font-weight: bold;")
            p.drawText(r, QtCore.Qt.AlignmentFlag.AlignCenter, "X")

    def on_click(self) -> None:
        self.grid.reveal_cells(self._x, self._y)
        self.grid.place_mines()
        self.update()