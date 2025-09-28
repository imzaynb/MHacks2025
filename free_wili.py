# python libs
import time

# external libs
from freewili          import FreeWili
from freewili.types    import FreeWiliProcessorType, EventType, AccelData
from freewili.framing  import ResponseFrame
from enum              import Enum

# personal files
from helpers           import deadband, Vec3d 

class UnableToFindDevice(Exception):
    def __init__(self, err_string: str, message="Device not found: "):
        self.err_string = err_string
        self.message = f"{message}: {err_string}"
        super().__init__(self.message)

class FailToOpenDevice(Exception):
    def __init__(self, message="Fail to open FreeWili"):
        self.message = message
        super().__init__(self.message)


class FreeWiliDevice():
    class Colors(Enum): 
        RED = (60, 0, 0) 
        GREEN = (0, 60, 0) 
        BLUE = (0, 0, 60)
        YELLOW = (30, 30, 0)
        PURPLE = (30, 0, 30)
        WHITE = (20, 20, 20)
        OFF = (0, 0, 0)
    def __init__(self, acceleration_period=1):
        self.acceleration_period = acceleration_period

        result = FreeWili.find_first()
        if result.is_err():
            raise UnableToFindDevice(result.unwrap_err())
        
        self.freewili = result.unwrap()
        self.freewili.set_event_callback(self.event_handler)

        # print(f"{self.freewili=}")

        if self.freewili.open().is_err():
            raise FailToOpenDevice()

        # Increasing the number parameter will make the event come in slower 
        self.freewili.enable_accel_events(True, self.acceleration_period)

        self.acceleration = Vec3d(0, 0, 0)

    def process_events(self):
        self.freewili.process_events()

    def end(self):
        self.freewili.enable_accel_events(False)
        self.freewili.close()


    def loop(self):
        try:
            while True:
                self.process_events()
                time.sleep(0.01)
        except KeyboardInterrupt:
            print("Keyboard Interrupt detected")
            self.end()

    def configure_led(self, color: Colors, duration: float = 1.0, hold: bool = False):
        r, g, b = color.value

        for io in range(7):
            res = self.freewili.set_board_leds(
                io=io,
                red=r,
                green=g,
                blue=b,
                processor=FreeWiliProcessorType.Display
            )
            # if res.is_err():
            #     print(f"LED {io} command failed: {res.unwrap_err()}")
            # else:
            #     print(f"LED {io} set to {color.name} (R={r}, G={g}, B={b})")
        if not hold:
            # Keep the color for `duration` seconds
            time.sleep(duration)

            # Turn off all LEDs
            for io in range(7):
                self.freewili.set_board_leds(
                    io=io,
                    red=0,
                    green=0,
                    blue=0,
                    processor=FreeWiliProcessorType.Display
                )
            # print("All LEDs turned off")



    def event_handler(self, event_type: EventType, frame: ResponseFrame, data):
        if event_type == EventType.Accel and isinstance(data, AccelData):
            self.acceleration.x = deadband(data.x, 3000)
            self.acceleration.y = deadband(data.y, 3000)
            self.acceleration.z = deadband(data.z, 3000)

        
def main():
    freewili = FreeWiliDevice()
    freewili.loop()

if __name__ == "__main__":
    main()

