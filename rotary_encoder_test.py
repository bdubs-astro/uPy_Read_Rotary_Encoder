'''
Tests a class used to read a KY-040 rotary encoder using interrupts.

Resources:
https://github.com/gurgleapps/rotary-encoder
https://gurgleapps.com/learn/electronics/ky-040-rotary-encoder-on-a-raspberry-pi-pico-detailed-explanation-and-step-by-step-code
'''

from rotary_bdw import Rotary
import utime as time

rotary = Rotary(16,17,18)  # pin numbers: clk,dt,sw
val = 0

def rotary_changed(event):
    global val
    if event == Rotary.ROT_CW:
        val +=  1
        print(val)
    elif event == Rotary.ROT_CCW:
        val -= 1
        print(val)
    elif event == Rotary.SW_PRESS:
        print('Switch Pressed')
    elif event == Rotary.SW_RELEASE:
        print('Switch Released')
        val = 0 # reset position
        print(val)
        
rotary.add_handler(rotary_changed)

while True:
    time.sleep_ms(10)