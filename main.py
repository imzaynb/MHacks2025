import pynput
import pyautogui
import time
from dataclasses import dataclass
from typing import Tuple
import threading


# Our files
from get_acceleration import FreeWiliDevice
from graph            import Graph

def get_window_size() -> Tuple[int, int]:
    return pyautogui.size()


def plot_thread(acceleration_function):
    animation = Graph(acceleration_function)
    animation.show()


def main():
    freewili = FreeWiliDevice()
    mouse = pynput.mouse.Controller()

    def acceleration_getter():
        return freewili.acceleration
    
    t1 = threading.Thread(target=plot_thread, args=(acceleration_getter, ), daemon=True)
    t1.start()

    try:
        while True:
            freewili.process_events()
            print(f"{freewili.acceleration=}")
            mouse.move(-freewili.acceleration.x/100, freewili.acceleration.y/100)
            time.sleep(0.01)
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected")
        freewili.end()


if __name__ == "__main__":
    main()