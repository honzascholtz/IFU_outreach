from tkinter import Tk, Label, Button
import os
from pyaudio import PyAudio # sudo apt-get install python{,3}-pyaudio
import math
import time

try:
    from itertools import izip
except ImportError: # Python 3
    izip = zip
    xrange = range

def sine_tone(frequency, duration, volume=1, sample_rate=22050):
    n_samples = int(sample_rate * duration)
    restframes = n_samples % sample_rate

    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(1), # 8bit
                    channels=1, # mono
                    rate=sample_rate,
                    output=True)
    s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)
    samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))
    for buf in izip(*[samples]*sample_rate): # write several samples at a time
        stream.write(bytes(bytearray(buf)))

    # fill remainder of frameset with silence
    stream.write(b'\x80' * restframes)

    stream.stop_stream()
    stream.close()
    p.terminate()


class MyFirstGUI:
    def __init__(self, master):
        self.master = master
        master.title("Random Tone Generator")

        self.label = Label(master, text="Press Generate and enjoy")
        self.label.pack()

        self.generate_button = Button(master, text="Generate", command=self.generate)
        self.generate_button.pack()

        self.close_button = Button(master, text="Close", command=master.quit)
        self.close_button.pack()

    def generate(self):
        while True:
            sine_tone(
                # see http://www.phy.mtu.edu/~suits/notefreqs.html
                frequency=440.00, # Hz, waves per second A4
                duration=0.1, # seconds to play sound
                volume=.01, # 0..1 how loud it is
                # see http://en.wikipedia.org/wiki/Bit_rate#Audio
                sample_rate=22050 # number of samples per second
                )
            time.sleep(0.1)


root = Tk()
my_gui = MyFirstGUI(root)
root.mainloop()