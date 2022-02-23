import sys
import argparse
from PyQt5.QtWidgets import QApplication
from PyQt5 import QtCore

import newlifelib


life_window: newlifelib.graphics.LifeWindow = None


def timer_event():
    life_window.life_grid.next_generation()
    life_window.update()


def main():
    args = parse_command_line_args()
    logger = newlifelib.util.Logger(debug=args.debug)
    App = QApplication(sys.argv)
    global life_window
    life_window = newlifelib.graphics.LifeWindow(args, args.cell_size, logger)
    timer = QtCore.QTimer()
    timer.timeout.connect(timer_event)
    timer.start(args.period_milliseconds)
    return App.exec()


def parse_command_line_args():
    parser = argparse.ArgumentParser(description='Conway\'s Game of Life with Qt frontend')
    parser.add_argument('-d',
                        '--debug',
                        action='store_true',
                        help='Enable debugging output')
    parser.add_argument('-f',
                        '--fullscreen',
                        action='store_true',
                        help='Enable fullscreen')
    parser.add_argument('-m',
                        '--maximized',
                        action='store_true',
                        help='Enable maximized window')
    parser.add_argument('--width',
                        default=500,
                        type=int,
                        help='Life grid width')
    parser.add_argument('--height',
                        default=500,
                        type=int,
                        help='Life grid height')
    parser.add_argument('-c',
                        '--cell-size',
                        default=1,
                        type=int,
                        help='Life grid cell size')
    parser.add_argument('-b',
                        '--birth-probability',
                        default=0.5,
                        type=float,
                        help='Probability of initial births of cells in [0, 1] float range')
    parser.add_argument('-l',
                        '--click-birth-probability',
                        default=0.5,
                        type=float,
                        help='Probability of births of cells by click in [0, 1] float range')
    parser.add_argument('-r',
                        '--click-birth-radius',
                        default=50,
                        type=float,
                        help='Probability of births of cells by click in [0, 1] float range')
    parser.add_argument('-p',
                        '--period-milliseconds',
                        default=1000,
                        type=int,
                        help='Time period between generations in milliseconds')
    parser.add_argument('-u',
                        '--use-primary-screen',
                        action='store_true',
                        help='Use primary screen instead of current')
    args = parser.parse_args()
    return args


if __name__ == '__main__':
    sys.exit(main())
