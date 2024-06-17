# LED blink on the Lunchpad MK2
# ref: Launchpad MK2 developers guide

import time
import mido
from mido import Message



# Get the list of available output ports
# because we need to talk to the midi device and don't need to listen it
available_out_ports= mido.get_output_names()
print(available_out_ports)

# we know which device we want to talk to
portname = "Launchpad MK2"

# open it as an output port
port = mido.open_output(portname)

# Send a note_on
# note = 11 ==> pad on the bottom left corner, check developers guide pg. 7 fig 4
on = Message('note_on', note=11, velocity=12)
port.send(on)

# Watch the pad glow
time.sleep(1)

# Watch the pad change color
# change velocity to change color, check developers guide pg. 5 fig 2
on = Message('note_on', note=11, velocity=20)
port.send(on)

# Watch the pad change color~
time.sleep(1)

# Switch if off
off = Message('note_off', note=11)
port.send(off)

# Finally, LED blink~
for i in range(127):
    on = Message('note_on', note=11, velocity = i)
    port.send(on)
    time.sleep(0.1)

port.send(off)


# no no wait, lets do the whole board now
list_of_notes = []

# Get a list of ports, again, look at the dev guide for ref
# range(start, stop)
for i in range(1, 9):
    for j in range(1,9):
        list_of_notes.append(i*10+j)

# there are 127 colors

for color in range(127):
    for note in list_of_notes:
            on = Message('note_on', note=note, velocity=color)
            port.send(on)
    time.sleep(0.1)


# lets switch everything off now

for note in list_of_notes:
     off = Message('note_off', note=note)
     port.send(off)


print('Done!')