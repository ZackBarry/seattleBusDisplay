#!/usr/bin/env python
from samplebase import SampleBase
from metro.data import Data
from metro.context import download_context
import time

try:
    from rgbmatrix import graphics
except ImportError:
    from RGBMatrixEmulator import graphics


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.bus_names = [
            ["31S", "32S"],
            ["44W"],
            ["44E", "31N", "32N"],
        ]

    def run(self):
        # download_context()

        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("./assets/fonts/7x13.bdf")
        COLOR = {
            'delayed': graphics.Color(255, 87, 51),
            'on-time': graphics.Color(255, 215, 0),
            'ahead':   graphics.Color(80, 200, 120),
        }

        time_passed_ms = 0
        time_passed_s = 0
        bus_index = 0
        data = Data()
        data.update_stop_statuses()

        while True:
            offscreen_canvas.Clear()

            bus_names = self.bus_names[bus_index]
            statuses = data.get_bus_statuses(bus_names)
 
            for i in range(min(len(statuses), 3)):  
                status = statuses[i]
                text = status['text']
                color = COLOR[status['status']]
                text_width = sum([font.CharacterWidth(ord(letter)) for letter in text])
                led_width = 64
                pos = max(0, (64 - text_width) // 2 + 1)
                text_len = graphics.DrawText(
                    offscreen_canvas, font, pos, 10 + 10 * i, 
                    color, text
                )

            time.sleep(0.05)
            time_passed_ms += 50
            time_passed_s = time_passed_ms // 1000

            if time_passed_ms % 1000 == 0:
                if (time_passed_s % 30) == 0:
                    print(f'Updating, {time_passed_s}')
                    data.update_stop_statuses()
                    stop_index = 0
                if (time_passed_s % 5) == 0:
                    bus_index += 1
                    bus_index %= len(self.bus_names)

            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()