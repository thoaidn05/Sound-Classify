import os
import pathlib
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import tensorflow as tf
from IPython import display
import keras


def get_spectrogram(waveform):
  spectrogram = tf.signal.stft(
      waveform, frame_length=255, frame_step=128)
  spectrogram = tf.abs(spectrogram)
  spectrogram = spectrogram[..., tf.newaxis]
  return spectrogram

model = keras.models.load_model('mymodel.h5')

x = tf.io.read_file('_test.wav')
x, sample_rate = tf.audio.decode_wav(x, desired_channels=1, desired_samples=16000,)
x = tf.squeeze(x, axis=-1)
waveform = x
x = get_spectrogram(x)
x = x[tf.newaxis,...]

prediction = model(x)
x_labels = ['clap', 'knock', 'snap']
plt.bar(x_labels, tf.nn.softmax(prediction[0]))
plt.title('Result')
plt.show()

display.display(display.Audio(waveform, rate=16000))