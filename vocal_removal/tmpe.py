from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
import librosa

from pydub import AudioSegment

import librosa.display

sound = AudioSegment.from_mp3('111.mp3')
AudioSegment.converter = "C:\\ffmpeg\\bin\\ffmpeg.exe"
seg = sound[:len(sound) / 10]
seg.export('222.mp3', format='mp3')

