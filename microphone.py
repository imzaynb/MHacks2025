import sounddevice as sd
import vosk
import queue
import json
import pynput
from free_wili import FreeWiliDevice

model = vosk.Model("./vosk-model-small")
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))


def voiceThread(freewili, setPause):
    with sd.RawInputStream(samplerate=16000, blocksize=500, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, 16000)
        # print("Speak something...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                # Full result for completed words
                result = json.loads(rec.Result())
                text = result.get("text", "")
                if text:
                    word = text.split(" ")[0].lower()
                    with pynput.mouse.Controller() as mouse:
                        match(word):
                            case "click":
                                mouse.click(pynput.mouse.Button.left, 1)
                                freewili.configure_led(FreeWiliDevice.Colors.BLUE, 0.3)
                                print("CLICK")
                            case "left":
                                mouse.click(pynput.mouse.Button.left, 1)
                                freewili.configure_led(FreeWiliDevice.Colors.BLUE, 0.3)
                                print("LEFT")
                            case "double":
                                mouse.click(pynput.mouse.Button.left, 2)
                                freewili.configure_led(FreeWiliDevice.Colors.GREEN, 0.3)
                                print("DOUBLE")
                            case "right":
                                mouse.click(pynput.mouse.Button.right, 1)
                                freewili.configure_led(FreeWiliDevice.Colors.PURPLE, 0.3)
                                print("RIGHT")
                            case "hold":
                                mouse.press(pynput.mouse.Button.left)
                                freewili.configure_led(FreeWiliDevice.Colors.YELLOW, 0.3, True)
                                print("HOLD")
                            case "release":
                                mouse.release(pynput.mouse.Button.left)
                                freewili.configure_led(FreeWiliDevice.Colors.OFF, 0.3)
                                print("RELEASE")
                            case "scroll":
                                mouse.scroll(0, 100)
                                freewili.configure_led(FreeWiliDevice.Colors.WHITE, 0.3)
                                print("SCROLL")
                            case "paused":
                                setPause(False)
                                freewili.configure_led(FreeWiliDevice.Colors.RED, 0.3, True)
                                print("PAUSED")
                            case "resume":
                                setPause(True)
                                freewili.configure_led(FreeWiliDevice.Colors.GREEN, 0.1)
                                print("RESUME")
            # else:
            #     # Partial result for in-progress recognition
            #     partial = json.loads(rec.PartialResult())
            #     text = partial.get("partial", "")
            #     if text:
            #         print("Partial:", text)
    pass
