import numpy as np
import matplotlib.pyplot as plt
import wave
import os

def find_first_last_crossing(signal, threshold):
    crossings = np.where(np.diff((signal > threshold).astype(int)))[0]
    
    first_crossing = crossings[0]
    last_crossing = crossings[-1]
    return first_crossing, last_crossing

def plot_wave(file_path):
    # Đọc file WAV
    wave_file = wave.open(file_path, 'rb')
    
    # Lấy thông tin từ file WAV
    framerate = wave_file.getframerate()
    frames = wave_file.getnframes()
    
    # Đọc dữ liệu âm thanh
    signal = wave_file.readframes(frames)
    signal = np.frombuffer(signal, dtype=np.int16)
    
    # Tính thời gian cho trục x
    time = np.linspace(0, frames / framerate, num=len(signal))
    
    # Biểu diễn sóng âm thanh
    plt.figure(figsize=(10, 4))
    plt.plot(time, signal, linewidth=0.5)
    plt.xlabel('Thời Gian (s)')
    plt.ylabel('Biên Độ')
    plt.title('Biểu Đồ Sóng Âm Thanh')
    plt.grid(True)

    # Xác định điểm vượt qua biên độ ngưỡng đầu tiên và cuối cùng
    threshold = 1000
    first_crossing, last_crossing = find_first_last_crossing(signal, threshold)
    
    # Tính thời gian tương ứng
    time_first_crossing = time[first_crossing]
    time_last_crossing = time[last_crossing]
    
    print(f'Thời gian tồn tại của tiếng động: {(time_last_crossing - time_first_crossing)*1000} ms')

    # Đánh dấu điểm vượt qua biên độ ngưỡng đầu tiên và cuối cùng
    plt.scatter([time_first_crossing, time_last_crossing], [threshold, threshold], color='red', marker='o')
    plt.show()

    # Đóng file WAV
    wave_file.close()

# Đường dẫn đến file WAV của bạn
# file_path = 'knock/knock0.wav'
# plot_wave(file_path)

path = os.getcwd() + "/clap"
files = os.listdir(path)
for file in files:
    plot_wave(path + "/" + file)
