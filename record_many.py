import pyaudio
import numpy as np
from scipy.fft import fft
import time
from datetime import datetime
import csv
import sounddevice as sd
import wave

# thiết lập số chunk (frame), kiểu dữ liệu, kênh mic, tần số lấy mẫu
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

# lắng nghe mic
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

def find_first_last_crossing(signal, threshold):
    crossings = np.where(np.diff((signal > threshold).astype(int)))[0]
    first_crossing = crossings[0]
    last_crossing = crossings[-1]
    return first_crossing, last_crossing

def record_and_save(file_path, duration=0.3, sample_rate=44100):
    # Thu âm từ microphone
    recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=2, dtype='int16')
    sd.wait()

    # Lưu file WAV
    with wave.open(file_path, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(recording.tobytes())

if __name__ == "__main__":
    isProcessed = False
    count = 0

    print("------START------")
    # Lắng nghe liên tục
    while True:
        try:
            stream.start_stream()
            data = stream.read(CHUNK)
            signal = np.frombuffer(data, dtype=np.int16)

            threshold = 1000
            # print(np.max(signal))
            if np.max(signal) < threshold:
                isProcessed = False
            if np.max(signal) >= threshold and not isProcessed:
                print("Have sound")
                isProcessed = True
                record_and_save(f"clap/clap{count}.wav")
                count+=1


        except KeyboardInterrupt:
            print("------CLOSE------")
            break
