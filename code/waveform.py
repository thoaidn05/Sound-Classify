import numpy as np
import matplotlib.pyplot as plt
import wave
import os

def getWavInfo(file_patch):    
    wave_file = wave.open(file_patch, 'rb')
    framerate = wave_file.getframerate()
    frames = wave_file.getnframes()
    signal = wave_file.readframes(frames)
    signal = np.frombuffer(signal, dtype=np.int16)
    time = np.linspace(0, frames / framerate, num=len(signal))
    wave_file.close()
    return time, signal

def plot_wave(init, denoised, i):
    init_time, init_signal = getWavInfo(init)
    denoised_time, denoised_signal = getWavInfo(denoised)

    fig, (ax1, ax2) = plt.subplots(2,1, figsize=(10, 8), sharey=True)
    fig.suptitle(f"SOUND {i}")
    ax1.plot(init_time, init_signal, linewidth=0.5)
    ax1.grid(True)

    ax2.plot(denoised_time, denoised_signal, linewidth=0.5)
    ax2.grid(True)

    plt.show()

type_sound = "clap/"
init_path = "./dataset/"
processed_path = "./processed_dataset/"

for i in range(0, 10):
    init_firstFile = init_path + type_sound + os.listdir(init_path + type_sound)[i]

    processed_firstFile = processed_path + type_sound + os.listdir(processed_path + type_sound)[i]

    plot_wave(init_firstFile, processed_firstFile, i)
