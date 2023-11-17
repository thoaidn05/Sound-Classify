import numpy as np
import tensorflow as tf
import keras
import pyaudio
import wave
import numpy as np
from pedalboard.io import AudioFile
import noisereduce as nr

chunk = 1024
sample_format = pyaudio.paInt16 
chanels = 1
smpl_rt = 16000
seconds = 1
pa = pyaudio.PyAudio() 

stream = pa.open(format=sample_format, channels=chanels, 
                rate=smpl_rt, input=True, 
                frames_per_buffer=chunk)

def record(filename):
    print("wait...")
    stream.start_stream()
    frames = [] 
    for i in range(0, int(smpl_rt / chunk * seconds)):
        data = stream.read(chunk)
        frames.append(data)
    stream.stop_stream()

    sf = wave.open(filename, 'wb')
    sf.setnchannels(chanels)
    sf.setsampwidth(pa.get_sample_size(sample_format))
    sf.setframerate(smpl_rt)
    sf.writeframes(b''.join(frames))
    sf.close()

def get_spectrogram(waveform):
  spectrogram = tf.signal.stft(
      waveform, frame_length=255, frame_step=128)
  spectrogram = tf.abs(spectrogram)
  spectrogram = spectrogram[..., tf.newaxis]
  return spectrogram

def predict_model():
  model = keras.models.load_model('newModel.h5')

  x = tf.io.read_file('test.wav')
  x, _ = tf.audio.decode_wav(x, desired_channels=1, desired_samples=16000,)
  x = tf.squeeze(x, axis=-1)
  x = get_spectrogram(x)
  x = x[tf.newaxis,...]
  prediction = model(x)
  labels = ['clap', 'knock', 'snap']
  # if np.max(tf.nn.softmax(prediction[0])) < 0.7:
  #    print("Noise")
  # else:
  print(labels[np.argmax(prediction[0])])
  print(np.max(tf.nn.softmax(prediction[0])))

if __name__ == '__main__':
  isProcessed = False
  while True:
    try:
        stream.start_stream()
        data = stream.read(chunk)
        signal = np.frombuffer(data, dtype=np.int16)
        threshold = 8000
        if np.max(signal) < threshold:
          isProcessed = False
        if np.max(signal) >= threshold and not isProcessed:
          isProcessed = True
          record(f"test.wav")
          with AudioFile('test.wav') as f:
              audio = f.read(f.frames)
          reduced_noise = nr.reduce_noise(y=audio, sr=smpl_rt, stationary=True, prop_decrease=1)
          with AudioFile('test.wav', 'w', smpl_rt, reduced_noise.shape[0]) as f:
              f.write(reduced_noise)
          predict_model()

    except KeyboardInterrupt:
      stream.stop_stream()
      stream.close()
      pa.terminate()
      break
    
