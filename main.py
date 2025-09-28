import pynput
import time
from dataclasses import dataclass
import matplotlib.pyplot as plt

# Our files
from free_wili import FreeWiliDevice
from graph     import Graph
from physics    import Physics       

def main():
    freewili = FreeWiliDevice()
    physics  = Physics(lambda: freewili.acceleration)
    mouse = pynput.mouse.Controller()

    enable_graph = False 
    if enable_graph:
        graph = Graph(lambda: physics.acceleration, lambda: physics.velocity, lambda: physics.position)

    try:
        while True:
            freewili.process_events()
            physics.step()
            mouse.position = (physics.position.y, 1080-physics.position.x)
            if enable_graph:
                plt.pause(0.01)
    except KeyboardInterrupt:
        print("Keyboard Interrupt detected")
        freewili.end()


if __name__ == "__main__":
    main()
