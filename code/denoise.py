from pedalboard.io import AudioFile
from pedalboard import *
import noisereduce as nr
import os

# def denoise(path, type, file):
#     sr=16000
#     with AudioFile(path + type + file) as f:
#         audio = f.read(f.frames)

#     reduced_noise = nr.reduce_noise(y=audio, sr=sr, stationary=True, prop_decrease=0.1)
    
#     # board = Pedalboard([
#     #     NoiseGate(threshold_db=-30, ratio=1.5, release_ms=250),
#     #     Compressor(threshold_db=-16, ratio=2.5),
#     #     LowShelfFilter(cutoff_frequency_hz=700, gain_db=10, q=1),
#     #     Gain(gain_db=10)
#     # ])

#     # effected = board(reduced_noise, sr)

#     with AudioFile("./processed_dataset/" + type + file, 'w', sr, reduced_noise.shape[0]) as f:
#         f.write(reduced_noise)

# if __name__ == "__main__":
#     type_sound = "clap/"
#     path = "./dataset/"
#     listFiles = os.listdir(path + type_sound)

#     for file in listFiles:
#         denoise(path, type_sound, file)




sr=16000
with AudioFile('test.wav') as f:
    audio = f.read(f.frames)

reduced_noise = nr.reduce_noise(y=audio, sr=sr, stationary=True, prop_decrease=1)

with AudioFile('_test.wav', 'w', sr, reduced_noise.shape[0]) as f:
    f.write(reduced_noise)