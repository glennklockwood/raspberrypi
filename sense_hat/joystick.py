#!/usr/bin/env python3
"""Demonstrates two methods for receiving joystick input: callback and event
loop"""

import sense_hat

USE_CALLBACK = True

def event_loop(sense):
    while True:
        for event in sense.stick.get_events():
            if event.action == "pressed":
                handle_event(sense, event)
                
            elif event.action == "released":
                sense.clear()

def handle_event(sense, event):
    print(event.direction, event.action)
    if event.action == "pressed":
        sense.show_letter(event.direction[0][0].upper())
    elif event.action == "released":
        sense.clear()

def callback_loop(sense):
    sense.stick.direction_any = lambda event: handle_event(sense, event)
    while True:
        pass

if __name__ == "__main__":
    sense = sense_hat.SenseHat()
    print("Ready!")

    if USE_CALLBACK:
        callback_loop(sense)
    else:
        event_loop(sense)
