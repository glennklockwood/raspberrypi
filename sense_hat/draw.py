#!/usr/bin/env python3
"""Use the joystick to draw on the pixel display.  Press the joystick to toggle
between colors and eraser mode.
"""

import sense_hat

COLORS = [
    (255,   0,   0),
    (  0, 255,   0),
    (  0,   0, 255),
    (255, 255,   0),
    (  0, 255, 255),
    (255,   0, 255),
    (  0,   0,   0),
]

def event_loop(sense):
    current_xy = [0, 0]
    current_color_idx = 0
    sense.set_pixel(current_xy[0], current_xy[1], *(COLORS[current_color_idx]))

    while True:
        prev_color = None
        for event in sense.stick.get_events():
            event_act = event.action[0].lower()
            event_dir = event.direction[0].lower()
            if event_act in ("p", "h"):
                if event_dir != 'm':
                    if prev_color is not None:
                        sense.set_pixel(current_xy[0], current_xy[1], *prev_color)
                    if event_dir == "l":
                        current_xy[0] = (current_xy[0] - 1) % 8
                    elif event_dir == "r":
                        current_xy[0] = (current_xy[0] + 1) % 8
                    elif event_dir == "u":
                        current_xy[1] = (current_xy[1] - 1) % 8
                    elif event_dir == "d":
                        current_xy[1] = (current_xy[1] + 1) % 8
                    prev_color = sense.get_pixel(current_xy[0], current_xy[1])
                else:
                    current_color_idx = (current_color_idx + 1) % len(COLORS)
                sense.set_pixel(current_xy[0], current_xy[1], *(COLORS[current_color_idx]))

if __name__ == "__main__":
    sense = sense_hat.SenseHat()
    sense.clear()
    print("Ready!")
    event_loop(sense)
