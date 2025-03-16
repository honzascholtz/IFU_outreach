#!/usr/bin/env python3
#############################################################################
# Filename    : Dimmable_mine.py
# Description : Use rotary encoder to control LED brightness. 
# Author      : www.freenove.com
# modification: 2025/01/01
########################################################################

from gpiozero import RotaryEncoder,Button,PWMLED
import time
import numpy as np

class light_rgb:
	def __init__(self):
		self.led_r = PWMLED(5)
		self.led_g = PWMLED(6)
		self.led_b = PWMLED(13)
		
	def light_up_r(self, val=0.3):
		while True:
			self.led_r.value = val
			time.sleep(0.5)
			self.led_r.value = 0
			print('Blink')
		
	def destroy(self):
		
		self.led_r.close()  
		self.led_g.close()
		self.led_b.close()  
		

class Light_loop:
	def __init__(self):
		self.CounterValue = 0
		self.NextCounterValue = 0
		self.button = Button(27) # define Button pin according to BCM Numbering 
		self.rotor = RotaryEncoder(17, 18,max_steps=30, wrap=True)# pins 17 and 18, max steps = 30
		self.led_red = PWMLED(22)
		self.led_blue = PWMLED(19)

		self.value_red= 0
		self.value_blue = 0
	
	def red(self):
		self.CounterValue = self.rotor.steps
		self.value_red = abs(np.sin((self.CounterValue/30)*2*np.pi))
		self.value_blue = abs(-np.cos((self.CounterValue/30)*2*np.pi))

	def reset(self):
		self.CounterValue = 0

	def loop(self):
		self.button.when_pressed = self.reset
		self.rotor.when_rotated = self.red
		

		while True:
			if self.NextCounterValue != self.CounterValue:
				print('value red = %.2f' % self.value_red + ' value blue = %.2f' % self.value_blue )
				self.NextCounterValue = self.CounterValue
				print(self.rotor.steps)
				
			self.led_red.value = self.value_red    # set dc value as the duty cycle
			self.led_blue.value = self.value_blue
			time.sleep(0.01)
			
	def destroy(self):
		self.button.close()    
		self.rotor.close()   
		self.led_red.close()  
		self.led_blue.close()
		 
if __name__ == '__main__':     # Program start from here
	
	print ('Program is starting ... ')
	
	try:
		main = light_rgb()
		main.light_up_r()

	except KeyboardInterrupt:  # When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		print('')
		main.destroy()
		print("Ending program")
