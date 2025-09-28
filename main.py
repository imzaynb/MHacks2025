import pynput
import pyautogui
import time
from dataclasses import dataclass
from typing import Tuple

# Our files
from get_acceleration import FreeWiliDevice
from graph            import Graph

def get_window_size() -> Tuple[int, int]:
    return pyautogui.size()

def main():
    freewili = FreeWiliDevice()
    mouse = pynput.mouse.Controller()
    animation = Graph()

    try:
        while True:
            freewili.process_events()
            print(f"{freewili.acceleration=}")
            mouse.move(-freewili.acceleration.x/100, freewili.acceleration.y/100)
            animation.set_acceleration(freewili.acceleration)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected")
        freewili.end()


if __name__ == "__main__":
    main()