import pyaudio
import wave
import numpy as np

chunk = 1024
sample_format = pyaudio.paInt16 
chanels = 1
smpl_rt = 44100
seconds = 1
pa = pyaudio.PyAudio() 

stream = pa.open(format=sample_format, channels=chanels, 
                rate=smpl_rt, input=True, 
                frames_per_buffer=chunk)

def record(filename):
    print('Recording...')
    stream.start_stream()
    frames = [] 
    for i in range(0, int(smpl_rt / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    print('Done !!! ')
    stream.stop_stream()

    sf = wave.open(filename, 'wb')
    sf.setnchannels(chanels)
    sf.setsampwidth(pa.get_sample_size(sample_format))
    sf.setframerate(smpl_rt)
    sf.writeframes(b''.join(frames))
    sf.close()

if __name__ == "__main__":
    isProcessed = False
    count = 100
    while True:
        try:
            stream.start_stream()
            data = stream.read(chunk)
            signal = np.frombuffer(data, dtype=np.int16)
            # print(np.max(signal))
            threshold = 10000
            if np.max(signal) < threshold:
                isProcessed = False
            if np.max(signal) >= threshold and not isProcessed:
                isProcessed = True
                record(f"dataset/clap/clap{count}.wav")
                count+=1

        except KeyboardInterrupt:
            stream.stop_stream()
            stream.close()
            pa.terminate()
            break