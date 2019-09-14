from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import librosa

import time
from pydub import AudioSegment

import librosa.display

# sound = AudioSegment.from_mp3('111.mp3')
# AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
# seg = sound[:len(sound) / 10]
# seg.export('222.mp3', format='mp3')


def librosa_vocal_remover(file, output_file, threshold_l=2, threshold_h=10,):

    y, sr = librosa.load(file)

    S_full, phase = librosa.magphase(librosa.stft(y))

    # idx = slice(*librosa.time_to_frames([30, 55], sr=sr))
    plt.figure(figsize=(12, 4))
    librosa.display.specshow(librosa.amplitude_to_db(S_full, ref=np.max),
                             y_axis='log', x_axis='time', sr=sr)

    S_filter = librosa.decompose.nn_filter(S_full,
                                           aggregate=np.median,
                                           metric='cosine',
                                           width=int(librosa.time_to_frames(2, sr=sr)))

    S_filter = np.minimum(S_full, S_filter)

    margin_i, margin_v = threshold_l, threshold_h
    power = 2

    mask_i = librosa.util.softmask(S_filter,
                                   margin_i * (S_full - S_filter),
                                   power=power)
    mask_v = librosa.util.softmask(S_full - S_filter,
                                   margin_v * S_filter,
                                   power=power)

    S_foreground = mask_v * S_full
    D_foreground = S_foreground * phase
    y_foreground = librosa.istft(D_foreground)
    S_background = mask_i * S_full
    D_background = S_background * phase
    y_background = librosa.istft(D_background)

    librosa.output.write_wav('fore_ground.wav', y_foreground, sr)
    librosa.output.write_wav(output_file, y_background, sr)


if __name__ == '__main__':
    librosa_vocal_remover('111.mp3', 'final_111.wav', 2.5, 10)


