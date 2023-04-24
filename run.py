#!/usr/bin/env python
import time
from datetime import datetime

from samplebase import SampleBase
from metro.data import Data
from metro.context import download_context

try:
    from rgbmatrix import graphics
except ImportError:
    from RGBMatrixEmulator import graphics

REFRESH_S = 30
SWITCH_S = 5
MS_PER_S = 1000
COLOR = graphics.Color(255, 234, 0)


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.dirs = ["Ba", "Fr", "UW"]
        self.bus_names = {
            "Ba": ["44W"],
            "Fr": ["31S", "32S"],
            "UW": ["44E", "31N", "32N"],
        }

    def run(self):
        # download_context()

        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./assets/fonts/7x13.bdf")

        time_passed_ms = 0
        dir_index = 0
        data = Data()
        data.update_stop_statuses()

        while True:
            offscreen_canvas.Clear()

            if datetime.now().hour >= 23 or datetime.now().hour < 6:
                time.sleep(300)
                time_passed_ms =0

            if time_passed_ms % (REFRESH_S * MS_PER_S) == 0:
                data.update_stop_statuses()

            if (time_passed_ms % (SWITCH_S * MS_PER_S)) == 0:
                dir_index += 1
                dir_index %= len(self.dirs)
                if 0 <= datetime.now().weekday() <= 4 and datetime.now().hour < 8:
                        dir = "Fr"
                        bus_names = ["31S", "32S"]
                else:
                    dir = self.dirs[dir_index]
                    bus_names = self.bus_names[dir]
                statuses = data.get_bus_statuses(bus_names)

            short_dir = dir.strip()
            dir_start = 1 if len(short_dir) == 2 else 5
            graphics.DrawText(
                offscreen_canvas, font, dir_start, 10, 
                COLOR, short_dir
            )
            for i in range(min(len(statuses), 3)):  
                status = statuses[i]
                route = status['route'][:2]
                eta = status['short_time']
                dir_width = sum([font.CharacterWidth(ord(letter)) for letter in dir])
                led_width = 64
                pos_dir = max(0, (led_width - dir_width) // 2 + 1)
                pos_desc = pos_dir - 2

                graphics.DrawText(
                    offscreen_canvas, font, pos_desc, 10 + 10 * i, 
                    COLOR, route
                )
                offscreen_canvas.SetPixel(pos_desc + 17, 10 * i + 5, 255, 234, 0)
                graphics.DrawText(
                    offscreen_canvas, font, pos_desc + 22, 10 + 10 * i, 
                    COLOR, eta
                )

                for j in range(min(status['offset'], 9)):
                    if status['status'] == 'delayed':
                        offscreen_canvas.SetPixel(self.matrix.width - 2, 10 * i + 1 + j, 255, 0, 0)
                    elif status['status'] == 'ahead':
                        offscreen_canvas.SetPixel(self.matrix.width - 2, 10 * i + 1 + j, 0, 255, 0)

            sec_remaining = SWITCH_S - (time_passed_ms // MS_PER_S) % SWITCH_S - 1
            for i in range(sec_remaining):
                offscreen_canvas.SetPixel(1 + 3*i, 12, 0, 0, 255)
                offscreen_canvas.SetPixel(1 + 3*i + 1, 12, 0, 0, 255)
                offscreen_canvas.SetPixel(1 + 3*i + 2, 12, 0, 0, 255)

            time.sleep(0.05)
            time_passed_ms += 50

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()