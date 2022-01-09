from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPainter, QPen
from PyQt5.QtCore import Qt

from newlifelib.logic import *


class LifeWindow(QMainWindow):

    def __init__(self,
                 args,
                 cell_size: int,
                 logger):
        super().__init__()
        self.cell_size = cell_size
        if args.fullscreen or args.maximized:
            grid_width = int(self.screen().size().width() / self.cell_size)
            grid_height = int(self.screen().size().height() / self.cell_size)
        else:
            grid_width = args.width
            grid_height = args.height
        self.life_grid = LifeGrid(grid_width, grid_height, logger)
        self.life_grid.fill_random()
        self.title = 'New Life'
        self.top = 0
        self.left = 0
        self.width = self.life_grid.width
        self.height = self.life_grid.height
        self.fullscreen = args.fullscreen
        self.maximized = args.maximized
        self.InitWindow()

    def InitWindow(self):
        self.setWindowTitle(self.title)
        if self.fullscreen:
            self.showFullScreen()
        elif self.maximized:
            self.showMaximized()
        else:
            self.setGeometry(self.top,
                             self.left,
                             self.life_grid.width * self.cell_size,
                             self.life_grid.height * self.cell_size)
            self.show()

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        for iv in range(self.life_grid.height):
            for ih in range(self.life_grid.width):
                state = self.life_grid.cells[iv][ih].state
                if state == CellState.NEWBORN:
                    color = Qt.green
                elif state == CellState.GROWN:
                    color = Qt.blue
                elif state == CellState.MATURE:
                    color = Qt.cyan
                elif state == CellState.LONG_LIVING:
                    color = Qt.yellow
                elif state == CellState.DYING:
                    color = Qt.red
                elif state == CellState.NONE:
                    color = Qt.black
                else:
                    raise NotImplementedError
                painter.setPen(QPen(color, self.cell_size))
                painter.drawPoint(ih * self.cell_size, iv * self.cell_size)
        painter.end()
