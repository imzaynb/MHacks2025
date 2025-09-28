import time
from freewili import FreeWili
from freewili.types import FreeWiliProcessorType

def main():
    result = FreeWili.find_first()
    if result.is_err():
        print(f"Device not found: {result.unwrap_err()}")
        return

    fw = result.unwrap()
    if fw.open().is_err():
        print("Failed to open FreeWili")
        return

    # Cycle through a few colors
    colors = [
        (255, 0, 0),   # Red
        (0, 255, 0),   # Green
        (0, 0, 255),   # Blue
        (255, 255, 0), # Yellow
        (255, 255, 255) # White
    ]

    for r, g, b in colors:
        res = fw.set_board_leds(io=0, red=r, green=g, blue=b,
                                processor=FreeWiliProcessorType.Display)
        if res.is_err():
            print(f"LED command failed: {res.unwrap_err()}")
        else:
            print(f"LED set to R={r}, G={g}, B={b}")
        time.sleep(1)

    # Turn off LEDs
    fw.set_board_leds(io=0, red=0, green=0, blue=0,
                      processor=FreeWiliProcessorType.Display)

    fw.close()

if __name__ == "__main__":
    main()
