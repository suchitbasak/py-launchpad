'''
1. Read audio
2. Perform FFT
3. Change light on the Novation Launchpad

Optional:
Have a little gui with the launchpad in it
'''

import time
import numpy as np
import pyaudio
from launchpad import light_up_matrix, everything_off

GRID_ROWS = 8
GRID_HEIGHT = 8

# Part 1: Record audio

# Using the default mic because I am basic b.

CHUNKSIZE = 10000 # fixed chunk size

# initialize portaudio
p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=1000, input=True, frames_per_buffer=CHUNKSIZE)


while True:
    print("Recording in progress...")
    try:
        chunky_bytes = stream.read(CHUNKSIZE, exception_on_overflow = False)
    except:
        pass
    
    chunky_np = np.frombuffer(chunky_bytes, dtype=np.int16)

    # close stream
    stream.stop_stream()
    stream.close()
    p.terminate()

    print("Recording over")

    # FFFFFFFFT
    chunky_freq = np.fft.fft(chunky_np, GRID_ROWS)

    # normalize and quantize this
    chunky_norm = np.abs(chunky_freq)/ max(np.abs(chunky_freq))
    chunky_norm = GRID_HEIGHT * chunky_norm
    chunky_round = np.round(chunky_norm)

    
    # Convert to 8x8 matrix to give input to function for launchpad
    mat = np.zeros((8,8))
    for i in range(8):
        for j in range(int(chunky_round[i])):
            mat[i,j] = 1


    mat =np.flip(mat,1)
    mat = np.transpose(mat)
    mat = np.flip(mat,0)

    light_up_matrix(position_matrix=mat, color=12)
    time.sleep(0.1)
    everything_off()

# plot data
#plt.plot(chunky_np)
#plt.show()