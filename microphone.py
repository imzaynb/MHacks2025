import sounddevice as sd
import vosk
import queue
import json

model = vosk.Model("/Users/chiragbhat/CLionProjects/MHacks2025/vosk-model-small")
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

with sd.RawInputStream(samplerate=16000, blocksize=500, dtype='int16',
                       channels=1, callback=callback):
    rec = vosk.KaldiRecognizer(model, 16000)
    print("Speak something...")
    while True:
        data = q.get()
        if rec.AcceptWaveform(data):
            # Full result for completed words
            result = json.loads(rec.Result())
            text = result.get("text", "")
            if text:
                print("Detected:", text)
        else:
            # Partial result for in-progress recognition
            partial = json.loads(rec.PartialResult())
            text = partial.get("partial", "")
            if text:
                print("Partial:", text)
