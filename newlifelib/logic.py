import random
from enum import Enum
import math

from .util import Logger


class CellState(Enum):
    NEWBORN = 'newborn'
    GROWN = 'grown'
    MATURE = 'mature'
    LONG_LIVING = 'longliving'
    DYING = 'dying'
    NONE = 'none'


class Cell:
    def __init__(self,
                 grid: 'LifeGrid',
                 coord_vertical: int,
                 coord_horizontal: int,
                 alive: bool = None,
                 age: int = None):
        self.grid = grid
        self.logger = self.grid.logger
        self.coord_vertical = coord_vertical
        self.coord_horizontal = coord_horizontal
        self.alive = alive
        self.alive_prev = None
        self.alive_next = None
        self.age = age

    @property
    def state(self) -> CellState:
        if not self.alive_prev and self.alive:
            return CellState.NEWBORN
        elif self.alive_prev and self.alive:
            if self.age < 5:
                return CellState.GROWN
            elif 5 <= self.age < 50:
                return CellState.MATURE
            else:
                return CellState.LONG_LIVING
        elif not self.alive and self.alive_prev:
            return CellState.DYING
        else:
            return CellState.NONE

    def next_generation(self):
        self.alive_prev = self.alive
        self.alive = self.alive_next
        self.alive_next = None

    def kill(self):
        self.alive_next = False
        self.age = 0

    def give_birth(self):
        self.alive_next = True
        self.age = 0

    def live_more(self):
        self.alive_next = True
        self.age += 1

    @property
    def alive_neighbours(self):
        iv_from = self.coord_vertical - 1 if self.coord_vertical > 0 else 0
        iv_to = self.coord_vertical + 1 if self.coord_vertical < self.grid.height - 1 else self.grid.height - 1
        ih_from = self.coord_horizontal - 1 if self.coord_horizontal > 0 else 0
        ih_to = self.coord_horizontal + 1 if self.coord_horizontal < self.grid.width - 1 else self.grid.width - 1
        alive_neighbours = 0
        for iv in range(iv_from, iv_to + 1):
            for ih in range(ih_from, ih_to + 1):
                if iv == self.coord_vertical and ih == self.coord_horizontal:
                    continue
                if self.grid.cells[iv][ih].alive:
                    alive_neighbours += 1
        return alive_neighbours


class LifeGrid:

    def __init__(self,
                 width: int,
                 height: int,
                 birth_probability: float,
                 click_birth_probability: float,
                 click_birth_radius: int,
                 logger: Logger):
        self.logger = logger
        self.width = width
        self.height = height
        self.birth_probability = birth_probability
        self.click_birth_probability = click_birth_probability
        self.click_birth_radius = click_birth_radius
        self.cells = []
        self.generations_count = 0
        for iv in range(self.height):
            row = []
            for ih in range(self.width):
                row.append(Cell(self, iv, ih, False, 0))
            self.cells.append(row)

    def fill_random(self):
        born_count = 0
        for iv in range(self.height):
            for ih in range(self.width):
                rnd = random.random()
                if rnd < self.birth_probability:
                    self.cells[iv][ih].alive = True
                    born_count += 1
                else:
                    self.cells[iv][ih].alive = False
        self.logger.info(f'{born_count} cell(s) randomly born')
        self.generations_count += 1

    def make_random_birth(self, x: int, y: int):
        born_count = 0
        radius_v = self.click_birth_radius
        radius_h = self.click_birth_radius
        iv_from = int(y - radius_v if y - radius_v > 0 else 0)
        iv_to = int(y + radius_v if y + radius_v < self.height - 1 else self.height - 1)
        ih_from = int(x - radius_h if x - radius_h > 0 else 0)
        ih_to = int(x + radius_h if x + radius_h < self.width - 1 else self.width- 1)
        for iv in range(iv_from, iv_to + 1):
            for ih in range(ih_from, ih_to + 1):
                if math.fabs(ih - x)**2 / radius_h**2 + math.fabs(iv - y)**2 / radius_v**2 > 1:
                    continue
                rnd = random.random()
                if rnd < self.click_birth_probability:
                    self.cells[iv][ih].alive = True
                    born_count += 1
                else:
                    self.cells[iv][ih].alive = False
        self.logger.info(f'{born_count} cell(s) randomly born by command')

    def next_generation(self):
        total_alive_count = 0
        survived_count = 0
        died_count = 0
        born_count = 0
        total_ages = 0
        for iv in range(self.height):
            for ih in range(self.width):
                current_cell = self.cells[iv][ih]
                alive_neighbours = current_cell.alive_neighbours
                alive_next = True if alive_neighbours in (2, 3) else False
                if current_cell.alive and alive_next:
                    current_cell.live_more()
                    total_alive_count += 1
                    survived_count += 1
                    total_ages += current_cell.age
                elif current_cell.alive and not alive_next:
                    current_cell.kill()
                    died_count += 1
                elif not current_cell.alive and alive_next:
                    current_cell.give_birth()
                    total_alive_count += 1
                    born_count += 1
                    total_ages += 1
                elif not current_cell.alive and not alive_next:
                    pass
                else:
                    self.logger.critical(f'Invalid alive ({current_cell.alive}) and alive next ({alive_next}) combination for cell [{iv}, {ih}]')
                    raise NotImplementedError
        for iv in range(self.height):
            for ih in range(self.width):
                self.cells[iv][ih].next_generation()
        average_age = total_ages / total_alive_count if total_alive_count > 0 else 0
        alive_percent = total_alive_count / (self.width * self.height)
        self.logger.info(f'Generation #{self.generations_count}: {born_count} born, {survived_count} survived, {died_count} died, {total_alive_count}/{self.width * self.height} ({alive_percent:.2f}%) total alive, {average_age:.3f} average age')
        self.generations_count += 1
