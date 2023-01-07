import random
from enum import Enum
import math
from abc import abstractmethod
import random
from typing import (
    List
)

from .util import Logger


class CellState(Enum):
    NEWBORN = 'newborn'
    GROWN = 'grown'
    MATURE = 'mature'
    LONG_LIVING = 'longliving'
    DYING = 'dying'


class BasicEvolutionStrategy:

    def __init__(self,
                 grid: 'LifeGrid'):
        self.grid = grid

    @abstractmethod
    def born_new_cell(self,
                      coord_vertical: int,
                      coord_horizontal: int):
        pass

    @abstractmethod
    def if_will_born(self,
                     coord_vertical: int,
                     coord_horizontal: int):
        pass


class ClassicEvolutionStrategy(BasicEvolutionStrategy):

    def born_new_cell(self,
                      coord_vertical: int,
                      coord_horizontal: int):
        return TypicalCell(self.grid, coord_vertical, coord_horizontal)

    def if_will_born(self,
                     coord_vertical: int,
                     coord_horizontal: int):
        alive_neighbours = self.grid.alive_neighbours(coord_vertical, coord_horizontal)
        if TypicalCell.will_survive_with_neighbours(alive_neighbours):
            return TypicalCell
        else:
            return None


class MutationEvolutionStrategy(BasicEvolutionStrategy):

    MAX_AGE = 30

    @property
    def _random_cell_class(self):
        random_int = random.randint(0, 16)
        if random_int in (0, 1):
            cell_class = StandaloneCell
        elif random_int == 2:
            cell_class = SuperStandaloneCell
        elif random_int in (3, 4):
            cell_class = SociableCell
        elif random_int == 5:
            cell_class = SuperSociableCell
        elif random_int in (6, 7):
            cell_class = StandaloneAndSociableCell
        elif random_int == 8:
            cell_class = SuperStandaloneAndSociableCell
        else:
            cell_class = TypicalCell
        return cell_class

    def born_new_cell(self,
                      coord_vertical: int,
                      coord_horizontal: int):
        return self._random_cell_class(self.grid,
                                       coord_vertical,
                                       coord_horizontal)

    def if_will_born(self,
                     coord_vertical: int,
                     coord_horizontal: int):
        alive_neighbours = self.grid.alive_neighbours(coord_vertical, coord_horizontal)
        cell_class = self._random_cell_class
        if cell_class.will_survive_with_neighbours(alive_neighbours):
            return cell_class
        else:
            return None


class BasicCell:

    def __init__(self,
                 grid: 'LifeGrid',
                 coord_vertical: int,
                 coord_horizontal: int):
        self.grid = grid
        self.logger = self.grid.logger
        self.coord_vertical = coord_vertical
        self.coord_horizontal = coord_horizontal
        self.age = 0

    @property
    def state(self) -> CellState:
        if self.age == 0:
            return CellState.NEWBORN
        elif self.age > 0 and self.will_survive:
            if self.age < 5:
                return CellState.GROWN
            elif 5 <= self.age < 15:
                return CellState.MATURE
            else:
                return CellState.LONG_LIVING
        elif not self.will_survive:
            return CellState.DYING
        else:
            raise NotImplementedError

    @classmethod
    def will_survive_with_neighbours(cls, alive_neighbours):
        pass

    @property
    def will_survive(self):
        return self.will_survive_with_neighbours(self.alive_neighbours)

    @property
    def alive_neighbours(self):
        return self.grid.alive_neighbours(self.coord_vertical, self.coord_horizontal)


class TypicalCell(BasicCell):

    @classmethod
    def will_survive_with_neighbours(cls, alive_neighbours):
        return alive_neighbours in (2, 3)


class StandaloneCell(BasicCell):

    @classmethod
    def will_survive_with_neighbours(cls, alive_neighbours):
        return alive_neighbours in (1, 2, 3)


class SuperStandaloneCell(BasicCell):

    @classmethod
    def will_survive_with_neighbours(cls, alive_neighbours):
        return alive_neighbours in (0, 1, 2, 3)


class SociableCell(BasicCell):

    @classmethod
    def will_survive_with_neighbours(cls, alive_neighbours):
        return alive_neighbours in (2, 3, 4)


class SuperSociableCell(BasicCell):

    @classmethod
    def will_survive_with_neighbours(cls, alive_neighbours):
        return alive_neighbours in (2, 3, 4, 5)


class StandaloneAndSociableCell(BasicCell):

    @classmethod
    def will_survive_with_neighbours(cls, alive_neighbours):
        return alive_neighbours in (1, 2, 3, 4)


class SuperStandaloneAndSociableCell(BasicCell):

    @classmethod
    def will_survive_with_neighbours(cls, alive_neighbours):
        return alive_neighbours in (0, 1, 2, 3, 4, 5)


class LifeGrid:

    def __init__(self,
                 evolution_strategy_class,
                 width: int,
                 height: int,
                 birth_probability: float,
                 click_birth_probability: float,
                 click_birth_radius: int,
                 logger: Logger):
        self.evolution_strategy = evolution_strategy_class(self)
        self.logger = logger
        self.width = width
        self.height = height
        self.birth_probability = birth_probability
        self.click_birth_probability = click_birth_probability
        self.click_birth_radius = click_birth_radius
        self.cells: List[List[BasicCell]] = []
        self.generations_count = 0
        for iv in range(self.height):
            row = []
            for ih in range(self.width):
                row.append(None)
            self.cells.append(row)

    def fill_random(self):
        born_count = 0
        for iv in range(self.height):
            for ih in range(self.width):
                rnd = random.random()
                if rnd < self.birth_probability:
                    born_count += 1
                    self.cells[iv][ih] = self.evolution_strategy.born_new_cell(iv, ih)
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
                    if self.cells[iv][ih] is not None:
                        self.cells[iv][ih] = self.evolution_strategy.born_new_cell(self, iv, ih)
                    born_count += 1
        self.logger.info(f'{born_count} cell(s) randomly born by command')

    def alive_neighbours(self, coord_vertical, coord_horizontal):
        iv_from = coord_vertical - 1 if coord_vertical > 0 else 0
        iv_to = coord_vertical + 1 if coord_vertical < self.height - 1 else self.height - 1
        ih_from = coord_horizontal - 1 if coord_horizontal > 0 else 0
        ih_to = coord_horizontal + 1 if coord_horizontal < self.width - 1 else self.width - 1
        alive_neighbours = 0
        for iv in range(iv_from, iv_to + 1):
            for ih in range(ih_from, ih_to + 1):
                if iv == coord_vertical and ih == coord_horizontal:
                    continue
                if self.cells[iv][ih] is not None:
                    alive_neighbours += 1
        return alive_neighbours

    def next_generation(self):
        total_alive_count = 0
        survived_count = 0
        died_count = 0
        born_count = 0
        total_ages = 0
        future_cells = []
        for iv in range(self.height):
            future_cells_row = []
            for ih in range(self.width):
                current_cell = self.cells[iv][ih]
                will_survive = current_cell.will_survive if current_cell is not None else False
                will_born_cell_class = self.evolution_strategy.if_will_born(iv, ih)
                if current_cell is not None:
                    if isinstance(self.evolution_strategy, MutationEvolutionStrategy) and current_cell.age > MutationEvolutionStrategy.MAX_AGE:
                        will_survive = False
                    if will_survive:
                        future_cell = current_cell
                        current_cell.age += 1
                        total_alive_count += 1
                        survived_count += 1
                        total_ages += current_cell.age
                    else:
                        future_cell = None
                        died_count += 1
                else:
                    if will_born_cell_class is not None:
                        future_cell = will_born_cell_class(self, iv, ih)
                        total_alive_count += 1
                        born_count += 1
                        total_ages += 1
                    else:
                        future_cell = None
                future_cells_row.append(future_cell)
            future_cells.append(future_cells_row)
        self.cells = future_cells
        average_age = total_ages / total_alive_count if total_alive_count > 0 else 0
        alive_percent = total_alive_count / (self.width * self.height) * 100
        self.logger.info(f'Generation #{self.generations_count}: {born_count} born, {survived_count} survived, {died_count} died, {total_alive_count}/{self.width * self.height} ({alive_percent:.2f}%) total alive, {average_age:.3f} average age')
        self.generations_count += 1
