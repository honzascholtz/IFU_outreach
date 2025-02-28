from __future__ import division
import math
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons, RangeSlider

import numpy as np
from pyaudio import PyAudio # sudo apt-get install python{,3}-pyaudio

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
'''
sine_tone(
    # see http://www.phy.mtu.edu/~suits/notefreqs.html
    frequency=440.00, # Hz, waves per second A4
    duration=30, # seconds to play sound
    volume=.01, # 0..1 how loud it is
    # see http://en.wikipedia.org/wiki/Bit_rate#Audio
    sample_rate=22050 # number of samples per second
)
'''

class sonic:
    def __init__(self):
        self.f, self.ax = plt.subplots(1)

        self.sliceax = self.f.add_axes([0.12, 0.95, 0.8, 0.03])
        self.vel_slider = Slider(self.sliceax, 'Speed', valmin=-1000,
                                   valmax=1000,
                                    valinit=0)
        
        self.vel_slider.on_changed(self.slide_update)
        plt.show()
    
    def sine_tone(self, frequency, duration, volume=1, sample_rate=22050):
        n_samples = int(sample_rate * duration)
        restframes = n_samples % sample_rate

        self.p = PyAudio()
        self.stream = self.p.open(format=self.p.get_format_from_width(1), # 8bit
                        channels=1, # mono
                        rate=sample_rate,
                        output=True)
        s = lambda t: volume * math.sin(2 * math.pi * frequency * t / sample_rate)
        samples = (int(s(t) * 0x7f + 0x80) for t in xrange(n_samples))
        for buf in izip(*[samples]*sample_rate): # write several samples at a time
            self.stream.write(bytes(bytearray(buf)))

        # fill remainder of frameset with silence
        self.stream.write(b'\x80' * restframes)

        self.stream.stop_stream()
        self.stream.close()
        self.p.terminate()
    
    def slide_update(self,val):
        freq = 440+ val/1200*440
        self.sine_tone(
            # see http://www.phy.mtu.edu/~suits/notefreqs.html
            frequency=freq, # Hz, waves per second A4
            duration=0.3, # seconds to play sound
            volume=.02, # 0..1 how loud it is
            # see http://en.wikipedia.org/wiki/Bit_rate#Audio
            sample_rate=22050 # number of samples per second
            )
        

inst = sonic()