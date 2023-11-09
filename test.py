import pyaudio
import numpy as np
from scipy.fft import fft
import time
from datetime import datetime
import csv
import sounddevice as sd
import wave

# thiết lập số chunk (frame), kiểu dữ liệu, kênh mic, tần số lấy mẫu
CHUNK = 1024
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

def record_and_save(file_path, duration=0.3, sample_rate=RATE):
    # Thu âm từ microphone
    recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=2, dtype=np.int16)
    sd.wait()

    # Lưu file WAV
    with wave.open(file_path, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(recording.tobytes())

def get_time(file_path):
    # Đọc file WAV
    wave_file = wave.open(file_path, 'rb')
    
    # Lấy thông tin từ file WAV
    framerate = wave_file.getframerate()
    frames = wave_file.getnframes()
    
    # Đọc dữ liệu âm thanh
    _signal = wave_file.readframes(frames)
    _signal = np.frombuffer(_signal, dtype=np.int16)
    
    # Tính thời gian cho trục x
    time = np.linspace(0, frames / framerate, num=len(_signal))

    # Xác định điểm vượt qua biên độ ngưỡng đầu tiên và cuối cùng
    _threshold = 800
    first_crossing, last_crossing = find_first_last_crossing(_signal, _threshold)
    
    # Tính thời gian tương ứng
    time_first_crossing = time[first_crossing]
    time_last_crossing = time[last_crossing] 
        
    # Đóng file WAV
    wave_file.close()

    return round((time_last_crossing - time_first_crossing)*1000)

def classify(t, f):
    isClap = (t > 100) and (f > 1400 and f < 2500)
    isSnap = t < 100 and f > 2300
    isKnock = (t > 100) and (f < 1400 and f > 900)

    if isClap:
        print("Clap")
    elif isKnock:
        print("Knock")
    elif isSnap:
        print("Snap")
    else:
        print("Không xác định")

if __name__ == "__main__":
    filename = "cache.wav"
    isEnable = True
    timeOfSound = 0
    freqOfSound = 0
    isWarningEnable = True
    count = 0
    freqOfSound = 0

    print("------START------")
    # Lắng nghe liên tục
    while True:
        try:
            data = stream.read(CHUNK)
            signal = np.frombuffer(data, dtype=np.int16)
            fft_result = fft(signal)
            peak_frequency = np.argmax(np.abs(fft_result))
            frequency_hz = round(peak_frequency * RATE / CHUNK)
            # print(frequency_hz)

            if frequency_hz >= 900 and frequency_hz <= 4000:
                freqOfSound += frequency_hz
                count +=1
                
            
            if frequency_hz < 200 and not isEnable:
                isEnable = True
                classify(timeOfSound, round(freqOfSound/count))
                print(f"{timeOfSound}ms   {round(freqOfSound/count)}Hz")
                freqOfSound = 0
                count = 0

            elif frequency_hz >= 900 and frequency_hz <= 4000 and isEnable:
                record_and_save(filename)
                timeOfSound = get_time(filename)   
                isEnable = False
                isWarningEnable = True

        except IndexError:
            if isWarningEnable:
                print("Khong nghe ro")
                isWarningEnable = False
            continue
        except KeyboardInterrupt:
            print("------CLOSE------")
            break
