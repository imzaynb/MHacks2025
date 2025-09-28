import pynput
import pyautogui
import time
from typing import Tuple
import matplotlib.pyplot as plt

# Our files
from get_acceleration import FreeWiliDevice
from graph import Graph
from physics import PhysicsEngine

def get_window_size() -> Tuple[int, int]:
    return pyautogui.size()

def main():
    freewili = FreeWiliDevice()
    mouse = pynput.mouse.Controller()

    # Create physics engine
    physics = PhysicsEngine(lambda: freewili.acceleration)

    # Optionally enable graphing
    enable_graph = False
    if enable_graph:
        graph = Graph(physics)

    try:
        while True:
            freewili.process_events()

            # Update physics
            ax, vel_x, pos_x, ay, vel_y, pos_y = physics.update()

            # Move mouse using the clamped positions
            mouse.position = (1920-pos_y, 1080-pos_x)

            # Update graph if enabled
            if enable_graph:
                plt.pause(0.01)

    except KeyboardInterrupt:
        print("Keyboard Interrupt detected")
        freewili.end()

if __name__ == "__main__":
    main()
