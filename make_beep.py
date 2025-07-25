import wave
import struct
import math

freq = 3000.0
duration = 5.0
volume = 32767.0

sample_rate = 44100
num_samples = int(sample_rate * duration)

wav_file = wave.open('alert.wav', 'w')
wav_file.setparams((1, 2, sample_rate, num_samples, 'NONE', 'not compressed'))

for i in range(num_samples):
    value = int(volume * math.sin(2 * math.pi * freq * (i / sample_rate)))
    wav_file.writeframes(struct.pack('h', value)) 

wav_file.close()
