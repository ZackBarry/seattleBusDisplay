import time
import logging

from data import Data, status
from renderers import busses

logger = logging.getLogger("render")


class MainRenderer:
    def __init__(self, matrix, data):
        self.matrix = matrix
        self.data = data
        self.canvas = matrix.CreateFrameCanvas()
        self.scrolling_text_pos = self.canvas.width
        self.bus_changed_time = time.time()
        self.animation_time = 0

    def render(self):
        self.__render_busses()

    def __render_busses(self):
        self.__draw_busses(stick=True)

    def __draw_busses(self, *, stick=False):
        while True:
            busses.render_busses(
                self.canvas,
                self.data,
            )