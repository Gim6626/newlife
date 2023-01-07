from enum import Enum

from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtGui import (
    QPainter,
    QBrush,
)
from PyQt5 import QtGui
from PyQt5.QtCore import (
    Qt,
    QPoint,
)

from newlifelib.logic import *


class ColorMode(Enum):
    MONOCHROME = 'monochrome'
    COLOR = 'color'


class LifeWindow(QMainWindow):

    def __init__(self,
                 args,
                 logger):
        super().__init__()
        self.cell_size = args.cell_size
        self.color_mode = args.color_mode
        if args.fullscreen or args.maximized:
            if args.use_primary_screen:
                geometry = QApplication.instance().primaryScreen().availableGeometry()
            else:
                geometry = self.screen().size()
            grid_width = int(geometry.width() / self.cell_size)
            grid_height = int(geometry.height() / self.cell_size)
        else:
            grid_width = args.width
            grid_height = args.height
        self.life_grid = LifeGrid(args.evolution_strategy_class,
                                  grid_width,
                                  grid_height,
                                  args.birth_probability,
                                  args.click_birth_probability,
                                  args.click_birth_radius,
                                  logger)
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

    def mousePressEvent(self, a0: QtGui.QMouseEvent) -> None:
        self.life_grid.make_random_birth(int(a0.x() / self.cell_size),
                                         int(a0.y() / self.cell_size))

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setBrush(QBrush(Qt.black))
        painter.drawRect(0,
                         0,
                         self.life_grid.width * self.cell_size,
                         self.life_grid.height * self.cell_size)
        for iv in range(self.life_grid.height):
            for ih in range(self.life_grid.width):
                current_cell = self.life_grid.cells[iv][ih]
                if current_cell is None:
                    continue
                state = current_cell.state

                if self.color_mode == ColorMode.MONOCHROME:
                    if isinstance(self.life_grid.evolution_strategy, ClassicEvolutionStrategy):
                        if state in (CellState.NEWBORN,
                                     CellState.GROWN,
                                     CellState.MATURE,
                                     CellState.LONG_LIVING):
                            primary_color = Qt.white
                            secondary_color = Qt.gray
                        elif state == CellState.DYING:
                            primary_color = Qt.black
                            secondary_color = Qt.black
                        else:
                            raise NotImplementedError
                    elif isinstance(self.life_grid.evolution_strategy, MutationEvolutionStrategy):
                        # TODO: Implement
                        raise NotImplementedError
                    else:
                        raise NotImplementedError
                elif self.color_mode == ColorMode.COLOR:
                    if isinstance(self.life_grid.evolution_strategy, ClassicEvolutionStrategy):
                        if state == CellState.NEWBORN:
                            primary_color = Qt.green
                            secondary_color = Qt.white
                        elif state == CellState.GROWN:
                            primary_color = Qt.blue
                            secondary_color = Qt.white
                        elif state == CellState.MATURE:
                            primary_color = Qt.cyan
                            secondary_color = Qt.white
                        elif state == CellState.LONG_LIVING:
                            primary_color = Qt.yellow
                            secondary_color = Qt.white
                        elif state == CellState.DYING:
                            primary_color = Qt.red
                            secondary_color = Qt.white
                        else:
                            raise NotImplementedError
                    elif isinstance(self.life_grid.evolution_strategy, MutationEvolutionStrategy):
                        if state == CellState.NEWBORN:
                            secondary_color = Qt.green
                        elif state == CellState.GROWN:
                            secondary_color = Qt.blue
                        elif state == CellState.MATURE:
                            secondary_color = Qt.cyan
                        elif state == CellState.LONG_LIVING:
                            secondary_color = Qt.yellow
                        elif state == CellState.DYING:
                            secondary_color = Qt.red
                        else:
                            raise NotImplementedError
                        if isinstance(current_cell, TypicalCell):
                            primary_color = Qt.gray
                        elif isinstance(current_cell, StandaloneCell):
                            primary_color = Qt.darkMagenta
                        elif isinstance(current_cell, SociableCell):
                            primary_color = Qt.darkCyan
                        elif isinstance(current_cell, StandaloneAndSociableCell):
                            primary_color = Qt.darkYellow
                        elif isinstance(current_cell, SuperStandaloneCell):
                            primary_color = Qt.darkBlue
                        elif isinstance(current_cell, SuperSociableCell):
                            primary_color = Qt.darkGreen
                        elif isinstance(current_cell, SuperStandaloneAndSociableCell):
                            primary_color = Qt.white
                        else:
                            raise NotImplementedError
                    else:
                        raise NotImplementedError
                else:
                    raise NotImplementedError

                if isinstance(self.life_grid.evolution_strategy, ClassicEvolutionStrategy) \
                        or isinstance(self.life_grid.evolution_strategy, MutationEvolutionStrategy):
                    painter.setBrush(QBrush(secondary_color))
                    painter.drawEllipse(QPoint(ih * self.cell_size - math.ceil(self.cell_size / 2),
                                               iv * self.cell_size - math.ceil(self.cell_size / 2)),
                                        math.ceil(self.cell_size / 2) - 1,
                                        math.ceil(self.cell_size / 2) - 1)
                    painter.setBrush(QBrush(primary_color))
                    painter.drawEllipse(QPoint(ih * self.cell_size - math.ceil(self.cell_size / 2),
                                               iv * self.cell_size - math.ceil(self.cell_size / 2)),
                                        math.ceil(self.cell_size / 4),
                                        math.ceil(self.cell_size / 4))
                else:
                    raise NotImplementedError
        painter.end()
