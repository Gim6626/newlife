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
    timer.start(1000)
    return App.exec()


def parse_command_line_args():
    # TODO: Add birth probability option
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
                        help='Life grid width')
    parser.add_argument('--height',
                        default=500,
                        help='Life grid height')
    parser.add_argument('-c',
                        '--cell-size',
                        default=1,
                        help='Life grid cell size')
    parser.add_argument('-p',
                        '--period',
                        default=1,
                        help='Time period between generations')
    args = parser.parse_args()
    # TODO: Refactor
    args.cell_size = int(args.cell_size)
    args.width = int(args.width)
    args.height = int(args.height)
    args.period = int(args.period)
    #
    return args


if __name__ == '__main__':
    sys.exit(main())
