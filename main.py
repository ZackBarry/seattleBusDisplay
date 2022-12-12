import logging
import threading
import time

from data import Data
from renderers.main import MainRenderer

logger = logging.getLogger("busses")

try:
    from rgbmatrix import RGBMatrix, __version__
    emulated = False
except ImportError:
    from RGBMatrixEmulator import RGBMatrix, version
    emulated = True


def main(matrix):
    # Print some basic info on startup
    logger.info("(%sx%s)", matrix.width, matrix.height)

    if emulated:
        logger.debug("rgbmatrix not installed, falling back to emulator!")
        logger.debug("Using RGBMatrixEmulator version %s", version.__version__)
    else:
        logger.debug("Using rgbmatrix version %s", __version__)

    # Create a new data object to manage the MLB data
    # This will fetch initial data from MLB
    data = Data(config)

    # create render thread
    render = threading.Thread(target=__render_main, args=[matrix, data], name="render_thread", daemon=True)
    time.sleep(1)
    render.start()

    __refresh_busses()


def __refresh_busses(render_thread, data):
    logger.debug("Main has selected the busses to refresh")
    while render_thread.is_alive():
        time.sleep(30)
        data.refresh_busses()


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