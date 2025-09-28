# python libs
import time

# external libs
from freewili          import FreeWili
from freewili.types    import EventType, AccelData
from freewili.framing  import ResponseFrame

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

