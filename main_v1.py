import pyaudio
import numpy as np
from scipy.fft import fft
import time
from datetime import datetime
import csv


# thiết lập số chunk (frame), kiểu dữ liệu, kênh mic, tần số lấy mẫu
CHUNK = 2048
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 40000

# lắng nghe mic
p = pyaudio.PyAudio()

stream = p.open(format=FORMAT,
                channels=CHANNELS,
                rate=RATE,
                input=True,
                frames_per_buffer=CHUNK)

haveSound = False
wait = 0
start_time = 0
current_freq = 0
sound_timestamp = 0

# tiền xử lý âm thanh, sử dụng FFT để biến đổi dữ liệu âm thanh sang miền tần số để thu được tần số lớn nhất
def SoundFFT():
    data = stream.read(CHUNK)
    audio_data = np.frombuffer(data, dtype=np.int16)
    fft_result = fft(audio_data)
    peak_frequency = np.argmax(np.abs(fft_result))
    frequency_hz = round(peak_frequency * RATE / CHUNK)
    return frequency_hz

# tính thời gian tồn tại của loại âm thanh
def SoundTime(fq):
    global haveSound, wait, start_time, current_freq, sound_timestamp
    if not haveSound and fq >= 900 and fq <= 4000:
        haveSound = True
        start_time = time.time()
        wait = time.time()
        current_freq = fq
        now = datetime.now()
        sound_timestamp = now.strftime("%Y-%m-%d %H:%M:%S")
    elif haveSound and fq < 1000 and (time.time() - wait)*1000 > 300:
        haveSound = False
        duration = (time.time() - start_time)*1000 - 300
        print(f"{duration}ms     {current_freq}Hz")
        # SoundClassify(current_freq, duration, sound_timestamp)

# phân loại âm thanh dựa trên tần số và thời gian thu được
def SoundClassify(f, t, timestamp):
    if f > 2700:
        print("Snap")
        writer.writerow([timestamp, f'{f}Hz', 'snap'])
    elif (f > 900 and f < 2300) and t > 11:
        print("Clap")
        writer.writerow([timestamp, f'{f}Hz', 'Clap'])
    elif f < 1500 :
        print("Knock")
        writer.writerow([timestamp, f'{f}Hz', 'Knock'])

def main():
    while True:
        try:
            frequency_hz = SoundFFT()
            SoundTime(frequency_hz)
        except KeyboardInterrupt:
            print("Saved!")
            break

if __name__ == "__main__":

    now = datetime.now()
    csv_timestamp = now.strftime("%Y-%m-%d %H%M%S")
    file = open(f'{csv_timestamp}Sound.csv', 'w')
    writer = csv.writer(file)
    writer.writerow(["timestamp", "sound_frequency", "sound_type"])
    print("listenning....")

    main()
    
    stream.stop_stream()
    stream.close()
    p.terminate()