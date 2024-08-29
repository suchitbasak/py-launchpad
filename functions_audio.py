# audio related functions live here

import time
import numpy as np
import pyaudio
from scipy.fft import fft

# Record audio
# Using the default mic because I am basic b.

CHUNKSIZE = 1024 # fixed chunk size
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100

GRID_ROWS = 8
GRID_HEIGHT = 8


def init_steam():
    # initialize portaudio and return it so that the start and stop recording functions can us it 
    p = pyaudio.PyAudio()
    return(p)
    

def start_recording(p):
    # open an audio stream
    stream_object = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNKSIZE)

    # read data from the stream
    raw_data = stream_object.read(CHUNKSIZE)

    # convert raw byte data to numpy array
    audio_data = np.frombuffer(raw_data, dtype=np.int16)
    return(stream_object, audio_data)


def stop_recording(stream_object, p):
    # this function closes the stream and pyaudio
    stream_object.stop_stream()
    stream_object.close()
    p.terminate()


def get_fft(audio_data):
    yf = fft(audio_data, CHUNKSIZE)
    yf = np.abs(yf)

    return(yf)


def fft_to_8x8matrix(yf):
    # process fft amplitudes to an 8x8 matrix and make it fit on launchpad grid

    # the length of the fft = CHUNKSIZE but we need only 8 samples to get it to fit on a launchpad
    step = int(CHUNKSIZE/GRID_ROWS)
    yf = yf[::step] # start from 0, end at the last element, takes steps of 1024/8 = 128

    # yes, we could have set the length of FFT to GRID_ROWS = 8
    # but increasing the FFT length gives better granularity and makes the lights move nicer

    # lets normalize it and multiply by 8 (GRID_HEIGHT) so that the max value will correspond to 8
    yf_scaled = yf/np.max(yf) * GRID_HEIGHT
    yf_scaled = np.round(yf_scaled)

    # yf_scaled looks something like this: [2. 4. 8. 3. 5. 3. 8. 4.]

    # we need to convert it to a matrix
    # in the main function, this matrix will then be sent to the launchpad
    matrix_for_launchpad = np.zeros((8,8))
    for i in range(8):
        for j in range(int(yf_scaled[i])):
            matrix_for_launchpad[i,j] = 1
    return(matrix_for_launchpad)