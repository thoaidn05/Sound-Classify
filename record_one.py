import sounddevice as sd
import wave

def record_and_save(file_path, duration=2, sample_rate=44100):
    # Thu âm từ microphone
    recording = sd.rec(int(sample_rate * duration), samplerate=sample_rate, channels=2, dtype='int16')
    print("Recording....")
    sd.wait()

    # Lưu file WAV
    with wave.open(file_path, 'w') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(recording.tobytes())
    print("Saved!")

if __name__ == "__main__":
    file_path = "cache.wav"
    record_and_save(file_path)
    print(f"Đã thu âm và lưu file: {file_path}")
