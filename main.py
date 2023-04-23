import logging
import threading
import time
import sys

from metro.data import Data
from renderers.main import MainRenderer

logger = logging.getLogger("busses")

try:
    from rgbmatrix import RGBMatrix, __version__
    emulated = False
except ImportError:
    from RGBMatrixEmulator import RGBMatrix, version
    emulated = True


"""
The data object has methods for saving the data

The MainRenderer handles creating the matrix from Data
    it does this by calling a render method, busses.render_busses

The __render_xxx functions update Data every N seconds, which MainRenderer 
   receives via reference

"""


def main(matrix):
    logger.info("(%sx%s)", matrix.width, matrix.height)

    if emulated:
        logger.debug("rgbmatrix not installed, falling back to emulator!")
        logger.debug("Using RGBMatrixEmulator version %s", version.__version__)
    else:
        logger.debug("Using rgbmatrix version %s", __version__)

    data = Data()

    render = threading.Thread(target=__render_main, args=[matrix, data], name="render_thread", daemon=True)
    time.sleep(1)
    render.start()

    __refresh_busses()


def __refresh_busses(render_thread, data):
    logger.debug("Main has selected the busses to refresh")
    while render_thread.is_alive():
        time.sleep(30)
        data.update_stop_statuses()


def __render_main(matrix, data):
    MainRenderer(matrix, data).render()

if __name__ == "__main__":
    matrix = RGBMatrix()
    try:
        main(matrix)
    except:
        logger.exception("Untrapped error in main!")
        sys.exit(1)
    finally:
        matrix.Clear()