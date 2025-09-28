import pynput
import pyautogui
import time
from dataclasses import dataclass
from typing import Tuple
import threading
import matplotlib.pyplot as plt


# Our files
from get_acceleration import FreeWiliDevice
from graph            import Graph

def get_window_size() -> Tuple[int, int]:
    return pyautogui.size()
    


def main():


    freewili = FreeWiliDevice()
    mouse = pynput.mouse.Controller()

    def acceleration_getter():
        return freewili.acceleration
    
    animation = Graph(acceleration_getter)

    try:
        while True:
            freewili.process_events()
            mouse.position = (animation.position_x_smooth[-1], 500)
            plt.pause(0.01)
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected")
        freewili.end()


if __name__ == "__main__":
    main()