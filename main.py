'''
1. Read audio
2. Perform FFT
3. Change light on the Novation Launchpad
'''

import time
import keyboard
from functions_launchpad import light_up_launchpad, everything_off
from functions_audio import init_steam, start_recording, stop_recording, get_fft, fft_to_8x8matrix


# Using the default mic because I am basic b.

everything_off()

# initialize portaudio
p = init_steam()

print("Press 'q' to quit")

while True:
    # start recording data
    stream_object, audio_data = start_recording(p)

    fft_audio_data = get_fft(audio_data)
    print(fft_audio_data)

    # convert fft to nice matrix that can be displayed on launchpad
    matrix_for_launchpad = fft_to_8x8matrix(fft_audio_data)

    light_up_launchpad(position_matrix=matrix_for_launchpad, color=120)

    if keyboard.is_pressed('q'):
        print('Closing stream')
        stop_recording(stream_object=stream_object, p=p)
        everything_off()
        break
    
    
    time.sleep(0.5))
    everything_off()