import logging
from colorama import Fore, Style
import sys


class Formatter(logging.Formatter):

    def __init__(self, fmt=None):
        if fmt is None:
            fmt = self._colorized_fmt()
        logging.Formatter.__init__(self, fmt)

    def _colorized_fmt(self, color=Fore.RESET):
        return f'{color}[%(asctime)s] %(levelname)s: %(message)s{Style.RESET_ALL}'

    def format(self, record):
        # Save the original format configured by the user
        # when the logger formatter was instantiated
        format_orig = self._style._fmt

        # Replace the original format with one customized by logging level
        if record.levelno == logging.DEBUG:
            color = Fore.CYAN
        elif record.levelno == logging.INFO:
            color = Fore.GREEN
        elif record.levelno == logging.WARNING:
            color = Fore.YELLOW
        elif record.levelno == logging.ERROR:
            color = Fore.RED
        elif record.levelno == logging.CRITICAL:
            color = Fore.MAGENTA
        else:
            color = Fore.WHITE
        self._style._fmt = self._colorized_fmt(color)

        # Call the original formatter class to do the grunt work
        result = logging.Formatter.format(self, record)

        # Restore the original format configured by the user
        self._style._fmt = format_orig

        return result


class Logger(logging.Logger):

    def __init__(self, debug=False):
        super().__init__('fntools')
        h = logging.StreamHandler(sys.stderr)
        f = Formatter()
        h.setFormatter(f)
        h.flush = sys.stderr.flush
        self.addHandler(h)
        if debug:
            self.setLevel(logging.DEBUG)
        else:
            self.setLevel(logging.INFO)
